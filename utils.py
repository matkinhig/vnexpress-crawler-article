import json
import os
from datetime import datetime, timedelta
from typing import List

import arrow as arrow
import tqdm
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from type import ResultType

article_type_dict = {
    0: "thoi-su",
    1: "du-lich",
    2: "the-gioi",
    3: "kinh-doanh",
    4: "khoa-hoc",
    5: "giai-tri",
    6: "the-thao",
    7: "phap-luat",
    8: "giao-duc",
    9: "suc-khoe",
    10: "doi-song"
}

url_usi = "https://usi-saas.vnexpress.net/index/get?sort=like&is_onload=1"


# objectid=4562790&objecttype=1&siteid=1003231&categoryid=1003315


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def read_file(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line


def get_text_from_tag(tag):
    if isinstance(tag, NavigableString):
        return tag

    # else if isinstance(tag, Tag):
    return tag.text


def extract_content(url):
    return None


def write_content(result, output_fpath):
    if result is None:
        return False
    with open(output_fpath, "a", encoding="utf-8") as file:
        file.write("\n")
        file.write(result.url)
    return True


def get_urls_of_type(article_type, total_pages=5):
    articles_urls = list()
    for i in tqdm.tqdm(range(1, total_pages + 1)):
        content = requests.get(f"https://vnexpress.net/{article_type}-p{i}").content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="title-news")
        if len(titles) == 0:
            continue
        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))

    return articles_urls


def fetch_data(urls, number_of_article=20):
    listArticle: List[ResultType] = []
    compare_date = datetime.now() - timedelta(days=7)
    with tqdm.tqdm(total=len(urls)) as pbar:
        for url in urls:
            if url == "\n":
                pbar.update(1)
                continue
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("h1", class_="title-detail")
            if title is None:
                pbar.update(1)
                continue
            public_date_attr = soup.find("meta", itemprop="datePublished")
            if public_date_attr is None:
                pbar.update(1)
                continue
            public_date = datetime.strptime(public_date_attr.attrs.get("content")[:public_date_attr.attrs.get("content").find("T")], "%Y-%m-%d")
            if public_date < compare_date:
                pbar.update(1)
                continue
            data_fetch_comment = soup.find("div", class_="box_comment_vne")
            if data_fetch_comment is not None:
                comment_attr = json.loads(data_fetch_comment.attrs.get("data-component-input"))
                comments_response = requests.get(url_usi
                                                 + "&objectid=" + comment_attr.__getitem__("article_id")
                                                 + "&objecttype=1&siteid=" + comment_attr.__getitem__("site_id")
                                                 + "&categoryid=" + comment_attr.__getitem__("category_id")
                                                 + "&sign=" + comment_attr.__getitem__("sign"))
                error = comments_response.json().__getitem__("error")
                if error == 0:
                    comments = comments_response.json().__getitem__("data").__getitem__("items")
                    sum_like = 0
                    for comment in comments:
                        sum_like = sum_like + comment.__getitem__("userlike")
                    article = ResultType(title=title.text, url=url, total_like=sum_like,
                                         public_date=public_date)
                    listArticle.append(article)
            pbar.update(1)
    listArticle.sort(key=lambda x: x.total_like, reverse=True)
    return listArticle[:number_of_article]
