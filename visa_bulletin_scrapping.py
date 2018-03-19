
# coding: utf-8

# In[8]:


import requests
from bs4 import BeautifulSoup

homepage  = 'https://travel.state.gov'
visa_page = 'https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html'

page = requests.get(visa_page)
soup = BeautifulSoup(page.content, "lxml")

recent_link = soup.find_all("li",{"class":"current"})[1].find_all("a")[0].get("href")

recent_full_link = homepage + recent_link
print recent_full_link

thismonth_page = requests.get(recent_full_link)
thismonth_soup = BeautifulSoup(thismonth_page.content, "lxml")
   
all_divs = thismonth_soup.find_all('div',{'class':'tsg-rwd-text parbase section'})

def find_employment_collection(sec):
    
    if sum(['EMPLOYMENT' in x.text.upper() for x in sec.find_all('u')]) > 0:
        return sec
    else:
        return None

all_employment_collections = [y for y in [find_employment_collection(x) for x in all_divs] if y is not None]

final_date = all_employment_collections[0]
file_date = all_employment_collections[1]

