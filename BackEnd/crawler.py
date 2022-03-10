# coding: utf-8
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import nltk
nltk.download('stopwords')
nltk.download('rslp')
import json
import pymongo
import db

def getText(soup):
    for tags in soup(['script', 'style']):
        tags.decompose()
    return ' '.join(soup.stripped_strings)

def breakWord(text):
    text = re.sub(r'[0-9]', '', text)
    
    stop = nltk.corpus.stopwords.words('portuguese')
    stop.extend(('http','https','têm'))
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W+')
    word_list = []
    list_split = [p for p in splitter.split(text) if p != '']
    for p in list_split:
        if stemmer.stem(p.lower()) not in stop:
            if len(p) > 1:
                word_list.append(stemmer.stem(p.lower()))
    return word_list


def indexador(url, sopa, textDiv):
    palavras = breakWord(' '.join(textDiv))
    if len(palavras)>0:
        urlWord = {
            "url":url,
            "palavra":palavras, 
            "paragrafo": textDiv
        }
        idUrlPage = db.insertUlrPage(urlWord)
        return idUrlPage
    else:
        return

def unionUrlWord(origin_url, destination_url):
    url_text = destination_url.replace('_', ' ')
    words = breakWord(url_text)
    value = {
        "url":destination_url,
        "urlTexto":words
    }
    return value

def crawl(pages, depth):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for count in range(depth):
        print("Nível: ",count,"Nº de links: ",len(pages))
        
        new_pages = set()
        for page in pages:
            # print("Próxima página ",page)
            http = urllib3.PoolManager()
            try:
                page_data = http.request('GET', page)
            except:
                print('Erro ao abrir a página ' + page)
                # 9
                continue
            
            indexada = db.paginaIndexada(page)
            
            if indexada==-2:
                continue

            # print("Faz limpeza")
            soup = BeautifulSoup(page_data.data, "lxml")
            
            #<div class="feed-post-body-resumo">
            textDiv = set()
            for foo in soup.find_all('div', attrs={'class': 'feed-post-body-resumo'}):
                textDiv.add(foo.text)
            
            for foo in soup.find_all('p'):
                textDiv.add(foo.text)
            
            idUrlWord = indexador(page, soup,list(textDiv))


            links = soup.find_all('a')
            # i = 1
            # print("Pega links ",len(links))
            links_bd=[]
            for link in links:
                if ('href' in link.attrs):
                    url = urljoin(page, str(link.get('href')))
                    # print("Próximo link",url)
                    
                    if url.find("'") != -1:
                        continue
                    url = url.split('#')[0]
                    if url[0:4] == 'http':
                        new_pages.add(url)
                        links_bd.append(unionUrlWord(idUrlWord, url))

            unique = list({ each['url'] : each for each in links_bd }.values())
            db.updateUrlDestination(idUrlWord,unique)
            # print("Adicionando mais ",len(unique))
            # print(len(new_pages))
            pages = new_pages
       
#page_list = ['https://g1.globo.com/ciencia-e-saude/','https://g1.globo.com/tecnologia/']
page_list = ['https://g1.globo.com/ciencia-e-saude/']
crawl(page_list,3) #trocar o 3 pelo número de níveis desejado
