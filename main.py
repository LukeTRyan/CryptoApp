from urllib.request import urlopen as uReq
import urllib
from flask import Flask, render_template, request
import random
from bs4 import BeautifulSoup as soup
import re
import requests

app = Flask(__name__)

def grabCrypto():
    my_url = 'https://coinmarketcap.com/all/views/all/'

    #opening connection, grabbing page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    #html parsing 
    page_soup = soup(page_html, "html.parser")

    #grabs each crypto
    containers = page_soup.findAll("tr",{"class":""})

    priceList = []
    marketCapList = []
    volumeList = []
    percentChangeList = []
    URLList = []

    #for each row (each cryptocurrency)
    for container in containers[1:]:

        MC = container.findAll("td", {"class":"market-cap"})
        P = container.findAll("a", {"class":"price"})
        V = container.findAll("a", {"class":"volume"})
        PC = container.findAll("td",{"class":"percent-change"})
        URL = container.findAll("a", {"class":"link-secondary"}, {"href":""})

        match = re.search(r'href=[\'"]?([^\' >]+)', str(URL)).group(0)
        match2 = re.search(r'[\/][^href]([^\' >]+/)', str(match)).group(0)

        market_cap = MC[0].text.strip()
        try:
            price = P[0].text
        except: 
            pass
        try:    
            volume = V[0].text
        except: 
            pass
        try:    
            percent_change = PC[0].text
        except: 
            pass

        URLList.append(match2)
        priceList.append(price)
        marketCapList.append(market_cap)
        volumeList.append(volume)
        percentChangeList.append(percent_change)    


    #grabs a random index from the range of cryptocurrencies
    random_choice = random.sample(marketCapList,1)
    indexValue = marketCapList.index(random_choice[0])

    #adds the details of the random crypto (except name) to a list
    Random_choice_list = []
    Random_choice_list.append(marketCapList[indexValue])
    Random_choice_list.append(priceList[indexValue])
    Random_choice_list.append(volumeList[indexValue])
    Random_choice_list.append(percentChangeList[indexValue])
    Random_choice_list.append(URLList[indexValue])

    #uses the regex url to find this random cryptos information page
    new_url = 'https://coinmarketcap.com' + Random_choice_list[4]

    uClient = uReq(new_url)
    page_html = uClient.read()
    uClient.close()

    #finds the name and ticker code, and adds this to the information list
    new_soup = soup(page_html, "html.parser")
    newName = new_soup.findAll("h1", {"class":"details-panel-item--name"})
    textName = newName[0].text
    Random_choice_list.append(textName)

    images = new_soup.findAll("h1", {"class":"details-panel-item--name"})
    imgURL = re.search(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', str(images)).group(0)

    path = 'C:\\Users\\Luke\\Desktop\\Projects\\CryptoApp\\static\\cryptoIcon.jpg'
    f = open(path,'wb')
    f.write(requests.get(imgURL).content)
    f.close()
    
    return Random_choice_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_crypto():
    Random_choice_list = grabCrypto()
    url = 'https://coinmarketcap.com' + Random_choice_list[4]
    return render_template('generated.html', choices = Random_choice_list, url = url)

if __name__ == '__main__':
    app.run(debug=True)

    