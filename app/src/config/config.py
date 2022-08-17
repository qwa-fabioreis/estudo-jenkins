import os
import datetime
from datetime import datetime

class Config():

    def is_debug():
        return os.environ.get("DEBUG", False)

    def debug_folder():
        return os.environ.get("DEBUG_FOLDER", "/debug/")

    def is_celery_on():
        return os.environ.get('IS_CELERY_ON', False)

    def report_folder():
        return os.environ.get('REPORT_FOLDER', '/report/')

    def success_folder():
        return os.environ.get('SUCCESS_FOLDER', '/raiz/success/')

    def in_progress_folder():
        return os.environ.get('IN_PROGRESS_FOLDER', '/raiz/in_progress/')

    def to_process_folder():
        return os.environ.get('TO_PROCESS', '/raiz/to_process/')

    def to_failure_folder():
        return os.environ.get('FAILURE', '/raiz/failure/')

    def transform_dir_into_date(timestamp_as_string: str) -> str:
        timestamp_as_float = float(timestamp_as_string)
        date_and_time = datetime.fromtimestamp(timestamp_as_float)
        return date_and_time.strftime("%m_%d_%Y %H:%M:%S.%f")
