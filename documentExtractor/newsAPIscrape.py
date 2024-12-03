import eventregistry as e
import clickLink as cl
import threading



q = input('Type a query: ')
outFile = input('What is the name of the output file you want to store it in?: ')
artNum = ""
while artNum.isdigit()==False:
    artNum = input('How many articles do you want to parse?')
artNum = int(artNum)
maxthreads = 10
pagenum = 3
domains = 'apnews.com, reuters.com, bbc.com, npr.org, pbs.org, bloomberg.com, axios.com, c-span.org, thehill.com, politico.com, newsweek.com, time.com, usatoday.com, abcnews.go.com, cbsnews.com, nbcnews.com, marketwatch.com, fortune.com, businessinsider.com, theatlantic.com'



er = e.EventRegistry(apiKey = "57ca642b-b78a-426c-b84e-6487953609ed")
query = {
  "$query": {
    "$and": [
      {
        "keyword": q,
        "keywordSearchMode": "simple"
      },
      {
        "$or": [
          {
            "sourceUri": "apnews.com"
          },
          {
            "sourceUri": "reuters.com"
          },
          {
            "sourceUri": "bbc.com"
          },
          {
            "sourceUri": "npr.org"
          },
          {
            "sourceUri": "pb.pl"
          },
          {
            "sourceUri": "bloomberg.com"
          },
          {
            "sourceUri": "axios.com"
          },
          {
            "sourceUri": "thehill.com"
          },
          {
            "sourceUri": "politico.com"
          },
          {
            "sourceUri": "newsweek.com"
          },
          {
            "sourceUri": "time.com"
          },
          {
            "sourceUri": "usatoday.com"
          },
          {
            "sourceUri": "abcnews.go.com"
          },
          {
            "sourceUri": "cbsnews.com"
          },
          {
            "sourceUri": "marketwatch.com"
          },
          {
            "sourceUri": "fortune.com"
          },
          {
            "sourceUri": "businessinsider.com"
          },
          {
            "sourceUri": "theatlantic.com"
          }
        ]
      }
    ]
  },
  "$filter": {
    "forceMaxDataTimeWindow": "31"
  }
}
q = e.QueryArticlesIter.initWithComplexQuery(query)
allArticles = []
for article in q.execQuery(er, maxItems = 2000):
    allArticles.append(article['url'])
    print(article['url'])






allContent = {}
Threads = []
successful_count = 0
lock = threading.Lock()

def scrapeAndStore (url):
    global successful_count
    """url = article['url']"""
    content = cl.scrapeLinks(url)
    if content!=None:
        with lock:
            allContent[url]=content
            successful_count +=1
        print(content[:100])

i=0
while successful_count<artNum:
    if i<len(allArticles):
        article = allArticles[i]
    else:
        break
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

    