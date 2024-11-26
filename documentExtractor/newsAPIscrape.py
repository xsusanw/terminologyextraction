from newsapi import NewsApiClient
import clickLink as cl
import threading

newsapi = NewsApiClient(api_key='0c1e4440607a4575970b4540ebc77e8f')

query = input('Type a query: ')
outFile = input('What is the name of the output file you want to store it in?: ')
artNum = ""
while artNum.isdigit()==False:
    artNum = input('How many articles do you want to parse?')
artNum = int(artNum)
maxthreads = 10
pagenum = 3
domains = 'apnews.com, reuters.com, bbc.com, npr.org, pbs.org, bloomberg.com, axios.com, c-span.org, thehill.com, politico.com, newsweek.com, time.com, usatoday.com, abcnews.go.com, cbsnews.com, nbcnews.com, marketwatch.com, fortune.com, businessinsider.com, theatlantic.com'



allArticles = newsapi.get_everything(q=query,page=pagenum,domains=domains)
print(len(allArticles['articles']))
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
        print(content[:100])

i=0
while successful_count<artNum:
    if i<len(allArticles['articles']):
        article = allArticles['articles'][i]
    else:
        i=0
        pagenum+=1
        allArticles = newsapi.get_everything(q=query,page=pagenum, domains=domains)
        article = allArticles['articles'][i]
        print(f'len of all articles:{len(allArticles['articles'])}')
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
    j=0
    for key,item in allContent.items():
        outp.write(f'HEADER: {key}\n\n')
        outp.write(f'CONTENT: {item}\n\n')
        print(j)
        j+=1

    