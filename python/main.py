import requests
import json
import os
from bs4 import BeautifulSoup

def CountFiles(path):
    files = folders = 0

    for _, dirnames, filenames in os.walk(path):
        files += len(filenames)
        folders += len(dirnames)
    
    return files

class ACM():

    def GetIds(pageNumber):

        url = f'https://dl.acm.org/action/doSearch?AllField=%22data+quality%22%2C+%22big+data%22&startPage={pageNumber}&pageSize=50&startPage=0&target=default&content=standard&sortBy='

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def ExtractIds():
        page = 1
        load = True

        while(load):

            data = ACM.GetIds(pageNumber = page)
  
            divs = data.find_all("input", {"class": "issue-Item__checkbox"})
            
            ids = ''
            for i in range(len(divs)):
                if(i != 0):
                    ids = ids + ","
                
                ids = ids + divs[i]['name']

            ids = ids.replace("%2F", "/")
            
            with open(f'raw/ACM/page_{page}.json', 'w+', encoding='utf-8') as f:
                json.dump(ids, f, ensure_ascii=False, indent=4)

            if (page > 41):
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

                print(f"ACM - Page {page} de {CountFiles('raw/ACM')}")
                
                ids = json.load(f)
                bib = ACM.GetBibs(ids)

                data = ""
                for i in range(len(bib['items'])):
                    for i_item in bib['items'][i]:
                        item = bib['items'][i][i_item]

                        bibtrex = "@inproceedings{"+item['id']

                        if "title" in item.keys():
                            bibtrex = bibtrex + ",title = {"+item['title']+"}"

                        if "author" in item.keys():
                            
                            text = ''
                            for i in range(len(item['author'])):
                                if(i != 0):
                                    text = text + ", "

                                if "family" in item['author'][i].keys():
                                    text = text + item['author'][i]['family'] + " "

                                if "given" in item['author'][i].keys():
                                    text = text + item['author'][i]['given'] + " "

                            bibtrex = bibtrex + ", author = {"+text+"}"
                        
                        if "issued" in item.keys():
                            bibtrex = bibtrex + ",year = {"+str(item['issued']['date-parts'][0][0])+"}"
                        
                        if "ISBN" in item.keys():
                            bibtrex = bibtrex + ", isbn = {"+item['ISBN']+"}"

                        if "publisher" in item.keys():
                            bibtrex = bibtrex + ", publisher = {"+item['publisher']+"}"

                        if "publisher-place" in item.keys():
                            bibtrex = bibtrex + ", address = {"+item['publisher-place']+"}"

                        if "URL" in item.keys():
                            bibtrex = bibtrex + ", url = {"+item['URL']+"}"

                        if "DOI" in item.keys():
                            bibtrex = bibtrex + ", doi = {"+item['DOI']+"}"

                        if "abstract" in item.keys():
                            bibtrex = bibtrex + ", abstract = {"+item['abstract']+"}"

                        if "event-place" in item.keys():
                            bibtrex = bibtrex + ", location = {"+item['event-place']+"}"
                        
                        if "collection-title" in item.keys():
                            bibtrex = bibtrex + ", series = {"+item['collection-title']+"}"

                        if "page" in item.keys():
                            bibtrex = bibtrex + ", pages = {"+item['page']+"}"

                        if "number-of-pages" in item.keys():
                            bibtrex = bibtrex + ", numpages = {"+item['number-of-pages']+"}"
                        
                        if "keyword" in item.keys():
                            bibtrex = bibtrex + ", keywords = {"+item['keyword']+"}"

                        bibtrex = bibtrex + "}"

                        data = data + bibtrex;

                with open(f'dados/BIB/ACM_{page}.bib', 'w', encoding='utf-8') as f:
                    json.dump(data, f)
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

                print(f"IEEE - Page {page} de {CountFiles('raw/IEEE')}")

                ids = json.load(f)
                bib = IEEE.GetBibs(ids)

                bib = bib.replace("\r", "")
                bib = bib.replace("\n", "")
                bib = bib.replace("<br>", "")

                with open(f'dados/BIB/IEEE_{page}.bib', 'w+', encoding='utf-8') as f:
                    json.dump(bib, f, ensure_ascii=False, indent=4)
                page = page + 1

if __name__ == '__main__':

    # IEEE.ExtractIds()
    # IEEE.ExtractBibs()

    ACM.ExtractIds()
    ACM.ExtractBibs()