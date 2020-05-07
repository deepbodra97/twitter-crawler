from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

import time
import math
from textblob import TextBlob


def index(request):
    return render(request, 'crawl/index.html')


def search(request):

    if request.method == 'GET':
        q = request.GET.get('q')
        tweets = get_n_tweets(5, q)
        return render(request, 'crawl/result.html', {'tweets': tweets})

    else:
        return HttpResponse('You must send a GET request only')


def get_n_tweets(n, search_str='COVID 19'):
    response = []
    twitter_listener = TwitterListener(n)
    ff_driver = webdriver.Firefox(executable_path='geckodriver.exe')
    driver = EventFiringWebDriver(ff_driver, twitter_listener)
    driver.get("http://twitter.com/search?q=" + search_str + "&src=typd")
    driver.execute_script("window.scrollTo(0, 0);")
    return twitter_listener.tweets


class TwitterListener(AbstractEventListener):

    def __init__(self, num_tweets_to_scrape):
        self.tweets = []
        self.num_tweets_to_scrape = num_tweets_to_scrape

    def after_execute_script(self, url, driver):
        css_selector_tweet_container = "div[class='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o']"
        css_selector_tweet_fullname = "div>span[class='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']"
        css_selector_tweet_text = "div[class='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0']"

        while len(self.tweets)<self.num_tweets_to_scrape:
            time.sleep(20);
            e_tweets = driver.find_elements(By.CSS_SELECTOR, css_selector_tweet_container)
            for e_tweet in e_tweets:
                e_fullname = e_tweet.find_element(By.CSS_SELECTOR, css_selector_tweet_fullname)
                e_tweet_text = e_tweet.find_element(By.CSS_SELECTOR, css_selector_tweet_text)
                self.tweets.append({'by': e_fullname.text,
                                    'tweet': e_tweet_text.text,
                                    'score': TextBlob(e_tweet_text.text).sentiment.polarity})
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")