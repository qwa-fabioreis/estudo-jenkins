import json 
from ..config.config import Config


def serializar_para_json(dicionario: dict, minification=False, indent=2) -> str:    
    if minification:
        return json.dumps(dicionario, ensure_ascii=False)
    
    return json.dumps(dicionario, ensure_ascii=False, indent=indent)


def criar_arquivo_json(filename: str, content: str):
    with open(filename, 'w') as export_file:
        export_file.write(content)
