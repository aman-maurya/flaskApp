import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config.errors import UnKnownError
from utils.common import CommonUtils


class LoggerUtils:

    @staticmethod
    def setup_logger(name, log_file, formatter, level=logging.DEBUG):
        my_file = Path(log_file)

        if my_file.is_file():
            # print(logging.getLogger(name).hasHandlers())
            # if logging.getLogger(name).hasHandlers():
            if len(logging.getLogger(name).handlers) > 0:
                return logging.getLogger(name)
            else:
                handler = RotatingFileHandler(log_file, maxBytes=5000000,
                                              backupCount=3, mode='a')
                handler.setFormatter(formatter)
                logger = logging.getLogger(name)
                logger.setLevel(level)
                logger.addHandler(handler)
                logger.propagate = False
                return logger
        else:
            handler = RotatingFileHandler(log_file, maxBytes=5000000,
                                          backupCount=3, mode='a')
            handler.setFormatter(formatter)
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)
            logger.propagate = False
            return logger

    @classmethod
    def error(cls, exc):
        import traceback
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        file_path = ex_traceback.tb_frame.f_code.co_filename
        tb = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        _log_message = f"{ex_value}\n{''.join(tb)}"
        d = {
            'file_name': os.path.relpath(file_path, CommonUtils.project_root_dir()),
            'line_no': ex_traceback.tb_lineno
        }
        formatter = logging.Formatter('%(asctime)s - [%(file_name)s:%(line_no)d] - %(message)s', '%m-%d-%Y %H:%M:%S')
        _log = cls.setup_logger('error', 'logs/error.log', formatter)
        _log.error(_log_message, extra=d)
        raise UnKnownError

    @classmethod
    def query_logger(cls, bind_info, statement, duration):
        if CommonUtils.is_development_env() or CommonUtils.is_testing_env():
            bind_info = bind_info if bind_info else 'master'
            _log_message = f"({bind_info})\n{statement}\nDuration: {duration}\n"
            formatter = logging.Formatter('%(asctime)s - %(message)s', '%m-%d-%Y %H:%M:%S')
            _log = cls.setup_logger('query_logger', 'logs/query.log', formatter)
            _log.debug(_log_message)

