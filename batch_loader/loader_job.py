__author__ = 'shilavantarp'

"""
Job Parent Class

References:
http://stackoverflow.com/questions/9802102/python-mysql-when-to-explicitly-rollback-a-transaction
"""

import sys
import logging
import traceback
import collections
import functools
import ConfigParser
from datetime import datetime

logger = logging.getLogger("pulsar")

from utils import get_logger, Database


class memorized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


def update_ops_batch(db_cursor, batch_start_time, success_flag, status_desc, batch_key):
    end_time = datetime.now()
    elapsed_job_time = end_time - batch_start_time
    elapsed_job_time_seconds = ((elapsed_job_time.seconds + elapsed_job_time.days * 24 * 3600) * 10**6) / 10**6
    total_elapsed_time_sec = round(float("%s.%s" % (elapsed_job_time_seconds, elapsed_job_time.microseconds)), 4) # 4 digit precision
    row_dict = {'EndTime': end_time,
                'BatchSuccessFlag': success_flag,
                'DurationSeconds': total_elapsed_time_sec,
                'StatusDesc': status_desc,
                'RowModifiedDate': datetime.now(),
                'BatchKey': batch_key}
    sql_query = """UPDATE OPS_Batch
                   SET EndTime = %(EndTime)s,
                       BatchSuccessFlag = %(BatchSuccessFlag)s,
                       DurationSeconds = %(DurationSeconds)s,
                       StatusDesc = %(StatusDesc)s,
                       RowModifiedDate = %(RowModifiedDate)s
                   WHERE BatchKey = %(BatchKey)s;
                """
    db_cursor.execute(sql_query, row_dict)


def create_ops_batch(batch_name, db_cursor):
    batch_start_time = datetime.now()
    #self.logger.info("Batch started at: %s" % self.batch_start_time)
    row_dict = {'BatchName': batch_name,
                'StartTime': batch_start_time,
                'BatchSuccessFlag': 0,
                'RowCreatedDate': datetime.now()}
    sql_query = """INSERT INTO OPS_Batch(
                    BatchName,
                    StartTime,
                    BatchSuccessFlag,
                    RowCreatedDate
                ) VALUES (%(BatchName)s, %(StartTime)s, %(BatchSuccessFlag)s, %(RowCreatedDate)s);
                """
    db_cursor.execute(sql_query, row_dict)

    # need the key just inserted
    sql_query = "SELECT LAST_INSERT_ID() AS BatchKey"
    db_cursor.execute(sql_query)
    sql_results = db_cursor.fetchone()
    return sql_results['BatchKey'], batch_start_time


def get_last_batch_details(batch_name, db_cursor):
    batch_key = None
    success_flag = None
    sql_query = """SELECT BatchKey, BatchSuccessFlag FROM OPS_Batch
                    WHERE BatchName='%s' AND BatchSuccessFlag = 1 ORDER BY BatchKey DESC LIMIT 1;""" % batch_name
    db_cursor.execute(sql_query)
    res = db_cursor.fetchone()
    if res:
        batch_key = res['BatchKey']
        success_flag = res['BatchSuccessFlag']
    return batch_key, success_flag


class LoaderBatch(object):

    def __init__(self, batch_key, config_filename, raw_conn=None, raw_db_cursor=None):
        self.batch_key = batch_key
        self.config_filename = config_filename
        self.array_size = 10000
        self.config = self.get_config(config_filename)

        # get loggers
        section = 'main'
        logger = get_logger(self.config(section, "log_filename"))
        self.log = logger.log

        # DB Connections
        if raw_conn is None or raw_db_cursor is None:
            self.raw_conn, self.raw_db_cursor = self.get_db_cursor(self.config, 'raw_db')
        else:
            self.raw_conn = raw_conn
            self.raw_db_cursor = raw_db_cursor

    @classmethod
    def get_config(cls, config_filename):
        section = 'main'
        config = ConfigParser.ConfigParser()
        return config.read(config_filename)

    @classmethod
    def get_db_cursor(cls, config):
        db = Database(**config)
        return db._connect(), db._conn.cursor()


