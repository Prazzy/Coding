__author__ = 'shilavantarp'

"""
Process Flow:
-------------
- Start/Reload
    - Create new batch
    - Start RAW Job:
        If failed: Update batch record with success = 0 and Stop
        If success: Go-to DIM Job
    - Start DIM Job:
        If failed: Update batch record with success = 0 and Stop
        If success: Go-to FACT Job
    - Start FACT Job:
        If failed: Update batch record with success = 0 and Stop
        If success: Update batch record with success = 1 and Stop

"""

import sys
from optparse import OptionParser

from loader_job import (LoaderBatch, create_ops_batch, update_ops_batch, get_last_batch_details)

BATCH_NAME = 'eXTV'
CONFIG_FILENAME = 'config.ini'


class LoaderProcess(object):

    def __init__(self, batch_name, job_name=None, task_name=None, config_filename=None):
        self.batch_name = batch_name
        self.job_name = job_name
        self.task_name = task_name
        self.config_filename = config_filename
        self.config = eXTVLoaderBatch.get_config(config_filename)
        if self.job_name:
            self.jobs = self.config.get('main', self.job_name)
        else:
            self.jobs = self.config.get('main', 'jobs')
        self.raw_conn, self.raw_db_cursor = LoaderBatch.get_db_cursor(self.config, 'raw_db')
        # Previous batch details
        self.last_batch_key, self.last_batch_success_flag = get_last_batch_details(batch_name, self.raw_db_cursor)

        # Create new batch
        self.batch_key, self.batch_start_time = create_ops_batch(batch_name, self.raw_db_cursor)

    def process(self, jobs=None):
        if jobs:
            self.jobs = jobs
        jobs = self.jobs.split(" ")
        for each_job in jobs:
            module_name, job_name = each_job.split(":")
            module_name = __import__(module_name)
            job_name = getattr(module_name, job_name)
            if not self.run_job(job_name):
                return

        self.update_batch()

    def run_job(self, job):
        self.success_flag, self.status_desc = job(batch_name=self.batch_name,
                                                  batch_key=self.batch_key,
                                                  last_batch_key=self.last_batch_key,
                                                  last_batch_success_flag=self.last_batch_success_flag,
                                                  task_name=self.task_name,
                                                  config_filename=self.config_filename,
                                                  raw_conn=self.raw_conn,
                                                  raw_db_cursor=self.raw_db_cursor)
        # If failure, stop the process
        if not self.success_flag:
            # Update batch row
            update_ops_batch(self.raw_db_cursor, self.batch_start_time, self.success_flag,
                             self.status_desc, self.batch_key)
            return False
        return True

    def update_batch(self):
        # Update batch
        update_ops_batch(self.raw_db_cursor, self.batch_start_time, self.success_flag, self.status_desc, self.batch_key)

if __name__ == "__main__":
    args = sys.argv
    usage = """
             \n./loader_process.py -j <job_name>
             \n./loader_process.py -j <job_name> -t <raw_table_name>
    """
    option_parser = OptionParser(usage=usage)
    option_parser.add_option('-j', '--job_name', help='Run specified job')
    option_parser.add_option('-t', '--task_name', help='Run specified task of a job')
    (options, arguments) = option_parser.parse_args(sys.argv)
    obj = eXTVProcess(batch_name=BATCH_NAME, job_name=options.job_name, task_name=options.task_name,
                      config_filename=CONFIG_FILENAME)
    obj.process()