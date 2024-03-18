"""
This python file is a combination of main.py and urls_from_website.py.
This file was created as an attempt for chrome extension
"""
from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import urlparse
import matplotlib.pyplot as plt

def scrap_urls(main_url, domain_name):
    response = requests.get(main_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    urls_to_be_added = []
    for link in links:
        href = link.get("href")
        if href and domain_name in href:
            urls_to_be_added.append(href)
    # print(urls_to_be_added)
    return urls_to_be_added


def run_initial_url():
    f = open("InitialURL.txt", "r")
    url_list = []
    for url in f.readlines():
        url_list.append(url)
    f.close()
    domain = urlparse(url_list[0]).netloc  # Include the links within the actual website only

    for url in url_list:
        initial_count = len(url_list)
        new_urls = scrap_urls(url, domain)
        for ele in new_urls:
            url_list.append(ele)
        url_list = list(set(url_list))  # This step removes duplicates from the list
        add_count = len(url_list)
        if initial_count == add_count:
            break

    f = open("urlsfile.txt", "w")
    for url in url_list:
        f.write(url)
        f.write('\n')
    f.close()

    return url_list

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url_list = run_initial_url()
    # we are using request package to make a GET request for the website, which means we're getting data from it.

    topics = [' modi ', 'bjp', ' lotus ', ' politics ', 'namo', ' narendra modi', ' saffron ', ' right wing ', 'nda']
    sentiment = SentimentIntensityAnalyzer()
    scores = []
    count = 0
    for url in url_list:
        #print("URL: ", url)
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, features="lxml")
            results = soup.find_all('p')[1]
            p1 = results.text.lower()
            if [p1.find(ele) for ele in topics]:
                sent1 = sentiment.polarity_scores(p1)
                scores.append(sent1["compound"])
                count = count +1
                if count == 100: break
        except:
            continue

    plt.hist(scores)
    plt.show()
