import logging

logger = logging.getLogger()
# Exemplo da estrutura que sera criada
'''
[
  {
    "secao": "LATERAL ESQUERDA",
    "linhas": [
      {
        "paragrafo": [
          {
            "palavra": "PREMIERPET"
          },
          {
            "palavra": "-"
          }
        ]
      }
    ]
  }
]
'''
croqui_json = []


def criar_nova_estrutura_exportacao_croqui(croqui):

    logger.info('[exportacao_croqui] iniciando a construcao da estrutura de exportacao do croqui.')
    
    for nome_secao in croqui.d_sections:
        
        # Criacao do objeto que corresponde a uma secao que sera adiciona ao final
        secao_json = {
            "secao": nome_secao,
            "linhas": []
        }

        for row in croqui.d_sections[nome_secao].rows:
            
            linhas = []

            # Tratamento para todos os textos do croqui
            for paragraph in row.texts:
                
                lista_palavras = []

                for text_content in paragraph.text_contents:
                   
                    content = text_content.text.strip(' ').replace('\n','').upper().split(' ')
                    # content = content.split(' ')
                    content = list(filter(lambda a: a != '', content))

                    for palavra in content:
                              
                        lista_palavras.append({
                            "palavra": palavra,
                        })
                
                linhas.append({"paragrafo": lista_palavras})


            # Tratamento para as tabelas
            if nome_secao == "PAINEL VERSO CENTRAL" and len(row.tables) > 0:

              # Mudando o nome para reaproveitar essa variavei e nao ter problema com index
              tabela = row.tables[0]

              # TRATAMENTO PARA A TABELA NIVEIS DE GARANTIA
              if tabela.rows[0][0].text.upper() == "NÍVEIS DE GARANTIA":
      
                colunas = tratamento_tabela_niveis_garantia(tabela)        
                for coluna in colunas: 
                  linhas.append({'paragrafo': coluna})
                
  
              # TRATAMENTO PARA A TABELA GUIA ALIMENTAR
              elif row.texts[0].text_contents[0].text.replace('\n', '').upper() == "GUIA ALIMENTAR":
                
                linha1_tratar, linha2, linha3 = tratamento_tabela_guia_alimentar(tabela)

                # Caso especial da linha 1
                for linha in linha1_tratar: linhas.append({"paragrafo": linha})
                linhas.append({"paragrafo": linha2})
                linhas.append({"paragrafo": linha3})


              # TRATAMENTO PARA A TABELA RECOMENDACAO DIARIA DE CONSUMO
              elif row.texts[0].text_contents[0].text.replace('\n', '').upper() == "MODO DE USAR":

                # Poder haver casos onde havera duas ou mais tabelas, entao passa-se o atributo tables
                linhas_tabela = tratamento_tabela_recomendacao_diaria_de_consumo(row.tables)
                for linha in linhas_tabela: linhas.append({'paragrafo': linha})



            # Acrescentando a estrutura criada na seção
            for linha in linhas:
               secao_json['linhas'].append(linha)


        # Adiciona toda a estrutura criada 
        croqui_json.append(secao_json)

    # Retorna toda a estrutura criada
    logger.info('[exportacao_croqui] finalizada a estrutura de exportacao do croqui.')
    return croqui_json




