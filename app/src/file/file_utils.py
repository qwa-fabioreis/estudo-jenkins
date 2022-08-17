import datetime
import os
import shutil
import traceback

from docx.api import Document

class FileUtils():
    def concat_paths(paths: str = []):
        for str in paths:
            if not str.endswith('/'):
                str.join('/')
        return ''.join(paths)

    def move_directory(source, dest):
        return shutil.move(source, dest, copy_function = shutil.copytree)

    def file_to_bytes(file:os.DirEntry) -> bytes:
        return open(file, 'rb').read()
    
    def save_document(document: Document, path: str, name: str):
        document.save(path + name)

    def get_error_report_name(crop:str, timestamp_as_date_string:str) -> str:
        return "/failure_" + crop + "_" + timestamp_as_date_string + ".err"

    def redirect_error_output_to_file(actual_directory, input_directory, error_folder):
        source = actual_directory + input_directory
        FileUtils.move_directory(source, error_folder) 
        
        crop_name_list = os.listdir(os.path.join(error_folder, input_directory))
        crop_name = (''.join(str(a) for a in crop_name_list))
        
        path = os.path.join(error_folder, str(input_directory), str(crop_name))
        failure_file_name = FileUtils.get_error_report_name(crop_name, input_directory)
            
        with open(path + failure_file_name, "w") as error:
            log_time = datetime.datetime.now()
            error.write(log_time.strftime("%m_%d_%Y %H:%M:%S.%f"))
            error.write("\n")
            traceback.print_exc(file=error)

 