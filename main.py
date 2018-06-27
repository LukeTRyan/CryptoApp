from urllib.request import urlopen as uReq
from flask import Flask, render_template, request
import random
from bs4 import BeautifulSoup as soup

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

    filename = "data.csv"
    f = open(filename, "w")

    namesList = []
    priceList = []
    marketCapList = []
    volumeList = []
    percentChangeList = []

    for container in containers[1:]:

        N = container.findAll("a", {"class":"currency-name-container"})
        MC = container.findAll("td", {"class":"market-cap"})
        P = container.findAll("a", {"class":"price"})
        V = container.findAll("a", {"class":"volume"})
        PC = container.findAll("td",{"class":"percent-change"})

        name = N[0].text
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
        f.write(name + "," + market_cap.replace(",", "") + "," + price.replace(",", "") + "," + volume.replace(",", "") + "," + percent_change + "\n")

    
        namesList.append(name)
        priceList.append(price)
        marketCapList.append(market_cap)
        volumeList.append(volume)
        percentChangeList.append(percent_change)

    f.close()     

    random_choice = random.sample(namesList,1)
    indexValue = namesList.index(random_choice[0])

    Random_choice_list = []
    Random_choice_list.append(namesList[indexValue])
    Random_choice_list.append(marketCapList[indexValue])
    Random_choice_list.append(priceList[indexValue])
    Random_choice_list.append(volumeList[indexValue])
    Random_choice_list.append(percentChangeList[indexValue])
    return Random_choice_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_crypto():
    Random_choice_list = grabCrypto()
    return render_template('generated.html', choices = Random_choice_list)



if __name__ == '__main__':
    app.run(debug=True)

    