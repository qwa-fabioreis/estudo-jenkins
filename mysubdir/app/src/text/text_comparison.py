from ..text.utils import contains
import logging
from ..config.config import Config


logger = logging.getLogger()

def compare_blocks(blocks, doc_rows, section_name: str):

    if Config.is_debug():
        log_texto = open(f'{Config.debug_folder()}_{section_name}_comparativo.txt', 'w')
    
    logger.info('[compare_blocks] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    logger.info('[compare_blocks] start')
    
    if Config.is_debug():
        log_texto.write('[compare_blocks] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@' + '\n')
        log_texto.write('[compare_blocks] start' + '\n')    


    x_offset, y_offset = 5,5
    word_boxes = []

    for doc_row in doc_rows:
        for paragraph in doc_row.texts:
            for text_content in paragraph.text_contents:

                content = text_content.text.strip(' ').replace(',', '').replace('.', '').replace('\n','').upper()
                
                if len(content.split(':')[0]) <= 3:
                    content = content.split(':')[-1]

                content = content.split(' ')
                content = list(filter(lambda a: a != '', content))
                
                logger.info('[compare_blocks] ==============================================')
                logger.info('comparing ==>> ' + str(content))
                logger.info('[compare_blocks] ==============================================')

                if Config.is_debug():
                    log_texto.write('[compare_blocks] ==============================================' + '\n')
                    log_texto.write('comparing ==>> ' + str(content) + '\n')
                    log_texto.write('[compare_blocks] ==============================================' + '\n')


                for block in blocks:
                    
                    logger.info('to ' + str(block['text']))
                    if Config.is_debug():
                        log_texto.write('to ' + str(block['text']) + '\n')


                    c = contains(content, block['text'])
                    
                    if text_content.found is False and c is not False:
                        
                        logger.info('\n\n' + '--- Encontrado --- >>>>>>>> ' + str(content) + ' <<<<<<<<' + '\n\n\n')
                        if Config.is_debug():
                            log_texto.write('\n\n' + '--- Encontrado --- >>>>>>>> ' + str(content) + ' <<<<<<<<' + '\n\n\n')

                        text_content.found = True
                        
                        for word_index in range(c[0], c[1]):
                            (x_, y, w, h) = (
                                block['left'][word_index] - x_offset, block['top'][word_index] - y_offset,
                                block['width'][word_index] + x_offset,
                                block['height'][word_index] + y_offset)
                            word_boxes.append((x_, y, w, h))

                        break
    
    if Config.is_debug():
        log_texto.close()

    return word_boxes

