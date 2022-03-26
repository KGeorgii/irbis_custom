import requests
from bs4 import BeautifulSoup
 
urls = 'https://i.irklib.ru/cgi/irbis64r_61/cgiirbis_64.exe?C21COM=F&P21DBN=IBIS&I21DBN=IBIS'
grab = requests.get(urls)
soup = BeautifulSoup(grab.text, 'html.parser')

#https://i.irklib.ru/cgi/irbis64r_61/cgiirbis_64.exe?C21COM=F&P21DBN=IBIS&I21DBN=IBIS // The first page when we enter the electronic catalogue. First, I tried to run through the "YEARS" selector
#https://i.irklib.ru/cgi/irbis64r_61/cgiirbis_64.exe?Z21ID=&I21DBN=IBIS&P21DBN=IBIS&C21COM=F&LNG=&S21YEAR=2021 // when we select other year, the links gets like this.
#https://i.irklib.ru/cgi/irbis64r_61/cgiirbis_64.exe?C21COM=F&P21DBN=IBIS&I21DBN=IBIS&S21YEAR=2021 //The first link with added &S21YEAR=2022 works!

#looking for year in selector
year_list = soup.find(class_='inp1')
#select a year
year_list_selector = year_list.find_all('option')
#count number of years for a loop
x = len(year_list_selector)

#print(year_list.prettify())
#print(x)

#empty list to fill
pages = []

#looping through the years
for years in year_list_selector:
   year = years.contents[0]
   #print(year)
   url = 'https://i.irklib.ru/cgi/irbis64r_61/cgiirbis_64.exe?Z21ID=&I21DBN=IBIS&P21DBN=IBIS&C21COM=F&LNG=&S21YEAR=' + year
   pages.append(url)
   #print(url)
   grab = requests.get(url)
   soup = BeautifulSoup(grab.text, 'html.parser')
   f = open("sitemap.xml", "a")
   for link in soup.find_all("a"):
      data = link.get('href')
      f.write(data)
      f.write("\n")
      #print(data)
 
   f.close()

#print(pages)