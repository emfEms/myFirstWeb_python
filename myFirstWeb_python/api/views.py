from django.shortcuts import render
from django.utils import timezone
from .models import Post

from selenium import webdriver
import requests
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import *
from matplotlib import *
import matplotlib.pyplot as plt
from wordcloud import *
import operator

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'api/post_list.html', {'posts' : posts})

def post_list3(request):
    return render(request, 'api/html_test.html',{})


def post_list2(request):
    search_key = request.GET['search_key']
    startYear = request.GET['startYear']
    startMonthAndDay = request.GET['startMonthAndDay']
    endYear = request.GET['endYear']
    endMonthAndDay = request.GET['endMonthAndDay']

    def removeSlash(URL):
        while URL[0] == '/':
            URL = URL[1:]
        return URL

    def checkHttp(URL):
        if URL[0] == '/':
            URL = ('http:' + URL)
        return URL

    # 클리닝 함수
    def clean_text(text):
        cleaned_text = re.sub('[a-zA-Z]', '', text)
        cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                              '', cleaned_text)
        return cleaned_text

    # 크롤링 함수
    def get_text(URL):
        source_code_from_URL = urllib.request.urlopen(URL)
        soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
        text = ''
        word_Cloud_Text = ''

        if 'news.naver.com' in URL:
            for item in soup.find_all('div', id='articleBodyContents'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'naeil.com' in URL:
            for item in soup.find_all('div', id='contents'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'ajunews.com' or 'newstown.com' or 'ccnnews.co.kr' or 'anewsa.com' or 'ikpnews.net' in URL:
            for item in soup.find_all('div', id='articleBody'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'shinailbo.co.kr' or 'dtnews24.com' or 'idjnews.kr' or 'ggilbo.com' in URL:
            for item in soup.find_all('div', id='article-view-content-div'):
                text = text + str(item.find_all("p"))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'asiatoday.co.kr' in URL:
            for item in soup.find_all('div', id='font'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'newsworker.co.kr' in URL:
            for item in soup.find_all('div', {'class': 'articleBody'}):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'breaknews.com' in URL:
            for item in soup.find_all('div', id='CLtag'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text
        elif 'wikitree.co.kr' in URL:
            for item in soup.find_all(class_='article_body'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
        else:
            for item in soup.find_all('div', id='articleBody'):
                text = text + str(item.find_all(text=True))
                text = clean_text(text)
                word_Cloud_Text += text

        return text

    def get_news_url(url_list):
        url = driver.current_url  # 악취 키워드로 검색했을때 url을가져옴

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        for i in range(1, 150):
            my_titles2 = soup.select('#sp_nws%d > dl > dt > a' % i)

            for title in my_titles2:
                print(title.text)
                print(title.get('href'))
                url_list.append(title.get('href'))

    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(1)
    driver.get('http://naver.com')
    search = driver.find_element_by_id('query')
    #search.send_keys('악취+환경')
    search.send_keys(search_key)
    search.submit()

    driver.find_element_by_class_name('lnb4').click()
    driver.find_element_by_id('_search_option_btn').click()
    driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[2]').click()
    driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').click()
    # driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys('2019')
    # driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys('0128')
    driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys(startYear)
    driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys(startMonthAndDay)
    driver.find_element_by_xpath('//*[@id="news_input_period_end"]').click()
    # driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys('2019')
    # driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys('0131')
    driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys(endYear)
    driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys(endMonthAndDay)
    driver.find_element_by_xpath('//*[@id="_nx_option_date"]/div[2]/span/button').click()

    url_list = []

    get_news_url(url_list)
    driver.find_element_by_class_name('next').click()
    get_news_url(url_list)
    driver.find_element_by_class_name('next').click()
    get_news_url(url_list)
    driver.find_element_by_class_name('next').click()
    get_news_url(url_list)
    driver.find_element_by_class_name('next').click()
    get_news_url(url_list)
    word_Cloud_Text = ''

    for i in range(0, 50):
        URL = url_list[i]
        URL = checkHttp(URL)
        html = urlopen(URL)
        bsObject = BeautifulSoup(html, "html.parser")
        result_text = get_text(URL)
        word_Cloud_Text += result_text

        spliter = Okt()  # konlpy의 Okt
        nouns = spliter.nouns(result_text)  # nouns 함수를 통해서 text에서 명사만 분리/추출
        count = {}
        for i in nouns:
            wordCnt = nouns.count(i);  # 단어가 나온 횟수를 Count
            count[i] = wordCnt

        print(count)
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    # print(url_list)
    # print(word_Cloud_Text)
    spliter = Okt()  # konlpy의 Okt
    nouns = spliter.nouns(word_Cloud_Text)  # nouns 함수를 통해서 text에서 명사만 분리/추출
    count = {}
    for i in nouns:
        wordCnt = nouns.count(i);  # 단어가 나온 횟수를 Count
        count[i] = wordCnt


    news_list = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    # for key,value in d.items():
    #     print("%s: %s" %(key,value))

    from PIL import Image
    import numpy as np

    alice_mask = np.array(Image.open("korea.png"))

    wordcloud = WordCloud(
        font_path='NanumBarunGothic.ttf',
        width=800,
        height=800,
        background_color="white",
        mask=alice_mask,
        max_words=200
    )

    wordcloud = wordcloud.generate_from_frequencies(count)
    plt.figure(figsize=(40, 40))
    plt.imshow(wordcloud, cmap=plt.cm.gray, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig('wordcloud_image_generated_korea.png')

    return render(request, 'api/get_list.html', {'startYear': startYear, 'startMonthAndDay' : startMonthAndDay,
                                                 'search_key':search_key,'endYear' : endYear, 'endMonthAndDay' : endMonthAndDay, 'news_list': news_list})



