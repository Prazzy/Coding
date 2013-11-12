__author__ = 'shilavantarp'

import logging
import MySQLdb as mdb

def get_logger(log_file_name):
    logging.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(levelname)-6s - %(message)s - %(filename)s:%(lineno)d - %(msecs)d ms[%(asctime)s]',
                                        datefmt='%x %X %Z')
    handler = logging.handlers.RotatingFileHandler(filename=log_file_path, mode='a', maxBytes=1000000, backupCount=3)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class SingletonType(type):
    def __new__(mcls, name, bases, namespace):
        namespace.setdefault('__lock__', threading.RLock())
        namespace.setdefault('__instance__', None)
        return super(SingletonType, mcls).__new__(mcls, name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        cls.__lock__.acquire()
        try:
            #if cls.__instance__ is None:
            if getattr(cls, '__instance__', None) is None:
                instance = cls.__new__(cls, *args, **kwargs)
                instance.__init__(*args, **kwargs)
                cls.__instance__ = instance
            elif kwargs.get('section') != None and cls.__instance__.config:
                cls.__instance__.set_params(cls.__instance__.config, kwargs['section'])
        finally:
            cls.__lock__.release()
        return cls.__instance__


class Database(object):
    __metaclass__ = SingletonType

    def __init__(self, **kwargs):
        hostname = kwargs['hostname']
        userid = kwargs['userid']
        pwd = kwargs['pwd']
        dbname = kwargs['dbname']
        pass

    def _connect(self):
        self._conn = mdb.connect(hostname, userid, pwd, dbname)

    def _disconnect(self):
        if self._conn:
            self._conn.close()