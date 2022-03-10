import nltk
nltk.download('stopwords')
nltk.download('rslp')
import pymongo
import numpy as np
import itertools
import string
import re
import similaridade_cosseno as sc
import db

def normalizaMaior(notas):
    menor = 0.00001
    maximo = max(notas.values())
    if maximo == 0:
        maximo = menor
    return dict([(id, float(nota) / maximo) for (id, nota) in notas.items()])

def normalizaMenor(notas):
    menor = 0.00001
    minimo = min(notas.values())
    return dict([(id, float(minimo) / max(menor, nota)) for (id, nota) in notas.items()])

def frequenciaScore(linhas):
    contagem = dict([(linha[0], 0) for linha in linhas])
    for linha in linhas:
        contagem[linha[0]] += 1
    
    return normalizaMaior(contagem)

def localizacaoScore(linhas):
    localizacoes = dict([linha[0], 1000000] for linha in linhas)
    for linha in linhas:
        soma = sum(linha[1:])
        if soma < localizacoes[linha[0]]:
            localizacoes[linha[0]] = soma
    return normalizaMenor(localizacoes)

def distanciaScore(linhas):
    if len(linhas[0]) <= 2:
        return dict([(linha[0], 1.0) for linha in linhas])
    distancias = dict([(linha[0], 1000000) for linha in linhas])
    for linha in linhas:
        dist = sum([abs(linha[i] - linha[i - 1]) for i in range(2, len(linha))])
        if dist < distancias[linha[0]]:
            distancias[linha[0]] = dist
    return normalizaMenor(distancias)

def contagemLinkScore(linhas):
    contagem = dict([linha[0], 1.0] for linha in linhas)

    for i in contagem:
        result = db.countAmountUrlInDestionationUrls(i)
        contagem[i] = result
    
    return normalizaMaior(contagem)

def pageRankScore(linhas):
    pageranks = dict([linha[0], 1.0] for linha in linhas)
    notas = db.findUrlScore(list(pageranks.keys()))
    
    for i in pageranks:
        for n in notas:
            if n['url'] == i:
                pageranks[i] = n["nota"]
                break     
    return normalizaMaior(pageranks)

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

def pesquisaPeso(pesquisa): 
    consulta =pesquisa.split(' ')

    #aplicar stemmer
    stemmer = nltk.stem.RSLPStemmer()
    for pos in range(len(consulta)):
        consulta[pos]=stemmer.stem(consulta[pos])
    
    linhas = db.buscaMaisPalavras(consulta)
    
    if len(linhas)==0:
        return []

    values =[]
    for result in linhas:
        aux=[]
        aux.append([result["url"]])
        for palavra in consulta:
            positions=[i for i,x in enumerate(result["palavra"]) if x == palavra]
            if positions==[]:
                positions=[-1]
            aux.append(positions)
        values=values+list(itertools.product(*aux))
    
    
    totalscores = dict([linha[0], 0] for linha in values)
    
    pesos = [(4.0, localizacaoScore(values)),
             (3.0, distanciaScore(values)),
             (2.0, frequenciaScore(values)),
             (1.0, contagemLinkScore(values)), 
             (1.0, pageRankScore(values))]
    
    for (peso, scores) in pesos:
        for url in totalscores:
            totalscores[url] += peso * scores[url]
    
    scoresordenado = sorted([(score, url) for (url, score) in totalscores.items()], reverse = 1)
    
    lista_final=[]
    for (score, url) in scoresordenado[0:10]:
        listaParagrafo= db.buscaParagrafo(url)
        listaParagrafo[0]["paragrafo"].append(pesquisa)
        corpus_clear = sc.clear_text(listaParagrafo[0]["paragrafo"])
        vocabulary = sc.text_all(corpus_clear)
        features=[]
        for cp in corpus_clear:
            features.append(sc.fit_transform(cp,vocabulary))
        features=np.array(features)
        paragrafo_similar=sc.text_simillarities(len(listaParagrafo[0]["paragrafo"])-1, features, listaParagrafo[0]["paragrafo"],5)
        lista = {"url":url,"paragrafo":paragrafo_similar[0][0], "nota":score}
        lista_final.append(lista)

    # for lista in lista_final[0:20]:
    #     print('%f\t%s' % (lista["nota"],lista["url"]))       
    #     print(lista["paragrafo"])

    return lista_final[0:20]
