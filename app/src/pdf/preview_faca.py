import fitz

from io import BytesIO
from fastapi import UploadFile, File


def preview_faca_pdf(faca_pdf: UploadFile = File(...)) -> bytes:
    """
    Preview Faca PDF - v1.0

    Este metodo recebe um arquivo PDF da API, cria uma matriz de reducao
    para diminuir o tamanho dos pixels da primeira pagina do PDF, e entao multiplica
    essa matriz de reducao pelos pixels da pagina 1 do PDF, gerando assim uma imagem da
    primeira pagina em tamanho reduzido e retorna os bytes da imagem reduzida

    @param faca_pdf: Upload File
    @return: imageCompressed: bytes
    """

    # Converte o arquivo pdf de entrada para bytes
    pdf_bytes = BytesIO(faca_pdf.file.read())

    pdf = fitz.Document(stream=pdf_bytes, filename='pdf')

    '''
    Ao criar a matriz de zooom, o fitz ira multiplicar
    os coeficientes abaixo pela quantidade de pixels em X e em Y
    e no caso abaixo, ira gerar uma imagem com a 20% dos pixels
    em ambos os eixos, mas mantendo a mesma proporcao.
    Como resultado, irá gerar uma imagem com o tamanho em MBytes menor
    '''
    zoom_x, zoom_y = 0.2, 0.2
    matriz = fitz.Matrix(zoom_x, zoom_y)

    # Aplicacao da matriz de zoom na pagina 1 do PDF
    pixels = pdf[0].get_pixmap(matrix=matriz)

    # Retornar os bytes da imagem gerada
    return pixels.getImageData()
