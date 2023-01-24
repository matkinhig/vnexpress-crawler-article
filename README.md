# VN Express article crawler
[![Python 3.10.7](https://img.shields.io/badge/python-3.10.7-blue)](https://www.python.org/downloads/release/python-3107/)[![BeautifulSoup 0.0.1](https://img.shields.io/badge/BeautifulSoup-0.0.1-purple)](https://pypi.org/project/bs4/)[![Requests 2.28.1](https://img.shields.io/badge/Requests-2.28.1-black)](https://pypi.org/project/requests/)[![tqdm 4.64.1](https://img.shields.io/badge/tqdm-4.64.1-orange)](https://pypi.org/project/tqdm/)   
Crawling titles and paragraphs of VN Express articles using their URLs or categories names 

## Installation
Create virtual environment then install required packages:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
### Crawl article by top comment
To crawl article in a single type, you must provide number of article in `--articles` flag 
For example if you run below command:  
```bash
python types_crawler.py --articles=3 --output=.
```
## Todo
- [ ] Add logging module
- [ ] Crawl in other news websites