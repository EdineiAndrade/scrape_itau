from convert_data import convert_data

from functools import reduce
import pandas as pd

import PyPDF2
import os
import re
import datetime

#função para exportar od dados
def exportar_dados(dfs):
    df_final =  pd.concat(dfs,ignore_index=True)
    df_final = convert_data(df_final)
    # Obter a data e hora atual
    now = datetime.datetime.now()
    # Formatar a data e a hora conforme desejado (exemplo: 25-03-2025_14-35-20)
    data_hora_formatada = now.strftime('%d-%m-%Y_%H-%M-%S')
    nome_arquivo_pdf = os.path.join("C:\\scrape_itau","relatorio_excel", f"Lista_clientes_{data_hora_formatada}.xlsx")
    df_final.to_excel(nome_arquivo_pdf, index=False)
# Função para extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)  # Usando PdfReader em vez de PdfFileReader
        texto = ''
        for pagina in leitor.pages:  # Iterar sobre as páginas do PDF
            texto += pagina.extract_text()

        texto_limpo = texto.replace('\xa0', ' ')
        inf_3 = texto_limpo.split("avançados")
        texto_3 = inf_3[1]
        texto_4 = texto_3.split('Primeira')
        texto_5 = texto_4[0]
        texto_final = texto_5[1:-1]
    return texto_final

# Função para processar o texto e criar o DataFrame
def processar_texto_para_df(texto,arquivo):
    linhas = texto.split('\n')
    linhas = linhas[1:]
    # Função lambda que une elementos sem dígitos com o próximo
    unir = lambda lst: reduce(
        lambda acc, x: acc[:-1] + [acc[-1] + " " + x] if re.search(r'\d', acc[-1]) is None else acc + [x],
        lst[1:],
        [lst[0]]
    )
    linhas_ajustadas = unir(linhas)
    dados = []
    for linha in linhas_ajustadas:      
        # Expressão regular para extrair os dados
        # Regex para cada campo
        regex_nome = r'^(.*?)(?=\s*\d)' # Nome completo (tudo até o primeiro número)                      
        regex_contrato = r'\d+'  # Contrato (sequência de dígitos)
        regex_situacao = r'(em dia|em atraso)'  # Situação (em dia ou em atraso)
        regex_valor_contratado = r'R\$\s*([\d.,]+)'  # Valor contratado (R$ seguido de número)
        regex_saldo_devedor = r'R\$\s*([\d.,]+,\d{2})'  # Saldo devedor (R$ seguido de número)
        regex_parcelas = r'(\d+\s+de\s+\d{1,2})'  # Parcelas (X de Y)
        #regex_parcelas = r'(\d+\s+de\s+\d{2})'  # Parcelas (X de Y)
        regex_prox_venc = r'(\d{2}\s+\w{3}\s+\d{4})'  # Próximo vencimento (DD MMM AAAA)
        regex_valor_parcela = r'R\$\s*([\d.,]+,\d{2})'  # Valor da parcela (R$ seguido de número)
        regex_atraso = r'(\d+\s+dias)$'  # Atraso (número seguido de "dias")

        # Função para extrair um campo usando regex
        def extrair_campo(regex, texto):
            match = re.search(regex, texto)
            if match:
                return match.group(1) if len(match.groups()) > 0 else match.group(0)
            return None

        # Extrair cada campo
        nome_completo = extrair_campo(regex_nome, linha)
        linha = linha.replace(nome_completo, '', 1).strip()  # Remove o nome da linha

        contrato = extrair_campo(regex_contrato, linha)
        linha = linha.replace(contrato, '', 1).strip()  # Remove o contrato da linha

        situacao = extrair_campo(regex_situacao, linha)
        linha = linha.replace(situacao, '', 1).strip()  # Remove a situação da linha

        valor_contratado = extrair_campo(regex_valor_contratado, linha)
        linha = linha.replace(f'R$ {valor_contratado}', '', 1).strip()  # Remove o valor contratado da linha

        saldo_devedor = extrair_campo(regex_saldo_devedor, linha)
        linha = linha.replace(f'R$ {saldo_devedor}', '', 1).strip()  # Remove o saldo devedor da linha

        parcelas = extrair_campo(regex_parcelas, linha)
        linha = linha.replace(parcelas, '', 1).strip()  # Remove as parcelas da linha

        prox_venc = extrair_campo(regex_prox_venc, linha)
        linha = linha.replace(prox_venc, '', 1).strip()  # Remove o próximo vencimento da linha

        valor_parcela = extrair_campo(regex_valor_parcela, linha)
        linha = linha.replace(f'R$ {valor_parcela}', '', 1).strip()  # Remove o valor da parcela da linha

        atraso = extrair_campo(regex_atraso, linha)

         # Adicionar os dados à lista
        dados.append({
            "Nome Completo": nome_completo,
            "Contrato": contrato,
            "Situação": situacao,
            "Valor Contratado": valor_contratado,
            "Saldo Devedor": saldo_devedor,
            "Parcelas": parcelas,
            "Próximo Vencimento": prox_venc,
            "Valor Parcela": valor_parcela,
            "Atraso": atraso,
            "Caminho Arquivo:": arquivo
        })    
    
    return dados

def ler_pdf():

    caminho_pasta = 'C:\scrape_itau\paginas_pdf'
    arquivos = os.listdir(caminho_pasta)
    dfs = []
    for arquivo in arquivos:
        # Caminho do arquivo PDF
        caminho_pdf = f'{caminho_pasta}\\{arquivo}'

        # Extrair texto do PDF
        texto = extrair_texto_pdf(caminho_pdf)


        # Processar texto e criar DataFrame
        df = processar_texto_para_df(texto, arquivo)
        df = pd.DataFrame(df)
        print(f"Extraindo informações do arquivo | {arquivo}")
        dfs.append(df)
    return dfs
# Exibir o DataFrame
if __name__ == "__main__":
    dfs = ler_pdf()
    exportar_dados(dfs)
    print("fim da execução")