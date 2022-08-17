import os
import sys
import logging
import traceback

from app.src.api.process import start_process
from app.src.config.config import Config
from app.src.file.file_utils import FileUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

try:
    input_directory: str = sys.argv[1]
    start_process(input_directory)
except Exception:
    print(traceback.print_exc())
    list_directories = os.listdir(Config.in_progress_folder())

    if(input_directory in list_directories):
        FileUtils.redirect_error_output_to_file(Config.in_progress_folder(),
                            input_directory, Config.to_failure_folder())
    else:
        FileUtils.redirect_error_output_to_file(Config.to_process_folder(),
                             input_directory, Config.to_failure_folder())
