import requests
import json
import os
from bs4 import BeautifulSoup
import math

def CountFiles(path):
    files = folders = 0

    for _, dirnames, filenames in os.walk(path):
        files += len(filenames)
        folders += len(dirnames)
    
    return files

class ACM():

    def GetIds(pageNumber):

        url = f'https://dl.acm.org/action/doSearch?AllField=%22data+quality%22%2C+%22big+data%E2%80%9C&startPage={pageNumber}&pageSize=100'

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def ExtractIds():
        page = 1
        load = True

        while(load):

            data = ACM.GetIds(pageNumber = page)
            
            result__count = data.find("span", {"class": "result__count"})

            totalPages = result__count.text.replace(" Results", "") 
            totalPages = int(totalPages.replace(",", ""))
            totalPages = math.ceil(totalPages / 100)

            divs = data.find_all("input", {"class": "issue-Item__checkbox"})
            
            ids = ''
            for i in range(len(divs)):
                if(i != 0):
                    ids = ids + ","
                
                ids = ids + divs[i]['name']

            ids = ids.replace("/", "%2F")
            
            with open(f'raw/ACM/page_{page}.json', 'w+', encoding='utf-8') as f:
                json.dump(ids, f, ensure_ascii=False, indent=4)

            if (page > totalPages):
                load = False
            
            page = page + 1

    def GetBibs(ids):

        url = f"https://dl.acm.org/action/exportCiteProcCitation?dois={ids}&targetFile=custom-bibtex&format=bibTex"

        r = requests.get(url)
        
        return r.json()

    def ExtractBibs():
        page = 1
        while (page <= CountFiles('raw/ACM')):

            with open(f'raw/ACM/page_{page}.json') as f:
                ids = json.load(f)
                bib = ACM.GetBibs(ids)
                
                # bibtrex =  "@inproceedings{"+item['id']+", author = {"+text_author+"}, title = {"+item['title']+"},year = {"+item['original-date']['date-parts'][0]+"},isbn = {"+item['ISBM']+"},publisher = {"+item['publisher']+"},address = {"+item['publisher-place']+"},url = {"+item['URL']+"}, doi = {"+item['DOI']+"}, abstract = {"+item['abstract']+"},location = {"+item['event-place']+"},series = {"+item['collection-title']+"}pages = {"+item['page']+"},numpages = {"+item['number-of-pages']+"},keywords = {"+item['keyword']+"} }"
                
                with open(f'dados/JSON/ACM_{page}.json', 'w+', encoding='utf-8') as f:
                    json.dump(bib, f, ensure_ascii=False, indent=4)
                page = page + 1

class IEEE():

    def GetIds(pageNumber):

        url = 'https://ieeexplore.ieee.org/rest/search'

        data = {
            "action":"search",
            "newsearch": True,
            "matchBoolean": True,
            "queryText":"(\"All Metadata\":data quality) AND (\"All Metadata\":big data)",
            "highlight": True,
            "returnFacets":["ALL"],
            "returnType":"SEARCH",
            "matchPubs": True,
            "rowsPerPage":"100",
            "pageNumber":pageNumber
        }

        headers = {
            "Content-Type": "application/json",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
        }

        r = requests.post(url, json = data, headers = headers)

        return r.json()

    def ExtractIds():
        page = 1
        load = True

        while(load):

            data = IEEE.GetIds(pageNumber = page)
            
            ids = ''
            for i in range(len(data['records'])):
                if(i != 0):
                    ids = ids + ","

                ids = ids + data['records'][i]['articleNumber']

            with open(f'raw/IEEE/page_{page}.json', 'w+', encoding='utf-8') as f:
                json.dump(ids, f, ensure_ascii=False, indent=4)

            if (page > data["totalPages"]):
                load = False
            
            page = page + 1

    def GetBibs(ids):

        url = f"https://ieeexplore.ieee.org/xpl/downloadCitations?recordIds={ids}&download-format=download-bibtex&citations-format=citation-only"

        headers = {
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
            "Accept": "application/x-bibtex"
        }

        r = requests.post(url, headers = headers)

        return r.text

    def ExtractBibs():
        page = 1
        while (page <= CountFiles('raw/IEEE')):

            with open(f'raw/IEEE/page_{page}.json') as f:
                ids = json.load(f)
                bib = IEEE.GetBibs(ids)

                bib = bib.replace("\r", "")
                bib = bib.replace("\n", "")
                bib = bib.replace("<br>", "")

                with open(f'dados/BIB/IEEE_{page}.bib', 'w+', encoding='utf-8') as f:
                    json.dump(bib, f, ensure_ascii=False, indent=4)
                page = page + 1

if __name__ == '__main__':

    IEEE.ExtractIds()
    IEEE.ExtractBibs()

    # ACM.ExtractIds()
    # ACM.ExtractBibs()