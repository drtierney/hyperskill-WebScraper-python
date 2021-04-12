import string
import requests

from bs4 import BeautifulSoup

saved_articles = []
translator = str.maketrans(' ', '_', string.punctuation)

url = 'https://www.nature.com/nature/articles'
response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('article')

for article in articles:
    article_type = article.find("span", attrs={'data-test': 'article.type'}).text.strip()
    if article_type == 'News':
        article_details = article.find("a", attrs={'data-track-action': 'view article'})
        article_title = article_details.text
        article_link = 'https://www.nature.com' + article_details['href']
        article_filename = article_title.translate(translator).strip() + '.txt'
        article_response = requests.get(article_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        article_content = article_soup.find('div', class_='article__body').text.strip().encode()
        with open(article_filename, 'wb') as file:
            file.write(article_content)
            saved_articles.append(article_filename)

print(f"Saved articles:\n {saved_articles}")
