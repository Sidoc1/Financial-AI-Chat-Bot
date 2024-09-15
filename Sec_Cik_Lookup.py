import requests
class Lookup:
    
    def __init__(self,link):
        self.link=link
        self.dic_Name={}
        self.dic_Ticker={}
        headers={'User-Agent':'sadaq abdulle abdulle4@augsburg.edu'}
        r= requests.get(link,headers=headers)
        self.data= data = r.json()
        
    def name_to_cik(self,name):
            for item in self.data["data"]:
              self.dic_Name[item[1]]=(item[0],item[1],item[2])
              
            return self.dic_Name[name]
   
    def ticker_to_cik(self,ticket):
           
            for item in self.data["data"]:
             self.dic_Ticker[item[2]]=(item[0],item[1],item[2])
             
            return self.dic_Ticker[ticket]
    
    def quater_filing(self,cik,year,quater):
        headers={'User-Agent':'sadaq abdulle abdulle4@augsburg.edu'}
        len_of_cik=len(cik)
        cik_val='CIK'
        while(len_of_cik<10):
             cik_val+='0'
             len_of_cik+=1
        cik_val+=cik
        url_cik_json= f'https://data.sec.gov/submissions/{cik_val}.json'
        print(url_cik_json)
        r= requests.get(url_cik_json,headers=headers)
        data= r.json()
        if(quater =='Q4'):
            return self.annual_filing(cik,year)
        
    
        maping={'Q3':'','Q2':'','Q1':''}
        j=3
        for dates in range (len(data[ "filings"]["recent"][ "filingDate"])):
            #index =data[ "filings"]["recent"][ "filingDate"].index(dates)
            if  year in data[ "filings"]["recent"][ "filingDate"][dates] and data[ "filings"]["recent"]["form"][dates] == '10-Q':
             print(data[ "filings"]["recent"][ "filingDate"][dates], data[ "filings"]["recent"]["form"][dates], dates, " ->>> \n")
             maping['Q'+str(j)]=dates
             j-=1
             print("_____________________________________")
          

        print(maping)
        year_index=maping[quater]
        k=data[ "filings"]["recent"][ "accessionNumber"][year_index]
        accessionNumber=""
        for i in k:
          if i != "-":
            accessionNumber+=i 
        primaryDocument=data[ "filings"]["recent"][  "primaryDocument"][year_index]
        cik_number = data["cik"]

        url = f'https://www.sec.gov/Archives/edgar/data/{cik_number}/{accessionNumber}/{primaryDocument}'
        print(url)
        e= requests.get(url,headers=headers)
        return e.content
    
    def annual_filing(self,cik,year):
        headers={'User-Agent':'sadaq abdulle abdulle4@augsburg.edu'}
        len_of_cik=len(cik)
        cik_val='CIK'
        while(len_of_cik<10):
             cik_val+='0'
             len_of_cik+=1
        cik_val+=cik
        url_cik_json= f'https://data.sec.gov/submissions/{cik_val}.json'
        print(url_cik_json)
        
        r= requests.get(url_cik_json,headers=headers)
        data= r.json()
        index1=0
        for dates in range (len(data[ "filings"]["recent"][ "filingDate"])):
            if  year in data[ "filings"]["recent"][ "filingDate"][dates] and data[ "filings"]["recent"]["form"][dates] == '10-K':
               index1=data[ "filings"]["recent"][ "filingDate"][dates]
               break
        primaryDocument=(data[ "filings"]["recent"][ "filingDate"].index(index1))
        k=data[ "filings"]["recent"][ "accessionNumber"][primaryDocument]
        str1=""
        for i in k:
            if i != "-":
                str1+=i
        q=data[ "filings"]["recent"][  "primaryDocument"][primaryDocument]
        cik_number = data["cik"]

        url = f'https://www.sec.gov/Archives/edgar/data/{cik_number}/{str1}/{q}'
        print(url)
        e= requests.get(url,headers=headers)
        return e.content
lk= Lookup('https://www.sec.gov/files/company_tickers_exchange.json')
lk.quater_filing(str(lk.name_to_cik("Apple Inc.")[0]),"2023",'Q3')
#print(type(lk.name_to_cik("Apple Inc.")))

'''#Testing
headers={'User-Agent':'sadaq abdulle abdulle4@augsburg.edu'}
r= requests.get('https://data.sec.gov/submissions/CIK0000320193.json',headers=headers)
data= r.json()
#print(data[ "filings"]["recent"][ "accessionNumber"][6])
#print(data[ "filings"]["recent"][  "primaryDocument"][6])
cik=str(data["cik"])
#print(data[ "filings"]["recent"]["primaryDocDescription"])
for i in data[ "filings"]["recent"]["primaryDocDescription"]:
     if i == '10-K':
          index= data[ "filings"]["recent"]["primaryDocDescription"].index(i)
          print(i,data[ "filings"]["recent"][ "filingDate"][index])
date_index =""
for i in data[ "filings"]["recent"][ "filingDate"]:
    index =data[ "filings"]["recent"][ "filingDate"].index(i)
    if '2023'in i:
       if data[ "filings"]["recent"]["primaryDocDescription"][index] == '10-Q':
        print(i, data[ "filings"]["recent"]["primaryDocDescription"][index] )
        date_index = i
        break
primaryDocument=(data[ "filings"]["recent"][ "filingDate"].index(date_index))
k=data[ "filings"]["recent"][ "accessionNumber"][primaryDocument]
str1=""
for i in k:
    if i != "-":
        str1+=i
q=data[ "filings"]["recent"][  "primaryDocument"][primaryDocument]
base_url = "https://www.sec.gov/Archives/edgar/data"
cik_number = "320193"

url = f'https://www.sec.gov/Archives/edgar/data/{cik_number}/{str1}/{q}'
print(url)
e= requests.get(url,headers=headers)'''
#print(e.content)
'''
lk= Lookup('https://www.sec.gov/files/company_tickers_exchange.json')
print(lk.name_to_cik("Apple Inc."))
print(lk.ticker_to_cik("GOOGL"))'''
