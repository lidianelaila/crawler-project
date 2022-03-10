import db

def calculaPageRank(iteracoes):
    db.updateRestartScore()

    for i in range(iteracoes):
        print("Iteração " + str(i + 1))
        
        # cursorUrl = list(mongo_client.urlPalavra.find({},{"_id":0, "urlDestino":0,"palavra":0,"paragrafo":0,"nota":0}))
        cursorUrl = db.selectAllUrls()
        
        qtdByUrls = db.getAmountUrlDestino()
        count=1
        for url in cursorUrl:
            # print("########################################")
            print(url["url"], count)

            count+=1
            
            pr = 0.15
            
            # Retorna todas as urls que chamaram essa url
            cursorLinks = db.urlsThatCallUrl(url["url"])

            for link in cursorLinks:
                # print(link["url"])
                linkPageRank = link["nota"] 
                
                linkQuantidade=0
                for i in qtdByUrls:
                    if i['url'] == link["url"]:
                        linkQuantidade=i["qtdUrlDestino"]
                        break
                
                # print(linkPageRank)
                # print(linkQuantidade)
                pr += 0.85 * (linkPageRank / linkQuantidade)
                # print(pr)

            db.updateScore(url["url"],pr)
            # resultUpdate = mongo_client.urlPalavra.update_many({"url":url["url"]},{"$set": {"nota": pr}} )

calculaPageRank(5)
