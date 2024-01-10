
from bs4 import BeautifulSoup
from urllib.request import urlopen
import runpy
import re
import pandas as pd
from datetime import  datetime, date
from urllib.error import URLError, HTTPError

data_e_hora_atuais = datetime.now()
data = date.today()
hora = data_e_hora_atuais.strftime('%H:%M')

listTauste_id, listTauste_nome, lisTauste_preco, listTauste_empresa, listTauste_produto = [], [], [], [], []
def getTauste(url, produto, nome):
    try:
        htmlINT = urlopen(url) 
        bsINT = BeautifulSoup(htmlINT, 'html.parser',from_encoding="iso-8859-8")    
    except HTTPError as e:
        print('Página %s não encontrada. O nome e o Preco está indisponível.'%url)
    except URLError as e:
        print('Não conseguimos alcançar um servidor.')
    else:
        pass
    try:    
            nameTauste = bsINT.find_all('h1', {'class':'page-title'}) 
            precoTauste = bsINT.find_all('span', {'class':'price-wrapper'}, limit=1) 
    except : 
            nameTauste = None
            precoTauste = None
    pass    


    try:
        for nINT in nameTauste:
            nome_INT = (nINT.text.replace('\n', "").rstrip()).upper()
            listTauste_nome.append(nome_INT)
            listTauste_id.append(len(listTauste_nome))
            listTauste_empresa.append("TAUSTE")
            listTauste_produto.append(produto)
        for pINT in precoTauste:
            preco =  (pINT.text.replace('\n', "").rstrip()).upper()
            preco = (re.sub('[^0-9, ,]', '', preco).replace(',','.').replace(' ',''))       
            preco = float("{:.2f}".format(float(preco)))
            lisTauste_preco.append(preco)
    except: 
        nome_INT = nome
        preco= float(0.0)
    pass


getTauste("https://tauste.com.br/jundiai/arroz-oriental-inari-pacote-5000g.html", "ARROZ", "ARROZ ORIENTAL INARI")
getTauste("https://tauste.com.br/jundiai/acucar-cristal-native-organico-pacote-5000g.html", "AÇÚCAR","AÇÚCAR CRISTAL NATIVE")
getTauste("https://tauste.com.br/jundiai/acucar-uni-o-refinado-pacote-1000g.html", "AÇÚCAR","AÇÚCAR CRISTAL NATIVE")
getTauste("https://tauste.com.br/jundiai/molho-shoyu-karui-frasco-500ml.html","SHOYU","MOLHO SHOYU KARUI")
getTauste("https://tauste.com.br/jundiai/saque-azuma-mirin-culinario-pet-500ml.html","MIRIN","SAQUÊ AZUMA MIRIN")
getTauste("https://tauste.com.br/jundiai/lombo-de-salm-o-400g.html", "SALMÃO","LOMBO DE SALMÃO")
getTauste("https://tauste.com.br/jundiai/cream-cheese-scala-bisnaga-400g.html","CREAM CHEESE","CREAM CHEESE SCALA")
getTauste("https://tauste.com.br/jundiai/cream-cheese-polenghi-bisnaga-400g.html","CREAM CHEESE","CREAM CHEESE POLENGHI")
getTauste("https://tauste.com.br/jundiai/alga-marinha-kenko-pacote-c-10-27g.html", "NORI", "ALGA MARINHA KENKO PACOTE C/10")
getTauste("https://tauste.com.br/jundiai/143419-alga-marinha-karui-asakusa-yakinori-pacote-c-50-115g.html","NORI","ALGA MARINHA KARUI C/50")
getTauste("https://tauste.com.br/jundiai/tempero-oriental-hondashi-pacote-60g.html","HONDASHI","TEMPERO ORIENTAL HONDASHI")
getTauste("https://tauste.com.br/jundiai/mistura-flocada-alfa-panko-pacote-200g.html","PANKO","MISTURA FLOCADA ALFA PANKO")

try:
    dINT = {'ID': listTauste_id, 'Empresa': listTauste_empresa, 'Produto': listTauste_produto,'Nome': listTauste_nome, 'Preço': lisTauste_preco, 'Data': data, 'Hora': hora}
    dadosTauste = pd.DataFrame(data = dINT)
    print(dadosTauste)
except (NameError):
    print('Por favor, atualize o programa novamente...')
    runpy.run_path(path_name='comJap.py')
pass

writer = pd.ExcelWriter(f'src/ComparaPreco_Tauste_{data}.xlsx')
dadosTauste.to_excel(writer, sheet_name='Tauste', index=False)
writer.save()

