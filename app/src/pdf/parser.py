from app.src.logger.image_logger import ImageLogger
import fitz
import cv2
import numpy as np
from .extractor.extractor_factory import create_extractor


def get_pdf_image(file_path, faca):
    pdf_page = convert_to_image(file_path)
    # return extract_sections(pdf_page, faca)
    return decide_extractor(pdf_page, faca)


def convert_to_image(file_path):
    doc = fitz.open(stream=file_path, filetype='pdf')

    # Imagem da primeira pagina para o debug
    img_sem_zoom = doc[0].getPixmap() 
    img_com_tamaho_1x1 = np.asarray(bytearray(img_sem_zoom.getImageData('png')), dtype="uint8")
    ImageLogger.log_image(f'imagem_pdf_1x1.png', cv2.imdecode(img_com_tamaho_1x1, cv2.IMREAD_COLOR))

    # Aplicar um zoom de 3x na altura e largura
    zoom_x, zoom_y = 3, 3
    mat = fitz.Matrix(zoom_x, zoom_y)
    
    img_com_zoom = doc[0].getPixmap(matrix=mat)
    img_com_tamanho_3x3 = np.asarray(bytearray(img_com_zoom.getImageData('png')), dtype='uint8')

    ImageLogger.log_image(f'imagem_pdf_3x3.png', cv2.imdecode(img_com_tamanho_3x3, cv2.IMREAD_COLOR))
    return cv2.imdecode(img_com_tamanho_3x3, cv2.IMREAD_COLOR)

def decide_extractor(img, faca):
    extractor = create_extractor(img, faca)
    return extractor