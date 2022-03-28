import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

#url for the main page with calendar and years/months selectors
urls = 'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_lib/cgiirbis_64.exe?C21COM=F&I21DBN=BIBL&P21DBN=BIBL&S21FMT=&S21ALL=&Z21ID='
grab = requests.get(urls)
soup = BeautifulSoup(grab.text, 'html.parser')

#years are filled dynamically through js script, hardcoded them here
year_list_selector = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993']

#first loop – creating urls for each year, output in sitemap.csv
pages = []
#looping through the years
for years in year_list_selector:
   print("year is", years)
   url = 'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_lib/cgiirbis_64.exe?Z21ID=&I21DBN=BIBL&P21DBN=BIBL&C21COM=F&S21YEAR=' + years
   pages.append(url)
   print(url)
   grab = requests.get(url)
   soup = BeautifulSoup(grab.text, 'html.parser')
   f = open("sitemap.csv", "a")
   for link in soup.find_all("a"):
      data = link.get('href')
      f.write(data)
      f.write("\n")
      print(data)
f.close()

#second loop – creating urls for each month within a year, output in months_sitemap.csv
searchfile = open("sitemap.csv", "r")
months_ds = open("months_sitemap.csv", "w")
for line in searchfile:
    if "S21All=<.>DP" in line:
        print(line)
        months_ds.write('http://www.irbis-nbuv.gov.ua' + line)
searchfile.close()
months_ds.close()

#third loop – iterating through urls inside months entry, output in content.csv
results = []
with open('months_sitemap.csv', newline='') as f:
    for row in csv.reader(f):
        print("row is", row)
        row = str(row)[2:-2]
        print("row is", row)
        grab = requests.get(row)
        soup = BeautifulSoup(grab.text, 'html.parser')
        ds = open ("content.csv", "a")
        for link in soup.find_all("a"):
            data = link.get('href')
            ds.write(data)
            ds.write("\n")
            print(data)
print(results)
f.close()

#fourth loop – refining results of content.csv: removing duplicate links and links to third-party resources, adding 'http://www.irbis-nbuv.gov.ua' prefix. Output in content_cleaned.csv
csv = open("content.csv", "r")
cleaned_csv = open("content_cleaned.csv", "w")
for line in csv:
    if "/cgi-bin/irbis_lib" in line:
        cleaned_csv.write('http://www.irbis-nbuv.gov.ua' + line)
csv.close()
cleaned_csv.close()
df = pd.read_csv('content_cleaned.csv')
df.drop_duplicates(inplace=True)
df.to_csv('content_cleaned.csv', index=False)
