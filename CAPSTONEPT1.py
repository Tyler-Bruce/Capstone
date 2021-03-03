from bs4 import BeautifulSoup as bs
import gevent.monkey
gevent.monkey.patch_all()  #needed this so import requests could work. 
import requests
import re
import concurrent.futures
from time import time
import os


'''Create directories'''''''''''''''''''''''''''
os.chdir(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.getcwd()
async_dir = "textfiles_async"
serial_dir = "textfiles"
async_path = os.path.join(parent_dir, async_dir)
serial_path = os.path.join(parent_dir, serial_dir)
os.makedirs(async_path, exist_ok = True)
os.makedirs(serial_path, exist_ok = True)
''''''''''''''''''''''''''''''''''''''''''''''''

#NOTE: this script downloads 556 files for both serial and async functions
#NOTE: This script is exceeding the allowed requests for the SEC's website. 
#NOTE: After checking through the debugger, the SEC website only allows 10 requests per second
#NOTE: I get timed out for 10 minutes when I go over which causes the 0.01 second finish times

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
        url = requests.get(link)    
        soup = bs(url.content, 'html.parser')
        contents = soup.find_all('a')
        for textfile in contents:   #search through list of links for text file links and download text files
            if re.search('.+txt', str(textfile)):
                file = requests.get(sub_URL1 + textfile.get('href'))
                with open(serial_path + "\\"  + textfile.text, 'wb') as f: 
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
            with open(async_path + "\\" + textfile.text, 'wb') as f: 
                print(textfile.text)
                f.write(file.content)
                time.sleep(1000)

def main():
    
    links = [] #list of links

    parseDirectory(links) #parse directory to build list of subdirectory links
    
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     
    '''
    #SERIAL
    startTime = time()
    download(links)
    endTime = time()
    serialDuration = endTime - startTime
    '''
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  

    #ASYNC
    startTime = time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as \
    executor:
        for link in links:
            executor.submit(download_async, link)
    endTime = time()
    asyncDuration = endTime - startTime

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  
    #print("Serial Duration was ", "{:.2f}".format(serialDuration), " seconds")
    print("Async Duration was ", "{:.2f}".format(asyncDuration), " seconds")

    #First serial runthrough time is 213 seconds.
    #Second serial runthrough time is 139.66 seconds
    print('end')  #program ends

if __name__ == "__main__":
    main()

    



    
    



