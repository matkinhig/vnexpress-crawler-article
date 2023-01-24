import argparse

import tqdm

from type import ResultType
from utils import create_dir, read_file, write_content, fetch_data, remove_file
from utils import get_urls_of_type, article_type_dict


def crawl_urls(urls_fpath="urls.txt", output_dpath="data", number_of_article=5):
    create_dir(output_dpath)
    remove_file("./results/top_comment.txt")
    urls = list(read_file(urls_fpath))
    # length of digits in an integer
    index_len = len(str(len(urls)))
    top_list: [ResultType] = []
    error_urls = list()
    list_by_url = fetch_data(urls, number_of_article)
    output_fpath = "".join([output_dpath, "/top_comment.txt"])
    for u in list_by_url:
        is_success = write_content(u, output_fpath)
        if not is_success:
            error_urls.append(u.url)
    return error_urls


def _init_dirs(output_dpath):
    create_dir(output_dpath)

    urls_dpath = "/".join([output_dpath, "urls"])
    results_dpath = "/".join([output_dpath, "results"])
    create_dir(urls_dpath)
    create_dir(results_dpath)

    return urls_dpath, results_dpath


def fetch_url(article_type, total_pages, urls_dpath, results_dpath, number_of_article):
    print(f"\n Crawl articles type {article_type}")
    error_urls = list()

    # get urls
    articles_urls = get_urls_of_type(article_type, total_pages)
    with open("./urls/all-link.txt", "a") as urls_file:
        urls_file.write("\n")
        urls_file.write("\n".join(articles_urls))


def crawl_all_types(total_pages, urls_dpath, results_dpath, number_of_article):
    total_error_urls = list()
    remove_file("./urls/all-link.txt")
    num_types = len(article_type_dict)
    for i in range(num_types):
        article_type = article_type_dict[i]
        fetch_url(article_type,
                  total_pages,
                  urls_dpath,
                  results_dpath,
                  number_of_article)
    error_urls = crawl_urls("./urls/all-link.txt", "./results", number_of_article)
    total_error_urls.extend(error_urls)

    return total_error_urls


def main(article_type, all_types=False, total_pages=5, output_dpath="data", number_of_article=10):
    urls_dpath, results_dpath = _init_dirs(output_dpath)
    error_urls = list()

    if all_types:
        error_urls = crawl_all_types(total_pages, urls_dpath, results_dpath, int(number_of_article))
    else:
        fetch_url(article_type,
                  total_pages,
                  urls_dpath,
                  results_dpath,
                  int(number_of_article))
    return error_urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VNExpress urls crawler by type")
    parser.add_argument("--articles",
                        default=5,
                        help="number of article",
                        dest="number_of_article")
    parser.add_argument("--type",
                        default="du-lich",
                        help="name of articles type",
                        dest="article_type")
    parser.add_argument("--all",
                        default=True,
                        action="store_true",
                        help="crawl all of types",
                        dest="all_types")
    parser.add_argument("--pages",
                        default=5,
                        type=int,
                        help="number of pages to crawl per type",
                        dest="total_pages")
    parser.add_argument("--output",
                        default="data",
                        help="saved directory path",
                        dest="output_dpath")

    args = parser.parse_args()

    main(**vars(args))
