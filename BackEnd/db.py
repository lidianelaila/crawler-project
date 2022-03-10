import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

mongo_client: pymongo.MongoClient = None
# hostDB = 'mongodb+srv://root:ASLA5jeQZQZCf3Bs@cluster.ko8t6.mongodb.net/test?retryWrites=true&w=majority'
hostDB='localhost:27017'

def connectDB():
    global mongo_client
    if mongo_client is None:
        mongo_client = pymongo.MongoClient(host= hostDB).project

#######FUNÇÕES PARA CRAWLER E PAGE RANK#########
def paginaIndexada(url):
    retorno = -1
    connectDB()
    resUrl = list(mongo_client.urlPalavra.find({"url" : url}))
    if len(resUrl)>0:
        retorno = -2
    return retorno

def insertUlrPage(urlWord):
    connectDB()
    id = mongo_client.urlPalavra.insert_one(urlWord)
    return id.inserted_id

def updateUrlDestination(idUrl, page):
    connectDB()
    mongo_client.urlPalavra.update_one(
   { "_id": ObjectId(idUrl) },
   { "$set": { "urlDestino": page } }
)

def updateRestartScore():
    connectDB()
    mongo_client.urlPalavra.update_many({},{"$set": {"nota": 1.0}} )

def selectAllUrls():
    connectDB()
    return list(mongo_client.urlPalavra.find({},{"_id":0, "urlDestino":0,"palavra":0,"paragrafo":0,"nota":0}))

def getAmountUrlDestino():
    connectDB()
    return list(mongo_client.urlPalavra.aggregate([
            {
                "$project": {
                    "url": 1,
                    "qtdUrlDestino": { 
                        "$cond": { 
                            "if": { 
                                "$isArray": "$urlDestino" 
                            }, 
                            "then": { 
                                "$size": "$urlDestino" 
                            }, 
                            "else": "NA"
                        } 
                    }
                }
            }
        ]))

def urlsThatCallUrl(url):
    connectDB()
    return list(mongo_client.urlPalavra.find( {
                     "urlDestino": { "$all": [
                                    { "$elemMatch" : { "url": url } }
                                  ] }
                   },{"_id":0, "urlDestino":0,"palavra":0,"paragrafo":0}))

def updateScore(url,score):
    connectDB()
    mongo_client.urlPalavra.update_one({"url":url},{"$set": {"nota": score}} )

######FUNÇÕES PARA BUSCA#####
def buscaMaisPalavras(consulta):
    connectDB()
    result = list(mongo_client.urlPalavra.find({"palavra":{"$in":consulta}},{"_id":0,"urlDestino":0,"paragrafo":0,"nota":0}))
    return result

def buscaParagrafo(consulta):
    connectDB()
    result = list(mongo_client.urlPalavra.find({"url":consulta},{"_id":0,"urlDestino":0,"palavra":0,"nota":0}))
    return result

def findUrlScore(urls):
    connectDB()
    return mongo_client.urlPalavra.find({"url":{"$in":urls}},{"_id":0, "urlDestino":0,"palavra":0,"paragrafo":0})

def countAmountUrlInDestionationUrls(url):
    connectDB()
    return mongo_client.urlPalavra.count_documents( {
                     "urlDestino": { "$all": [
                                    { "$elemMatch" : { "url": url } }
                                  ] }
                   })