__author__ = 'shilavantarp'

import logging
import traceback
from datetime import datetime, timedelta
import MySQLdb

from loader_job import LoaderJob

JOB_NAME = "RAW"


class TaskLoader(object):

    def __init__(self, **kwargs):
        self.config = kwargs['config']
        self.logger = kwargs['logger']
        self.log = self.logger.log
        self.raw_conn = kwargs['raw_conn']
        self.raw_db_cursor = kwargs['raw_db_cursor']
        self.array_size = kwargs['array_size']
        self.stats_tuple = kwargs['stats_tuple']
        self.last_batch_key = kwargs['last_batch_key']
        self.last_batch_success_flag = kwargs['last_batch_success_flag']
        self.cutoff_time = self.get_cutoff_time()

    def init_db_sessions(self):
        src_dbname = self.get_source_dbname()
        self.src_conn, self.src_db_cursor = eXTVLoaderJob.get_db_cursor(self.config, 'extv_source_db',
                                                                        src_dbname=src_dbname)

    def get_source_dbname(self):
        return None

    def get_source_tblname(self):
        return None

    def get_target_tblname(self):
        raise NotImplementedError

    def get_select_query(self):
        return None

    def get_select_query_dict(self):
        return {}

    def get_insert_sqlquery(self):
        raise NotImplementedError

    def get_last_reference_query(self, last_reference_field):
        self.select_query = "SELECT * FROM %s WHERE '%s' < `date` AND `date` <= '%s';" % \
            (self.src_tblname, last_reference_field, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def start_loading(self):
        """
        - Truncate target table before load
        - Load the data from source table to target table
        """
        self.start_time = datetime.now()
        self.get_target_tblname()
        self.logger.info("Task: %s" % self.target_tblname)
        self.src_tblname = self.get_source_tblname()
        self.last_reference_field = self.get_last_reference_field()
        self.select_query = self.get_select_query()
        last_reference_field = self.load_data()
        return self.stats_tuple(self.success_count, self.fail_count, 0, self.start_time, self.target_tblname,
                                last_reference_field)

    def truncate_target_table(self):
        try:
            sql_query = "TRUNCATE TABLE %s;" % self.target_tblname
            self.logger.info(sql_query)
            self.raw_db_cursor.execute(sql_query)
        except MySQLdb.Error, e:
            self.log(logging.ERROR, 'Error in truncating table %s: %s' % (self.target_tblname, str(e)))
            raise

    def load_data(self):
        self.logger.info("Source table: %s" % self.src_tblname)
        self.truncate_target_table()
        if not self.select_query:
            # Default SELECT query fetching all rows (no condition)
            self.select_query = "SELECT * FROM %s;" % self.src_tblname
        # SELECT * is used since the table columns are not known
        if self.last_batch_key:
            # Get last reference field from OPS_Task table to pull incremental data
            if self.last_reference_field:
                self.get_last_reference_query(self.last_reference_field)

        self.success_count = 0
        self.fail_count = 0
        self.src_db_cursor.execute(self.select_query, self.get_select_query_dict())
        no_rows = 0
        latest_reference_field = None
        for rows in ResultIter(self.src_db_cursor, array_size=self.array_size, fetch_all_rows=True):
            no_rows += 1
            count = self.insert_row(rows)
            if count:
                self.success_count += count
            else:
                self.fail_count += (len(rows) - count)
        if no_rows:
            # If rows inserted, use last_reference_field of recently inserted rows
            latest_reference_field = self.get_latest_reference_field()
        else:
            # If no rows inserted, use last_reference_field of previous row to avoid making the column as NULL
            latest_reference_field = self.last_reference_field
        return latest_reference_field

    def get_last_reference_field(self):
        """
        Get OPS_Task.TaskLastReferenceString
        """
        if not self.last_batch_key:
            return None
        last_reference_field = None
        sql_query = """SELECT TaskLastReferenceString FROM OPS_Task ot
                        JOIN OPS_Job oj ON oj.JobKey = ot.JobKey
                        JOIN OPS_Batch ob ON ob.BatchKey = oj.BatchKey
                        WHERE ot.TableName = '%s' AND
                              ot.TaskLastReferenceString IS NOT NULL AND
                              ob.BatchKey = %s;""" % (self.target_tblname, self.last_batch_key)
        self.raw_db_cursor.execute(sql_query)
        res = self.raw_db_cursor.fetchone()
        if res:
            last_reference_field = res['TaskLastReferenceString']
        return last_reference_field

    def get_latest_reference_field(self):
        """
        Get last reference field from target table and update OPS_Task.TaskLastReferenceString
        """
        return None

    def filter_row_data(self, row):
        """
        Apply filter validations to source row data so that the data can be loaded into target table successfully
        """
        return row

    def insert_row(self, rows):
        rows = self.filter_row_data(rows)
        row_count = 0
        try:
            row_count = self.raw_db_cursor.executemany(self.get_insert_sqlquery(), rows)
        except MySQLdb.Error, e:
            self.log(logging.ERROR, 'Error in inserting a row into a table %s: %s' % (self.target_tblname, str(traceback.format_exc())))
            raise
        return row_count


class Task1(TaskLoader):

    def __init__(self, **kwargs):
        TaskLoader.__init__(self, **kwargs)

    def get_source_dbname(self):
        return "Source DB Name"

    def get_source_tblname(self):
        return "Source Table Name"

    def get_target_tblname(self):
        return "Target Table Name"

    def get_insert_sqlquery(self):
        sql_query = "INSERT QUERY"
        return sql_query

    def filter_row_data(self, row):
        """
        Apply filter validations to source row data so that the data can be loaded into target table successfully
        """
        # No filters
        return row


def raw_job(batch_name, batch_key, last_batch_key, last_batch_success_flag, task_name=None, config_filename=None,
            raw_conn=None, raw_db_cursor=None):
    if task_name:
        cls_list = [task_name]
    success_flag = 1
    status_desc = ''
    obj = LoaderJob(batch_name, JOB_NAME, batch_key=batch_key, last_batch_key=last_batch_key,
                        last_batch_success_flag=last_batch_success_flag,
                        config_filename=config_filename, raw_conn=raw_conn, raw_db_cursor=raw_db_cursor)
    for each_cls in cls_list:
        task_cls = globals()[each_cls]
        success, desc = obj.start_task(task_cls)
        if not success:
            success_flag = success
            status_desc = desc
    obj.post_processor(success_flag, status_desc)
    return success_flag, status_desc


if __name__ == '__main__':
    obj = LoaderProcess()
    job = "%s:raw_job" % __name__
    obj.process(job)


