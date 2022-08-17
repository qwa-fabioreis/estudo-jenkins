import logging

logger = logging.getLogger()


def nova_estrutura_exportcao_tesseract_por_secao(nome_secao: str, texts):
    
    logger.info(f'[exportacao_tesseract] criando estrutura de exportacao do tesseract para secao {nome_secao}')

    estrutura_json = {
            'secao': nome_secao,
            'palavras': []
        }
        
    lista_palavras_dict = []
        
    for dict_tesseract in texts:
        for i in range(len(dict_tesseract['text'])):
            
            parsed_tesseract = {
                'texto': dict_tesseract['text'][i],
                'confianca': dict_tesseract['conf'][i],
                'left': dict_tesseract['left'][i],
                'top': dict_tesseract['top'][i],
                'width': dict_tesseract['width'][i],
                'height': dict_tesseract['height'][i]
            }

            # Adiciona o dicionario anterior em uma lista
            lista_palavras_dict.append(parsed_tesseract)

    # Adiciona a lista de palavras no dicionario da secao 
    estrutura_json['palavras'] = lista_palavras_dict


    return estrutura_json
