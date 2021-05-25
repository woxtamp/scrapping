import requests
from bs4 import BeautifulSoup
import re
import time

URL = 'https://habr.com/ru/all/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def get_data_from_url(address):
    response = requests.get(address)
    if response.status_code == 200:
        text = response.text
        soup = BeautifulSoup(text, features='html.parser')
        return soup
    else:
        print(f'Произошла ошибка! Адрес {address} недоступен')


def read_articles_preview_by_hub(address, hubs_set):
    articles_header_list = []
    soup = get_data_from_url(address)
    articles = soup.find_all('article')
    for article in articles:
        hubs = {h.text.lower() for h in article.find_all('a', class_='hub-link')}
        hubs_set_lower = {element.lower() for element in hubs_set}
        if hubs_set_lower & hubs:
            date = article.find('span', class_='post__time')
            header = article.find('a', class_='post__title_link')
            link = article.find('a', class_='post__title_link').attrs.get('href')
            articles_header_list += header.text
            print(f'Совпадение по {list(hubs_set_lower & hubs)}:\n{date.text} (МСК) - {header.text} - {link}\n')
    if len(articles_header_list) == 0:
        print(f'Произошла ошибка! Для хабов {list(KEYWORDS)} нет упоминаний в последних 20 статьях.')


def read_article_content_by_hub(address, hubs_set):
    hub_count_list = []
    soup = get_data_from_url(address)
    articles = soup.find_all('article')
    for article in articles:
        time.sleep(1)
        link = article.find('a', class_='post__title_link').attrs.get('href')
        soup = get_data_from_url(link)
        header = soup.find('span', class_='post__title-text').text
        article = soup.find('div', id='post-content-body').text.lower()

        hubs_set_lower = {element.lower() for element in hubs_set}
        for hub in hubs_set_lower:
            if re.findall(f'{hub}', article):
                hub_count_list += [hub]
        if len(hub_count_list) > 0:
            print(f'В статье "{header}"({link})\nнайдены совпадения для следующих хабов: '
                  f'{hub_count_list}\n')
        else:
            print(f'В статье "{header}"({link})\nне найдено совпадений для хабов: '
                  f'{KEYWORDS}\n')
        hub_count_list = []


if __name__ == '__main__':
    while True:
        print('Привет!\nЭта программа позволяет искать ключевые слова (хабы) по списку последних статей на сайте '
              f'habr.com.\nСейчас список хабов вот такой: {KEYWORDS}.\nВведи команду "1" чтобы искать '
              f'по превьюшкам статей.\nВведи команду "2" чтобы искать по тексту всех статей целиком.\n'
              f'Введи "0" чтобы выйти\n')
        user_input = (input('Введи команду: ')).lower()
        if user_input == '1':
            read_articles_preview_by_hub(URL, KEYWORDS)
            break
        elif user_input == '2':
            read_article_content_by_hub(URL, KEYWORDS)
            break
        elif user_input == '0':
            break
        else:
            print('Неверная команда!')