def tratamento_tabela_niveis_garantia(tabela):
  
  logger.info('[exportacao_croqui] processando tabela NIVEIS GARANTIA :)')

  coluna1_todas_palavras = []
  linhas = []
  # coluna2_todas_palavras = []
  # coluna3_todas_palavras = []

  for linhaTabela in tabela.rows:
    
    # Ignorar a Titulo
    if not linhaTabela[0].text.upper() == "NÍVEIS DE GARANTIA":
      
      coluna1 = linhaTabela[0].text + " " + linhaTabela[1].text + " " + linhaTabela[2].text + " " + linhaTabela[3].text + " " + linhaTabela[4].text 
      coluna1_tratada = coluna1.strip(' ').replace('\n','').upper().split(' ')
      palavras_linha = []
      for palavra in coluna1_tratada: 
        palavras_linha.append({'palavra': palavra})
        # coluna1_todas_palavras.append(palavra)
      linhas.append(palavras_linha)
      # Tratamento para o caso da tabela ter 6 colunas, onde a coluna 4 tem apenas % repetidos em todas as linhas
      # coluna2 = linhaTabela[2].text + linhaTabela[3].text if len(linhaTabela) == 6 else linhaTabela[2].text
      # coluna2_tratada = coluna2.strip(' ').replace(',', '').replace('.', '').replace('\n','').upper().split(' ')
      # for palavra in coluna2_tratada: coluna2_todas_palavras.append(palavra)


      # O Tratamento caso houver, ira influenciar aqui tambem
      # coluna3 = linhaTabela[4].text + " " + linhaTabela[5].text if len(linhaTabela) == 6 else linhaTabela[3].text + " " + linhaTabela[4].text
      # coluna3_tradada = coluna3.strip(' ').replace(',', '').replace('.', '').replace('\n','').upper().split(' ')
      # for palavra in coluna3_tradada: coluna3_todas_palavras.append(palavra)

      #print(coluna1 + "\t" + coluna2 + "\t" + coluna3)


  # coluna1_exportacao = []
  # coluna2_exportacao = []
  # coluna3_exportacao = []

  # Retirar espacos em branco, mas antes de colocar na estrutura final
  # coluna1_todas_palavras = filter(lambda palavra: len(palavra) > 0, coluna1_todas_palavras)
  # coluna2_todas_palavras = filter(lambda palavra: len(palavra) > 0, coluna2_todas_palavras)
  # coluna3_todas_palavras = filter(lambda palavra: len(palavra) > 0, coluna3_todas_palavras)

  # for palavra in coluna1_todas_palavras: coluna1_exportacao.append({'palavra': palavra})
  # for palavra in coluna2_todas_palavras: coluna2_exportacao.append({'palavra': palavra})
  # for palavra in coluna3_todas_palavras: coluna3_exportacao.append({'palavra': palavra})

  # Exporta uma matriz com as 3 colunas para serem adicionadas na linha de exportacao
  return linhas
  # return [coluna1_exportacao, coluna2_exportacao, coluna3_exportacao]



def tratamento_tabela_guia_alimentar(tabela):
  
  logger.info('[exportacao_croqui] processando tabela GUIA ALIMENTAR')

  linha1_todas_palavras: list[str] = []
  linha2_todas_palavras: list[str] = []
  linha3_todas_palavras: list[str] = []

  # Para esta primeira linha, sera feito um tratamento como se cada celula fosse uma frase, para nao quebrar
  # o comparador devido a repeticao da palavra DIA em todas as celulas
  for celula in tabela.rows[0]: linha1_todas_palavras.append(celula.text)
  
  for celula in tabela.rows[1]:
    for palavra in celula.text.split(): linha2_todas_palavras.append(palavra)

  for celula in tabela.rows[2]:
    for palavra in celula.text.split(): linha3_todas_palavras.append(palavra)

  #Limpeza das linhas e UPPER para os textos
  linha1 = []
  linha2 = []
  linha3 = []

  for palavra in linha1_todas_palavras: linha1.append(palavra.strip().upper())
  for palavra in linha2_todas_palavras: linha2.append(palavra.strip().upper())
  for palavra in linha3_todas_palavras: linha3.append(palavra.strip().upper())

  # Retirar linha em branco e splitar as palavras por espaço
  linha1_corrigida = [palavra for palavra in linha1 if len(palavra) > 0]
  linha1 = linha1_corrigida

  linha1_exportacao = []
  linha2_exportacao = []
  linha3_exportacao = []

  # Cria a estrutura para inclusao no JSON
  
  # Tratamento especial para a linha 1
  for palavra in linha1: linha1_exportacao.append(palavra.split())
  
  for palavra in linha2: linha2_exportacao.append({'palavra': palavra})
  for palavra in linha3: linha3_exportacao.append({'palavra': palavra})

  linha1_exportacao_corrigida = []
  
  # Trtamento Especial para a linha 1
  for item in linha1_exportacao:

    lista_palavras_linha1 = []
    
    for palavra in item:
      lista_palavras_linha1.append({'palavra': palavra})

    linha1_exportacao_corrigida.append(lista_palavras_linha1)


  return [linha1_exportacao_corrigida, linha2_exportacao, linha3_exportacao]



def tratamento_tabela_recomendacao_diaria_de_consumo(tabelas):

  logger.info('[exportacao_croqui] processando tabela(s) RECOMENDACAO DIARIA DE CONSUMO')

  tabela_textos: list[list[str]] = []

  for tabela in tabelas:
    
    textos = []
    
    for linha in tabela.rows:
      for celula in linha:
        
        if celula.text not in textos: 
          textos.append(celula.text)

    textos = [texto_corrigir.upper().split() for texto_corrigir in textos]
    tabela_textos.append(textos)

  
  linhas_exportar = []

  # Criacao da estrutura para a exportacao juntamente com o resto do croqui
  for tabela in tabela_textos:
    for linha in tabela:
      
      linhas_tabela_convertida = []
      for palavra in linha: linhas_tabela_convertida.append({'palavra': palavra})

      linhas_exportar.append(linhas_tabela_convertida)

  return linhas_exportar
