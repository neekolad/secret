import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
base_url = "https://canadianjewellers.com/directory/"

res = requests.get(base_url, headers=headers)
content = bs(res.content, 'html.parser')
items = content.select("tr.member-row")
print(items[542])


prods=[]
for index, i in enumerate(items):
    if i.find('h3') != None:
        name = i.find('h3').text
    else: name = ""
    # print(str(index) + ":" + name)

    if i.find_all('p') !=None:
        tel = str(i.find_all('p')[0].text)
        addr_string = str(i.find_all('p')[1]).split("<br/>")
        if len(addr_string) > 1:
            addr = addr_string[0][12:].strip().replace("Unlisted Address", "")
            state_str = addr_string[1].split('<')[0].strip()
        
        if len(state_str.split(",")) > 1:
            state = state_str.split(",")[1].strip()
            city = state_str.split(", ")[0].strip()
        
        if len(i.find_all('p')) > 2:
            site = str(i.find_all('p')[2].text)
            if " " in site:
                site = ""
        else: site =""
    else:
        tel = ""
        addr = ""

    if i.find('td', class_="membership-column") != None:
        memb = i.find('td', class_="membership-column").text.replace("View Map", "")
    else: memb=""

    services=[]
    serv = i.find('td', class_="type-of-service-column").find_all('span')
    if serv != None:
        for s in serv:
            services.append(s.text.strip())


    prod = [name, addr, city, state, tel, site, memb, " - ".join(services)]

    prods.append(prod)

for i in prods:
    print(i)


df = pd.DataFrame(prods, columns=["Business Name", "Address", "City", "Province", "Phone Number", "Website", "Business Type", "Types of Services"])

df.to_csv('canadianjewellers.csv', index=False)
df.to_excel('canadianjewellers.xlsx', index=False)



