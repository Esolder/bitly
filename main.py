import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def main():
    load_dotenv()
    token = {'Authorization': os.getenv('BITLY_TOKEN')}
    user_link = create_parser().parse_args().link
    if is_bitlink(token, user_link):
        try:
            total_clicks = get_total_clicks(token, user_link)
        except requests.exceptions.HTTPError as error:
            print(error)
        else:
            print('Количество переходов по ссылке битли:', total_clicks)
    else:
        try:
            bitlink = get_bitlink(token, user_link)
        except requests.exceptions.HTTPError as error:
            print(error)
        else:
            print(bitlink)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Ссылка')
    return parser


def is_bitlink(token, user_link):
    url_parts = urlparse(user_link)
    bitly_url = 'https://api-ssl.bitly.com/v4/expand'
    link = f'{url_parts.netloc}{url_parts.path}'
    bitlink_id = {'bitlink_id': link}
    response = requests.post(bitly_url, headers=token, json=bitlink_id)
    return response.ok


def get_bitlink(token, user_link):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    long_url = {'long_url': user_link}
    response = requests.post(bitly_url, headers=token, json=long_url)
    response.raise_for_status()
    return response.json()['link']


def get_total_clicks(token, user_link):
    url_parts = urlparse(user_link)
    bitlink = f'{url_parts.netloc}{url_parts.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    params = {'unit': 'month'}
    response = requests.get(url, headers=token, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    main()
