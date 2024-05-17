import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from urllib.parse import urlparse

#Проки при ip-бане (ошибка 429)

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

def scrape_and_save(url, file_path):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'google.com',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }

    response = requests.get(url, headers=headers)  # , proxies=proxies 
    soup = BeautifulSoup(response.text, 'html.parser')

    email_links = soup.find_all('div', class_='GyAeWb')
    links = set() 
    for div in email_links:
        spans = div.find_all('span')
        for span in spans:
            email_text = span.get_text()
            found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_text)
            for found_email in found_emails:
                domain = found_email.split('@')[1]
                site_email = f"info@{domain}"
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag.get('href')
                    if not href.startswith('/search') and 'google' not in href and not href.startswith('/preferences?') and not href.startswith('#'):
                        if domain in href:
                            links.add((site_email, href)) 

    # Записываем в CSV файл
    with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for email, link in links:
            csv_writer.writerow([email, link])

    if os.path.exists(file_path):
        if response.status_code==200:
            print('Успешная подгрузка файлов![+]')
            print('status code: ',response.status_code)
        elif response.status_code==429:
            print('Вы получили временную блокировку ip,попробуйте позже или используйте proxies')
    else:
        print('Не удалось создать csv файл.[-]')




repetitions = int(input("Введите количество повторений кода(чем больше число, тем больше результатов поиска): "))


current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'Emails.csv')


url = "https://www.google.ru/search?q=intext:info@&as_qdr=all&filter=0&num=100&start=100&complete=0&cr=countryRU"


for _ in range(repetitions):
    scrape_and_save(url, file_path)

print('Посмотрите файл в папке:', current_dir)
