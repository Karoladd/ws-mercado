
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import runpy
import re
import pandas as pd
from datetime import  datetime, date
from urllib.error import URLError, HTTPError

data_e_hora_atuais = datetime.now()
data = date.today()
hora = data_e_hora_atuais.strftime('%H:%M')

listCovab_id, listCovab_nome, lisCovab_preco, listCovab_empresa, listCovab_produto = [], [], [], [], []

def getCovab(url, produto, nome):
            try:
                session = HTMLSession()
                response = session.get(url)
            except requests.exceptions.RequestException as e:
                print(e)
            if response:
                    print(response.html.find('.vtex-store-components-3-x-productBrand', first=True))
                    nomeProd = response.html.find('.vtex-store-components-3-x-productBrand', first=True)
                    if nomeProd != None: nomeProd = (nomeProd.text).upper()
                    else: 
                          nomeProd = response.html.find('.vtex-store-components-3-x-productBrand ', first=True).text
                          nomeProd = nomeProd.upper()
                    print(nomeProd)
                    preco_int = response.html.find('.vtex-product-price-1-x-currencyInteger', first=True)
                    print(preco_int)
                    preco_float = response.html.find('.vtex-product-price-1-x-currencyFraction', first=True).text 
                    precProd = float(preco_int+"."+preco_float)
                    print(precProd)
            else:
                nomeProd = nome
                precProd = float(0.0)
                print("O produto", nomeProd, "está indisponível")
            listCovab_produto.append(produto)
            listCovab_nome.append(nomeProd)
            listCovab_empresa.append("COVABRA")
            listCovab_id.append(len(listCovab_nome))
            lisCovab_preco.append(precProd)



#getCovab("https://Covab.com.br/jundiai/arroz-oriental-inari-pacote-5000g.html", "ARROZ", "ARROZ ORIENTAL INARI")
getCovab("https://www.covabra.com.br/acucar-uniao-refinado-1kg/p", "AÇÚCAR","AÇÚCAR UNIAO REFINADO")
getCovab("https://www.covabra.com.br/molho-shoyu-karui-tradicional-500ml/p", "SHOYU","SHOYU KARUI 500 ML")
getCovab("https://www.covabra.com.br/molho-shoyu-karui-light-1l/p", "SHOYU","SHOYU KARUI LIGHT")

try:
    dINT = {'ID': listCovab_id, 'Empresa': listCovab_empresa, 'Produto': listCovab_produto,'Nome': listCovab_nome, 'Preço': lisCovab_preco, 'Data': data, 'Hora': hora}
    print(dINT)
    dadosCovab = pd.DataFrame(data = dINT)
    print(dadosCovab)
except (NameError):
    print('Por favor, atualize o programa novamente...')
    runpy.run_path(path_name='covabra.py')
pass

writer = pd.ExcelWriter(f'src/ComparaPreco_Covabra_{data}.xlsx')
dadosCovab.to_excel(writer, sheet_name='Covab', index=False)
writer._save()
