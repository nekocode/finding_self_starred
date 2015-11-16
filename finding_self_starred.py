#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import requests
from bs4 import BeautifulSoup
__author__ = 'nekocode'

BASE_URL = 'https://github.com'
STARRED_URL = BASE_URL + '/stars/%s'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
HEADERS = {"User-Agent": UA}


def get_self_starred_repos(account):
    url = STARRED_URL % account
    repos = []

    while True:
        req = requests.get(url, headers=HEADERS, timeout=20)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, "html.parser")

        repo_list = soup.select('.repo-list-item')
        for item in repo_list:
            repo_master = item.select('.repo-list-name .prefix')[0].text

            if account == repo_master:
                repo = dict()
                repo['name'] = "".join(item.select('.repo-list-name a')[0].text.split())
                repo['url'] = BASE_URL + item.select('.repo-list-name a')[0]['href']
                repo['description'] = item.select('.repo-list-description')[0].text.strip()
                repos.append(repo)

        paginations = soup.select('.pagination a')
        if len(paginations) == 0:
            break

        has_next = False
        for pagination in paginations:
            if pagination.text == 'Next':
                # 翻页
                url = pagination['href']
                has_next = True

        if not has_next:
                break;

    return repos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('account', help="Finding one's own repositories which are self-starred.", type=str)
    name = parser.parse_args().account
    rlt = get_self_starred_repos(name)

    for item in rlt:
        print '=' * 30
        print item['name'] + '\n' + item['description'] + '\n' + item['url']
        print '=' * 30 + '\n\n'

