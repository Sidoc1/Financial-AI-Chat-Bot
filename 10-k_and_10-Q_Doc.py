from urllib import request, parse
import json

class Lookup:
    
    def __init__(self, link):
        #self.link = link
        self.dic_Name = {}
        self.dic_Ticker = {}
        #headers = {'User-Agent': 'sadaq abdulle abdulle4@augsburg.edu'}
       # req = request.Request(link, headers=headers)
        #with request.urlopen(req) as response:
            #self.data = json.loads(response.read().decode())
        self.data=link
    def name_to_cik(self, name):
        for item in self.data["data"]:
            self.dic_Name[item[1]] = (item[0], item[1], item[2])
        return self.dic_Name[name]
   
    def ticker_to_cik(self, ticker):
        for item in self.data["data"]:
            self.dic_Ticker[item[2]] = (item[0], item[1], item[2])
        return self.dic_Ticker[ticker]
    
    def quater_filing(self, cik, year, quater):
        headers = {'User-Agent': 'sadaq abdulle abdulle4@augsburg.edu'}
        len_of_cik = len(cik)
        cik_val = 'CIK'
        while len_of_cik < 10:
            cik_val += '0'
            len_of_cik += 1
        cik_val += cik
        url_cik_json = f'https://data.sec.gov/submissions/{cik_val}.json'
        print(url_cik_json)
        
        req = request.Request(url_cik_json, headers=headers)
        with request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        if quater == 'Q4':
            return self.annual_filing(cik, year)
        
        maping = {'Q3': '', 'Q2': '', 'Q1': ''}
        j = 3
        for dates in range(len(data["filings"]["recent"]["filingDate"])):
            if year in data["filings"]["recent"]["filingDate"][dates] and data["filings"]["recent"]["form"][dates] == '10-Q':
                print(data["filings"]["recent"]["filingDate"][dates], data["filings"]["recent"]["form"][dates], dates, " ->>> \n")
                maping['Q' + str(j)] = dates
                j -= 1
                print("_____________________________________")
          
        print(maping)
        year_index = maping[quater]
        k = data["filings"]["recent"]["accessionNumber"][year_index]
        accessionNumber = "".join(i for i in k if i != "-")
        primaryDocument = data["filings"]["recent"]["primaryDocument"][year_index]
        cik_number = data["cik"]

        url = f'https://www.sec.gov/Archives/edgar/data/{cik_number}/{accessionNumber}/{primaryDocument}'
        print(url)
        
        req = request.Request(url, headers=headers)
        with request.urlopen(req) as response:
            e = response.read()
        return e
    
    def annual_filing(self, cik, year):
        headers = {'User-Agent': 'sadaq abdulle abdulle4@augsburg.edu'}
        len_of_cik = len(cik)
        cik_val = 'CIK'
        while len_of_cik < 10:
            cik_val += '0'
            len_of_cik += 1
        cik_val += cik
        url_cik_json = f'https://data.sec.gov/submissions/{cik_val}.json'
        print(url_cik_json)
        
        req = request.Request(url_cik_json, headers=headers)
        with request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        index1 = 0
        for dates in range(len(data["filings"]["recent"]["filingDate"])):
            if year in data["filings"]["recent"]["filingDate"][dates] and data["filings"]["recent"]["form"][dates] == '10-K':
                index1 = data["filings"]["recent"]["filingDate"][dates]
                break
        
        primaryDocument = data["filings"]["recent"]["filingDate"].index(index1)
        k = data["filings"]["recent"]["accessionNumber"][primaryDocument]
        str1 = "".join(i for i in k if i != "-")
        q = data["filings"]["recent"]["primaryDocument"][primaryDocument]
        cik_number = data["cik"]

        url = f'https://www.sec.gov/Archives/edgar/data/{cik_number}/{str1}/{q}'
        print(url)
        
        req = request.Request(url, headers=headers)
        with request.urlopen(req) as response:
            e = response.read()
        return e
