import requests

from bs4 import BeautifulSoup

url = input("Input the URL:\n")

r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
soup = BeautifulSoup(r.content, "html.parser")

title = soup.find('h1')
description = soup.find('div', {'class': ['summary_text']})

if None in (title, description):
    print('Invalid movie page!')
else:
    content = {'title': title.next.strip(), 'description': description.text.strip()}
    print(content)
