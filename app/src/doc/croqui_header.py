import docx

from io import BytesIO
from fastapi import UploadFile, File
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def croqui_header(croqui_doc: UploadFile = File(...)) -> list:
    """
    Croqui Header - v1.1

    Este metodo recebe um arquivo (.docx) que representa um croqui
    da PremierPet, e realizara a extracao de todos os dados
    da primeira tabela do arquivo, e retornara os dados em uma lista
    com valor e descricao

    @param croqui_doc: UploadFie
    @return: response: List
    """
    logger.info('[croqui_header] starting to process file')
    #Abertura do documento recebido pela API
    document = docx.Document(BytesIO(croqui_doc.file.read()))

    dados = dict()
    response = list()

    for row in document.tables[0].rows:
        for cell in row.cells:

            if ':' in str(cell.text):

                if '\n' in str(cell.text):

                    listContent = str(cell.text).split('\n')

                    # Caso existe um : apos da quebra de linha, entao eh um atributo
                    if ':' in str(listContent[1]):

                        # Percorre a lista divida pela quebra de linha e split pelos :
                        for item in listContent:
                            new = item.split(':')
                            dados[new[0].strip()] = new[1].strip()

                    # Caso nao tenha : depois do \n, eh porque o valor apenas esta na linha de baixo
                    else:
                        atributos = str(cell.text).split(':')
                        dados[atributos[0].strip()] = atributos[1].strip()

                else:
                    content = str(cell.text).split(':')
                    dados[content[0].strip()] = content[1].strip()



            elif '?' in cell.text:
                content = str(cell.text).split('?')
                dados[content[0]] = content[1].strip()

    for key in dados.keys():
        response.append({'value': key, 'description': dados[key]})

    return response
