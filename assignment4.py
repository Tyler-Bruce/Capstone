from bs4 import BeautifulSoup as bs
import gevent.monkey
gevent.monkey.patch_all()  #needed this so import requests could work. 
import requests
import re
import concurrent.futures
from time import time
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#NOTE: there are 588 text files to download 
#NOTE: this script downloads 556 files for both serial and async functions
#NOTE: Some directories have multiple txt files which could be the culprit? that or some txt files
#      share names and the files are being overwritten
#NOTE: create list of directories and compare between two programs


'''Globals'''
sub_URL1 = 'https://www.sec.gov'  #splitting URL so that I can search through the list of directories easier
sub_URL2 = '/Archives/edgar/data/20/' #hrefs only contain this string + textfile name data so splitting here makes most sense
website = requests.get(sub_URL1 + sub_URL2) #http request for website

'''Parse Directory for subdirectories'''
def parseDirectory(links):
    soup = bs(website.content, 'html.parser')
    subdirectories = soup.find_all('a')
    for directory in subdirectories:
        if re.search(sub_URL2 + '.+', str(directory)):
            FULL_URL = sub_URL1 + directory.get('href')
            links.append(FULL_URL)

'''Parse subdirectories for text files + download text files Serially'''
def download(links):
    for link in links:
        url = requests.get(link)    #takes a while
        soup = bs(url.content, 'html.parser')
        contents = soup.find_all('a')
        for textfile in contents:   #search through list of links for text file links and download text files
            if re.search('.+txt', str(textfile)):
                file = requests.get(sub_URL1 + textfile.get('href'))
                with open(os.getcwd() + '\\textfiles\\' + textfile.text, 'wb') as f: #using the textfile.text causes the script to no longer download all the text files for some reason
                    print(textfile.text)               
                    f.write(file.content)

'''Parse subdirectories for text files + download text files Asynchronously'''
def download_async(link):
    url = requests.get(link)    
    soup = bs(url.content, 'html.parser')
    contents = soup.find_all('a')
    for textfile in contents:   #search through list of links for text file links and download text files
        if re.search('.+txt', str(textfile)):
            file = requests.get(sub_URL1 + textfile.get('href'))
            with open(os.getcwd() + '\\textfiles_async\\' + textfile.text, 'wb') as f: #using the textfile.text causes the script to no longer download all the text files for some reason
                print(textfile.text)
                f.write(file.content)

if __name__ == "__main__":

    links = [] #list of links

    parseDirectory(links) #parse directory to build list of subdirectory links
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     

    #SERIAL
    startTime = time()
    download(links)
    endTime = time()
    serialDuration = endTime - startTime

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
    links = []

    parseDirectory(links)
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
    #ASYNC
    startTime = time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as \
    executor:
        for link in links:
            executor.submit(download_async, link)
    endTime = time()
    asyncDuration = endTime - startTime
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
    print("Serial Duration was ", "{:.2f}".format(serialDuration), " seconds")
    print("Async Duration was ", "{:.2f}".format(asyncDuration), " seconds")

    #First serial runthrough time is 213 seconds.
    #Second serial runthrough time is 139.66 seconds
    print('end')  #program ends
    



    
    



