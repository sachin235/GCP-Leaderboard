# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import fileinput
import json
import time
import concurrent.futures

biglist=[]
url =[]
url2 =[]

track1=[
    'Getting Started: Create and Manage Cloud Resources',
    'Perform Foundational Infrastructure Tasks in Google Cloud',
    'Set up and Configure a Cloud Environment in Google Cloud',
    'Deploy and Manage Cloud Environments with Google Cloud',
    'Build and Secure Networks in Google Cloud',
    'Deploy to Kubernetes in Google Cloud'
    ]

track2 = [
    'Getting Started: Create and Manage Cloud Resources',
    'Perform Foundational Data, ML, and AI Tasks in Google Cloud',
    'Insights from Data with BigQuery',
    'Engineer Data in Google Cloud',
    'Integrate with Machine Learning APIs',
    'Explore Machine Learning Models with Explainable AI'
    ]
#get the url in list

def data_scraping (url):
    #print("in data scraping")
    with fileinput.input(files=('userurl.txt')) as f:
        for line in f:
            url.append(line.replace("\n", ""))
    for ele in url:
        if ele.strip():
            url2.append(ele)
    start_thread(url2)

    # Connect to the URL

def data_gathering(link):
    #t3 = time.time()
    #print("data gathering")
    tempdic = {}
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    track1completed = []
    track2completed = []
    profile = soup.findAll('div', attrs = {'class':'public-profile__hero'})[0]
    dp = profile.img['src']
    name = profile.h1.text
    tempdic['name'] = name.strip()
    tempdic['dp'] = dp
    #tempdic['qlabid'] = link
    quests = soup.findAll('ql-badge')
    for quest in quests:
        allquest = json.loads(quest.get('badge'))['title']
        #print(allquest)
        if allquest in track1:
            track1completed.append(allquest)
        if allquest in track2:
            track2completed.append(allquest)
    tempdic['track1'] = track1completed
    tempdic['track2'] = track2completed

    tempdic['lentrack1'] = len(track1completed)
    tempdic['lentrack2'] = len(track2completed)

    tempdic['qcomplete_no'] = len(track1completed) + len(track2completed)
    #print(tempdic['qcomplete_no'])

    if tempdic['qcomplete_no']!=0:
        print(len(biglist)," ",tempdic['name']," ",tempdic['qcomplete_no']," ",tempdic['track1']," ",tempdic['track2'])
        biglist.append(tempdic)
        print("data saved")
    else:
        print("no badges")
    #t4 = time.time()
    #print(f"{t4-t3} seconds to download this profile.")
    #print("data saved")




def data_saving (biglist):
    print("in data saving")
    #print(biglist)
    #print("The original dictionary : " + str(biglist))
    #print("\n")
    res = sorted(biglist, key = lambda x: x['qcomplete_no'], reverse=True)
    #print("The sorted dictionary by marks is : " + str(res))
    with open('finallist.txt', 'w') as f:
        print(biglist, file=f)
    with open('sortedfinallist.txt', 'w') as f:
        print(res, file=f)
    with open("my.json","w") as f:
        json.dump(res,f)
    f.close()

    tk1 = 0
    tk2 = 0
    tkt = 0
    for tempdic in res:
        x = int(tempdic['lentrack1'])
        y = int(tempdic['lentrack2'])

        if x == 6:
            tk1+=1
        if y == 6:
            tk2+=1
        if (x+y)!= 0:
            tkt+=1

    print("Number of people completed track 1 : ",tk1)
    print("Number of people completed track 2 : ",tk2)
    print("Number of people completed atleast 1 track : ",tkt)
    #print("number of people completed atleast one track ",num)
    #print(res)



def start_thread(url2):

    threads = 10
    #print("in start thread")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(data_gathering, url2)
    data_saving (biglist)



def main(url):
    #print("in main")
    data_scraping (url)


t0 = time.time()
main(url)
t1 = time.time()
print(f"{t1-t0} seconds to download {len(url2)} profile.")
print("number of people started",len(biglist))
