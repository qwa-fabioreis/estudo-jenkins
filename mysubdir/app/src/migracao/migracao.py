import logging
import jsonpickle
import cv2
from io import BytesIO

from ..config.config import Config

from ..pdf.parser import get_pdf_image
from ..doc.parser import Croqui
from ..service.image_process import process

from ..migracao.exportacao_croqui import criar_nova_estrutura_exportacao_croqui
from ..migracao.exportacao_tesseract import nova_estrutura_exportcao_tesseract_por_secao
from .serealizacao import serializar_para_json
from .serealizacao import criar_arquivo_json


logger = logging.getLogger()


def novo_extract_compare(crop: str, pdf_bytes: bytes, doc_bytes: bytes, input_directory: str):
    
    logger.info("==================================================")
    logger.info("PROCESSO DE MIGRACAO DE ESTRUTURAS")
    logger.info("==================================================")
    logger.info('[migracao] INICIANDO PROCESSAMENTO...')

    d_imgs = get_pdf_image(BytesIO(pdf_bytes), crop)
    croqui = Croqui(BytesIO(doc_bytes))

    
    # Criacao da nova estrutura de exportcao para o Croqui
    croqui_dicionario_exportacao = criar_nova_estrutura_exportacao_croqui(croqui)
    
    # Processar os recortes
    resultados = []
    for section_name in d_imgs:
        resultados.append(process(section_name, jsonpickle.encode(d_imgs[section_name])) )


    # Criacao da nova estutura de exportacao para o Tesseract
    lista_novas_estruturas_exportacao_tesseract_por_secao = []

    for resultado in resultados:
        section_name, texts, tables, boxes = jsonpickle.decode(resultado)

        # Cria a nova estrutura do tesseract por secao
        nova_estrutura_tesseract_secao = nova_estrutura_exportcao_tesseract_por_secao(section_name, texts)

        lista_novas_estruturas_exportacao_tesseract_por_secao.append(nova_estrutura_tesseract_secao)
    

    logger.info('[migracao] iniciando processo de serealizacao do croqui e tesseract')
    croqui_parseado_minificado = serializar_para_json(croqui_dicionario_exportacao, minification=True)
    tesseract_parseado_minificado = serializar_para_json(lista_novas_estruturas_exportacao_tesseract_por_secao, minification=True)

    nome_arquivo_croqui_min = Config.in_progress_folder() + input_directory + '/' + crop + "/croqui." + "min.json"
    nome_arquivo_tesseract_min =  Config.in_progress_folder() + input_directory + '/' + crop + "/tesseract." + "min.json"
    
    logger.info(f'[migracao] exportando o arquivo do croqui gerado para >> {nome_arquivo_croqui_min}')
    criar_arquivo_json(nome_arquivo_croqui_min, croqui_parseado_minificado)

    logger.info(f'[migracao] exportando o arquivo do tesseract gerado para >> {nome_arquivo_tesseract_min}')
    criar_arquivo_json(nome_arquivo_tesseract_min, tesseract_parseado_minificado)


    # Exportcao das imagens
    for section_name in d_imgs:
        nome_recorte_secao = Config.in_progress_folder() + input_directory + '/' + crop + "/" + section_name + ".png"
        logger.info(f'[migracao] exportando recorte da secao [{section_name}] para >> {nome_recorte_secao}')
        cv2.imwrite(nome_recorte_secao, d_imgs[section_name])



    