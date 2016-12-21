
# coding: utf-8

# In[8]:

from bs4 import BeautifulSoup
import requests
import scraperwiki


# In[44]:

pages = ['http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=1&expand=1&q=&mem=1&par=-1&gen=0&ps=100&st=1',
        'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=2&expand=1&q=&mem=1&par=-1&gen=0&ps=100&st=1']

basedata = []

for page in pages:
    print(page)
    soup = BeautifulSoup(requests.get(page).content)
    maindiv = soup.find('div',class_='search-filter-results')
    entries = maindiv.find_all('div',class_='row')
    for e in entries:
        row = {}
        dts = e.find_all('dt')
        dds = e.find_all('dd')
        row['name'] = e.find_all('a')[1].text
        row['link'] = e.find_all('a')[1].get('href')
        counter = 0
        while counter<len(dts):
            if dts[counter].text.strip() != 'Connect':
                row[dts[counter].text] = dds[counter].text
            counter+=1
        basedata.append(row)


# In[51]:

offices = []
for b in basedata:
    page = requests.get('http://aph.gov.au'+b['link'])
    soup = BeautifulSoup(page.content)
    details = soup.find('div',id='panel21')
    address = details.find_all('p')
    for i,a in enumerate(address):
        if i % 2 == 0:
            b2 = b.copy()
            b2['address'] = a.text.strip()
            b2['office'] = i/2 + 1
            offices.append(b2)


# In[54]:

scraperwiki.sqlite.save(unique_keys='',data=offices,table_name='offices')


# In[ ]:



