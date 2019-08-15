from bs4 import BeautifulSoup
import requests
import json
import re
import time

while True:

    with open('arrests.json') as json_file:
        arrests = json.load(json_file)


    response = requests.get('https://kentucky.arrests.org/index.php?county=335&page=1&results=56')

    soup = BeautifulSoup(response.content, 'html.parser')

    for li in soup.findAll('div', class_='profile-card'):
        try:
            charges = []
            name = list(li.children)[1].get_text()
            name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
            liSoup = BeautifulSoup(str(li), 'html.parser')
            for charge in liSoup.findAll('div', class_='charge-title'):
                charges.append(charge.get_text())

            if charges:
                del charges[-1]

            time = liSoup.find('div', class_='description').get_text()

            picture = list(li.children)[3]
            picture = str(picture).split('data-large=')
            picture = picture[1]
            picture = picture.split('"')
            picture = picture[1]

            chargesString = ''
            for charge in charges:
                chargesString = chargesString + charge + '\n'

            arrest = {
                'name': name,
                'charges': chargesString,
                'time': time,
                'picture': picture
            }

            if arrest not in arrests:
                print('New Arrest')
                arrests.insert(0, arrest)

        except:
            pass

    with open('arrests.json', 'w') as f:
        json.dump(arrests, f)
    
    print('scraping')
    time.sleep(3600)

