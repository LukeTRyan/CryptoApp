from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://coinmarketcap.com/'

#opening connection, grabbing page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing 
page_soup = soup(page_html, "html.parser")

#grabs each crypto
containers = page_soup.findAll("tr",{"class":""})


filename = "data.csv"
f = open(filename, "w")

headers = "name, market_cap, price, volume, percent_change\n"

f.write(headers)

for container in containers[1:]:

    N = container.findAll("a", {"class":"currency-name-container"})
    MC = container.findAll("td", {"class":"market-cap"})
    P = container.findAll("a", {"class":"price"})
    V = container.findAll("a", {"class":"volume"})
    PC = container.findAll("td",{"class":"percent-change"})

    name = N[0].text
    market_cap = MC[0].text.strip()
    price = P[0].text
    volume = V[0].text
    percent_change = PC[0].text
    
    f.write(name + "," + market_cap + "," + price + "," + volume.replace(",", "|") + "," + percent_change + "\n")

f.close()