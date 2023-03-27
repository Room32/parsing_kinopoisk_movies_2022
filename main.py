import random

import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time

keys_list = ['название', 'оригинальное название', 'продолжительность', 'страна', 'жанр', 'режиссёр']
title_list = []
original_title_list = []
duration_list = []
country_list = []
genre_list = []
directors_list = []
dict = {}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'cookie': 'gdpr=0; yandex_login=; yuidss=6191471621678384220; location=1; mobile=no; mda_exp_enabled=1; crookie=jNsgGFMcf0uSvBRh3sdxM4klUXalWjqnctbymxh5+/0kjYb9LNq8jKehi5+RXjbXg6uqzxttEGbMluRQrgfBFUJwyeQ=; cmtchd=MTY3OTE1MjQyMTMwMg==; coockoos=4; desktop_session_key=7450e0e702923abeedd08dc989b195a61c092fdff9b654c9b43769a8cd201d49ebd9c1f4204ec31a0844ca1e0eecf9e4495abb21a12b44d3e0c30fe064b42cdfa9452c52a0c5dab260299fad74dc30562fbaff0ee9c711ea35b7063174f67dd9; desktop_session_key.sig=X_UkTJCptE_K7JXEPU3h8qiX6Qw; _ym_isad=1; yp=1679742241.yu.6191471621678384220; ymex=1682247841.oyu.6191471621678384220; PHPSESSID=281db70b42b21df40bbbd5bcdfe2d993; yandex_gid=21341; tc=1; _csrf_csrf_token=fXf4uIUDvvRRLY2Da1IA0jZXpT1EkB7Jv-NorbyVrJo; _csrf=xANMKC15e8HvkEtcMHryMAm4; _ym_uid=1599908632191190302; _yasc=zwvxSveF0rr2Kgqp78PDwBzqinAm6FZNMwdlwK/MxOfC1BP8J5YqCtVk3unqkmc=; disable_server_sso_redirect=1; sso_status=sso.passport.yandex.ru:synchronized; ya_sess_id=noauth:1679671639; ys=c_chck.1006265624; yandexuid=9707451371679671639; mda2_beacon=1679671639429; i=m4NAxdYxeYYoBECGQ44NBUPKYC3EHLIvPQd4DBIzDsfi/IhnhU852G25jK5yUsQ6kZlQY9tiVxdpWDAIwrZsLf3H4M0=; _ym_d=1679671680',
            'referer': 'https://sso.kinopoisk.ru/'
           }


def download_html():
    try:
        response = requests.get(url, headers=headers).text

        with open('kinopoisk.html', 'w', encoding='utf-8') as file:
            file.write(response)
    except Exception as ex:
        print(f'КАЖЕТСЯ ЧТО-ТО НЕ ПОЛУЧИЛОСЬ :(\n{ex}')


def parsing():

    with open('kinopoisk.html', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')
    movie_blocks = soup.find_all('div', class_='styles_root__ti07r')

    for movie_block in movie_blocks:
        country_span = movie_block.find_next('span', class_='desktop-list-main-info_truncatedText__IMQRP')
        country = country_span.text if country_span else 'none'

        if country.split('•')[0].strip() == 'Россия'or country.split('•')[0].strip() == 'Беларусь':
            pass
        else:
            label_span = movie_block.find_next('span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj')
            label = label_span.text if label_span else 'none'

            original_label_span = movie_block.find_next('span', class_='desktop-list-main-info_secondaryTitle__ighTt')
            original_label = original_label_span.text if original_label_span else 'none'

            duration_span = movie_block.find_next('span', class_='desktop-list-main-info_secondaryText__M_aus')
            duration = duration_span.text if duration_span else 'none'

            if country == 'none':
                genre = 'none'
            else:
                genre = country.split('•')[-1].strip().split()[0]
            if country == 'none':
                director = 'none'
            else:
                director_list = country.split('•')[-1].strip().split()[1:]
                director = ' '.join(director_list)

            title_list.append(label)
            original_title_list.append(original_label)
            duration_list.append(duration.split(',')[-1].strip())
            country_list.append(country.split('•')[0])
            genre_list.append(genre)
            directors_list.append(director.split(':')[-1].strip())

    time.sleep(random.randint(2, 5))


if __name__ == '__main__':
    page = 1
    while page < 671:
        url = f'https://www.kinopoisk.ru/lists/movies/year--2022/?page={page}'
        download_html()
        parsing()
        print(f'[INFO]: загрузил страницу {page}')
        page += 1

    dict[keys_list[0]] = title_list
    dict[keys_list[1]] = original_title_list
    dict[keys_list[2]] = duration_list
    dict[keys_list[3]] = country_list
    dict[keys_list[4]] = genre_list
    dict[keys_list[5]] = directors_list

    df = pd.DataFrame(dict)
    df.to_csv('movies_list.csv', encoding='utf-8')
    print('КАЖЕТСЯ ВСЁ...')