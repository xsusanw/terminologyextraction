from newsapi import NewsApiClient
import clickLink as cl
import threading

newsapi = NewsApiClient(api_key='')

query = input('Type a query: ')
outFile = input('What is the name of the output file you want to store it in?: ')
artNum = ""
while artNum.isdigit()==False:
    artNum = input('How many articles do you want to parse?')
artNum = int(artNum)
maxthreads = 10



allArticles = newsapi.get_everything(q=query)
allContent = {}
Threads = []
successful_count = 0
lock = threading.Lock()

def scrapeAndStore (article):
    global successful_count
    url = article['url']
    content = cl.scrapeLinks(url)
    if content!=None:
        with lock:
            allContent[url]=content
            successful_count +=1
        print(content)

i=0
while successful_count<artNum:
    article = allArticles['articles'][i]
    try:
        if threading.active_count() <= maxthreads:  # Limit the number of active threads
            thread = threading.Thread(target=scrapeAndStore, args=(article,))
            Threads.append(thread)
            thread.start()
            i += 1
        else:
            threading.Event().wait(1)
        

    except:
        pass
    



for thread in Threads:
    thread.join()


with open(outFile,'w', encoding='utf-8') as outp:
    for key,item in allContent.items():
        outp.write(f'HEADER: {key}\n\n')
        outp.write(f'CONTENT: {item}\n\n')

    