class LoaderJob(LoaderBatch):

    def __init__(self, batch_name, job_name, batch_key, last_batch_key=None, last_batch_success_flag=None,
                 config_filename=None, raw_conn=None, raw_db_cursor=None):
        LoaderBatch.__init__(self, batch_key, config_filename, raw_conn=raw_conn, raw_db_cursor=raw_db_cursor)
        self.batch_name = batch_name
        self.job_name = job_name
        self.last_batch_key = last_batch_key
        self.last_batch_success_flag = last_batch_success_flag
        self.stats_tuple = collections.namedtuple("Stats", ['success_count', 'fail_count', 'dup_count', 'start_time',
                                                            'target_tblname', 'last_reference_field'])

        # Make an entry in OPS_Batch table
        self.pre_processor()

    def stats(self, success_flag, status_desc):
        self.log(logging.INFO, 'stats: successes %s, failures %s, duplicates %s' % (self.stats_obj.success_count,
                                                                                    self.stats_obj.fail_count,
                                                                                    self.stats_obj.dup_count))
        end_time = datetime.now()
        elapsed_job_time = end_time - self.stats_obj.start_time
        elapsed_job_time_seconds = ((elapsed_job_time.seconds + elapsed_job_time.days * 24 * 3600) * 10**6) / 10**6
        total_elapsed_time_sec = round(float("%s.%s" % (elapsed_job_time_seconds, elapsed_job_time.microseconds)), 4) # 4 digit precision

        if self.stats_obj.fail_count:
            success_flag = 0
        row_dict = {'JobKey': self.job_key,
                    'TableName': self.stats_obj.target_tblname,
                    'StartTime': self.stats_obj.start_time,
                    'EndTime': end_time,
                    'TaskSuccessFlag': success_flag,
                    'TaskLastReferenceString': self.stats_obj.last_reference_field,
                    'DurationSeconds': total_elapsed_time_sec,
                    'SuccessCount': self.stats_obj.success_count,
                    'FailureCount': self.stats_obj.fail_count,
                    'DuplicateCount': self.stats_obj.dup_count,
                    'StatusDesc': status_desc,
                    'RowCreatedDate': end_time,
                    'RowModifiedDate': end_time}

        sql_query = """INSERT INTO OPS_Task(
                        JobKey,
                        TableName,
                        StartTime,
                        EndTime,
                        TaskSuccessFlag,
                        TaskLastReferenceString,
                        DurationSeconds,
                        SuccessCount,
                        FailureCount,
                        DuplicateCount,
                        StatusDesc,
                        RowCreatedDate,
                        RowModifiedDate
                    ) VALUES (%(JobKey)s, %(TableName)s, %(StartTime)s, %(EndTime)s, %(TaskSuccessFlag)s,
                    %(TaskLastReferenceString)s, %(DurationSeconds)s, %(SuccessCount)s, %(FailureCount)s,
                    %(DuplicateCount)s, %(StatusDesc)s, %(RowCreatedDate)s, %(RowModifiedDate)s);
                    """
        self.raw_db_cursor.execute(sql_query, row_dict)

    def insert_ops_job(self, row_dict={}):
        sql_query = """INSERT INTO OPS_Job(
                        BatchKey,
                        JobName,
                        JobSuccessFlag,
                        StartTime,
                        RowCreatedDate
                    ) VALUES (%(BatchKey)s,%(JobName)s, %(JobSuccessFlag)s, %(StartTime)s, %(RowCreatedDate)s);
                    """
        self.raw_db_cursor.execute(sql_query, row_dict)

        # need the key just inserted
        sql_query = "SELECT LAST_INSERT_ID() AS JobKey"
        self.raw_db_cursor.execute(sql_query)
        sql_results = self.raw_db_cursor.fetchone()
        return sql_results['JobKey']

    def update_ops_job(self, row_dict={}):
        sql_query = """UPDATE OPS_Job
                       SET EndTime = %(EndTime)s,
                           JobSuccessFlag = %(JobSuccessFlag)s,
                           DurationSeconds = %(DurationSeconds)s,
                           StatusDesc = %(StatusDesc)s,
                           RowModifiedDate = %(RowModifiedDate)s
                       WHERE JobKey = %(JobKey)s;
                    """
        self.raw_db_cursor.execute(sql_query, row_dict)
        return

    def pre_processor(self):
        self.job_start_time = datetime.now()
        self.logger.info("Job %s started: %s" % (self.job_name, self.job_start_time))
        row_dict = {'BatchKey': self.batch_key,
                    'JobName': self.job_name,
                    'JobSuccessFlag': 0,
                    'StartTime': self.job_start_time,
                    'RowCreatedDate': datetime.now()}
        # Make an entry in OPS_Job table
        self.job_key = self.insert_ops_job(row_dict=row_dict)

    def post_processor(self, success_flag=1, status_desc=''):
        end_time = datetime.now()
        elapsed_job_time = end_time - self.job_start_time
        elapsed_job_time_seconds = ((elapsed_job_time.seconds + elapsed_job_time.days * 24 * 3600) * 10**6) / 10**6
        total_elapsed_time_sec = round(float("%s.%s" % (elapsed_job_time_seconds, elapsed_job_time.microseconds)), 4) # 4 digit precision
        row_dict = {'JobKey': self.job_key,
                    'EndTime': end_time,
                    'JobSuccessFlag': success_flag,
                    'DurationSeconds': total_elapsed_time_sec,
                    'StatusDesc': status_desc,
                    'RowModifiedDate': datetime.now()}
        # Populate OPS_Batch table with stats report
        self.update_ops_job(row_dict=row_dict)

        self.logger.info("\nJob %s completed: %s" % (self.job_name, datetime.now()))

    def start_task(self, task_cls):
        success_flag = 1
        status_desc = ''
        try:
            self.logger.info("\nTask started: %s" % datetime.now())
            self.stats_obj = self.stats_tuple(0, 0, 0, datetime.now(), '', '')
            task_obj = task_cls(config=self.config, logger=self.logger, raw_conn=self.raw_conn,
                                raw_db_cursor=self.raw_db_cursor, array_size=self.array_size,
                                stats_tuple=self.stats_tuple, last_batch_key=self.last_batch_key,
                                last_batch_success_flag=self.last_batch_success_flag)
            task_obj.init_db_sessions()
            self.stats_obj = task_obj.start_loading()
            self.logger.info("Task completed: %s" % datetime.now())
        except Exception, e:
            self.logger.fatal("Loader Instance Fatal Crash\n %s" % e)
            self.logger.error(traceback.format_exc())

        self.stats(success_flag, status_desc)
        return success_flag, status_desc

