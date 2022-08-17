import time
import jsonpickle
import logging
from io import BytesIO
from celery import group

from app.src.logger.image_logger import ImageLogger

from ..worker.config import celery
from ..config.config import Config

from ..doc.parser import Croqui
from ..doc.writer import write_document

from ..pdf.parser import get_pdf_image

from ..image.block_finder import identify_text_areas
from ..image.text_binarization import image_to_black_white

from ..table.table_finder import detect_table
from ..table.table_comparison import compare_tables

from ..text.text_comparison import compare_blocks
from ..text.text_extraction import extract_text_from_blocks, extract_boxes_from_blocks

from ..image.helper import decide_zoom_factor, resize


logger = logging.getLogger()

def extract_compare(crop: str, pdf_bytes, doc_bytes, input_directory: str):

    d_imgs = get_pdf_image(BytesIO(pdf_bytes), crop)
    croqui = Croqui(BytesIO(doc_bytes))

    for section in d_imgs:
        logger.info(section)
        d_imgs[section] = adjust_img_size(d_imgs[section])

    logger.info('Begin comparison')
    start_time = time.time()

    if Config.is_celery_on():
        results = group(process_task.s(section_name, jsonpickle.encode(d_imgs[section_name]))
                        for section_name in d_imgs)().get()
    else:
        results = [process(section_name, jsonpickle.encode(d_imgs[section_name]))
                   for section_name in d_imgs]
    
    logger.info("processamento --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    for result in results:

        section_name, texts, tables, boxes = jsonpickle.decode(result)

        if section_name in croqui.d_sections and croqui.d_sections[section_name] is not None:
            
            logger.info(f'#################################################################')
            logger.info(f'[INICIANDO COMPARACAO] ==> [{str(section_name).upper()}]')
            
            word_blocks = compare_blocks(texts, croqui.d_sections[section_name].rows, section_name)

            logger.info(f'#################################################################')

            treated_img = image_to_black_white(d_imgs[section_name])
            table_blocks = compare_tables(tables, croqui.d_sections[section_name],
                                          treated_img, boxes)

            logger.info(f'[highlight - extract_compare] - Highlighting {section_name}')
            d_imgs[section_name] = highlight(d_imgs[section_name], word_blocks + table_blocks)

        else:
            logger.info('Secao nao encontrada: ' + section_name)
    
    write_document(crop, croqui, d_imgs, input_directory)
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    logger.info('End comparison')


def adjust_img_size(image):
    black_white = image_to_black_white(image)
    zoom = decide_zoom_factor(black_white)
    image = resize(image, zoom)
    return image


@celery.task(bind=True, serializer='json')
def process_task(task, section_name, image):
    return process(section_name, image)


def process(section_name, image):
    start_time = time.time()
    
    logger.info(section_name)
    
    image = jsonpickle.decode(image)
    
    treated_img = image_to_black_white(image)
    ImageLogger.log_image(f'treated_img_{section_name}.png', treated_img)

    text_areas = identify_text_areas(treated_img)

    texts = extract_text_from_blocks(treated_img, text_areas)
    
    # Lista com todos os textos encontrado pelo Tesseract
    if Config.is_debug():
        with open(f'{Config.debug_folder()}_{section_name}_texts.txt', 'w') as _:
                _.write(str(texts))


    tables = []
    boxes = []

    # if section_name == 'PAINEL VERSO CENTRAL':
    #     logger.info('process table')

    #     tables = detect_table(image)
    #     boxes = extract_boxes_from_blocks(treated_img, text_areas)
    # logger.info("--- %s seconds ---" % (time.time() - start_time))

    return jsonpickle.encode([section_name, texts, tables, boxes])
