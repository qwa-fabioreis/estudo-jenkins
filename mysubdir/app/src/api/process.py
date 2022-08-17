import os

from app.src.config.config import Config
from app.src.file.file_utils import FileUtils

from app.src.service.image_process import extract_compare
from app.src.migracao.migracao import novo_extract_compare

def start_process(input_directory):
    join_paths = os.scandir(os.path.join(Config.to_process_folder(), input_directory))

    for file in join_paths:
        crop_name = file.name
        address = file.path

    for file in os.scandir(address):
        if file.name.endswith(".pdf"):
            pdf_file = file
        elif file.name.endswith(".docx"):
            doc_file = file

    pdf_bytes:bytes = FileUtils.file_to_bytes(pdf_file) 
    doc_bytes:bytes = FileUtils.file_to_bytes(doc_file)

    source = Config.to_process_folder() + input_directory
    FileUtils.move_directory(source, Config.in_progress_folder())

    novo_extract_compare(crop_name, pdf_bytes, doc_bytes, input_directory)