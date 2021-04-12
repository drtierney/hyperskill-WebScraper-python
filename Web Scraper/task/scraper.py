import string
import os
import requests

from bs4 import BeautifulSoup

translator = str.maketrans(' ', '_', string.punctuation)

pages = int(input())
user_type = input()

for page_num in range(1, pages + 1):
    page_dir = f'Page_{page_num}'
    os.mkdir(page_dir)
    url = f'https://www.nature.com/nature/articles?page={page_num}'
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('article')

    for article in articles:
        article_type = article.find("span", attrs={'data-test': 'article.type'}).text.strip()
        if article_type == user_type:
            article_details = article.find("a", attrs={'data-track-action': 'view article'})
            article_title = article_details.text
            article_link = 'https://www.nature.com' + article_details['href']
            article_filename = article_title.translate(translator).strip() + '.txt'
            article_response = requests.get(article_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            article_body = article_soup.find('div', class_='article__body')
            article_item_body = article_soup.find('div', class_='article-item__body')
            article_content = article_body if article_body is not None else article_item_body
            with open(os.path.join(os.getcwd(), page_dir, article_filename), 'w', encoding='utf-8') as file:
                file.write(article_content.text.strip())

print("Saved all articles.")
