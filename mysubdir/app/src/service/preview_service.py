import uuid

from fastapi import File, UploadFile, status
from fastapi.exceptions import HTTPException

from ..doc.croqui_header import croqui_header
from ..doc.croqui_image import croqui_image
from ..pdf.preview_faca import preview_faca_pdf
import logging


logger = logging.getLogger()

async def preview_docx_croqui_service(doc: UploadFile = File(...)):

    # Verifica o tipo do arquivo
    if not doc.filename.endswith('.docx'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='O arquivo inserido não corresponde a um arquivo do tipo .DOCX'
        )

    try:
        # Recebe todos os valores dos campos da primeira tabela do croqui
        fields = croqui_header(doc)

        # Reseta o ponteiro do arquivo para inicio
        # Esta operacao precisa do await para nao bugar a funcao de retirada de imagem
        await doc.seek(0)

        # Recebe os bytes da imagem encontrada no croqui
        img_bytes = croqui_image(doc)

        # Diretorio default de arquivos temporarios
        app_temp = 'static'

        # # Caso tenha uma pasta temporaria defenida na variavel de ambiente
        # if 'APP_TEMP' in os.environ.keys():
        #     app_temp = os.environ['APP_TEMP']

        # Define um nome aleatorio para a imagem
        img_name = f'{uuid.uuid4()}.png'

        # Escreve os bytes no direrotio temporario
        with open(f'./{app_temp}/{img_name}', 'wb') as imgFile:
            imgFile.write(img_bytes)

        return {
            'imagem_link': f'{app_temp}/{img_name}',
            'fields': fields
        }
    except:
        logger.error("[preview_docx_croqui_service] It wasn't possible to process file")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Não foi possivel abrir o DOCX inserido. O arquivo provavelmente está corrompido ou mal formatado.'
        )


def preview_pdf_faca_service(pdf: UploadFile = File(...)):

    # Verifica o tipo do arquivo
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='O arquivo inserido não corresponde a um arquivo do tipo .PDF'
        )

    try:
        # Passa para funcao, o PDF recebido da API e retorna os bytes da img
        img_preview_image_bytes = preview_faca_pdf(pdf)

        # Diretorio default de arquivos temporarios
        app_temp = 'static'

        # Define um nome aleatorio para a imagem
        img_name = f'{uuid.uuid4()}.png'

        # Escreve os bytes no direrotio temporario
        with open(f'./{app_temp}/{img_name}', 'wb') as imgFile:
            imgFile.write(img_preview_image_bytes)

        return {'preview_link': f'{app_temp}/{img_name}'}
        # return Response(img_preview_image_bytes, media_type='image/png')
    except:
        logger.error("[preview_pdf_faca_service] It wasn't possible to process file")        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Não foi possivel abrir o PDF inserido. O arquivo provavelmente está corrompido ou mal formatado.'
        )

