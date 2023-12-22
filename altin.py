from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL
URL = 'https://altin.doviz.com/'

# user-agent
headers = {"User-Agent": userbilgileri.user_agent}

try:
    # Sayfa bağlantısının yapılması
    page = requests.get(URL, headers = headers)
    # Hata durumunda istek hatası alınır
    page.raise_for_status()
    # Sayfa bilgilerini alma
    content = BeautifulSoup(page.content, 'html.parser')
except requests.exceptions.RequestException as e:
    print(f"Hata oluştu: {e}")


# isimler
currencyDetails = content.find_all('div', class_='currency-details')
variableNameList = list()
for items in currencyDetails:
    variableNames = items.get_text().strip()
    variableNameList.append(variableNames)


# Alış
currentBuyPrices = content.find_all('td', class_ = 'text-bold', attrs={'data-socket-attr': 'bid'})
buyPricesList = list()
for items in currentBuyPrices:
    variableBuyPrices = items.get_text().strip().replace('$','').replace(',','.')[0:5]
    buyPricesList.append(variableBuyPrices)


# Satış
currentSellPrices = content.find_all('td', class_ = 'text-bold', attrs={'data-socket-attr': 'ask'})
sellPricesList = list()
for items in currentSellPrices:
    variableSellPrices = items.get_text().strip().replace('$','').replace(',','.')[0:5]
    sellPricesList.append(variableSellPrices)


# Günlük Fark
dailyChange = content.find_all('td', class_ = 'text-bold', attrs={'data-socket-attr': 'c'})
dailyChangeList = list()
for items in dailyChange:
    change = items.get_text().strip().replace('%','').replace(',','.')
    dailyChangeList.append(change)

# Para birimi bilgileri
typesList = ['$', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺', '₺']



# DataFrame
data = {'Altın': variableNameList, 'Alış': buyPricesList, 'Satış': sellPricesList, 'Günlük Fark': dailyChangeList, 'Para Birimi': typesList}
df = pd.DataFrame(data)

# Veri Dönüştürme
df['Alış'] = df['Alış'].astype(float)
df['Satış'] = df['Satış'].astype(float)
df['Günlük Fark'] = df['Günlük Fark'].astype(float)


print(df)
