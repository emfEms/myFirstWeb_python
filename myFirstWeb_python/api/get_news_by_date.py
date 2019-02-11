from selenium import webdriver
import requests
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import *
from matplotlib import *
import matplotlib.pyplot as plt
from wordcloud import *


def removeSlash(URL):
    while URL[0] == '/':
        URL = URL[1:]
    return URL

def checkHttp(URL):
    if URL[0] == '/':
        URL=('http:'+URL)
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
            text =clean_text(text)
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
    elif 'shinailbo.co.kr' or 'dtnews24.com' or 'idjnews.kr' or 'ggilbo.com'in URL:
        for item in soup.find_all('div', id='article-view-content-div'):
            text = text + str(item.find_all("p"))
            text = clean_text(text)
            word_Cloud_Text += text
    elif 'asiatoday.co.kr'in URL:
        for item in soup.find_all('div', id='font'):
            text = text + str(item.find_all(text=True))
            text = clean_text(text)
            word_Cloud_Text += text
    elif 'newsworker.co.kr'in URL:
        for item in soup.find_all('div', {'class':'articleBody'}):
            text = text + str(item.find_all(text=True))
            text = clean_text(text)
            word_Cloud_Text += text
    elif 'breaknews.com'in URL:
        for item in soup.find_all('div', id='CLtag'):
            text = text + str(item.find_all(text=True))
            text = clean_text(text)
            word_Cloud_Text += text
    elif 'wikitree.co.kr' in URL:
        for item in soup.find_all(class_='article_body'):
            text = text + str(item.find_all(text=True))
            text = clean_text(text)
            word_Cloud_Text += text
    else :
        for item in soup.find_all('div', id='articleBody'):
            text = text + str(item.find_all(text=True))
            text = clean_text(text)
            word_Cloud_Text += text
        # for item in soup.find_all(class_='article_body'):
        #     text = text + str(item.find_all(text=True))
        #     text = clean_text(text)
        #     word_Cloud_Text += text

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
search.send_keys('악취')
search.submit()

driver.find_element_by_class_name('lnb4').click()
driver.find_element_by_id('_search_option_btn').click()
driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[2]').click()
driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').click()
driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys('2019')
driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys('0128')
driver.find_element_by_xpath('//*[@id="news_input_period_end"]').click()
driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys('2019')
driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys('0128')
driver.find_element_by_xpath('//*[@id="_nx_option_date"]/div[2]/span/button').click()

url_list = []

get_news_url(url_list)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ1페이지 끝(총 10개출력)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
driver.find_element_by_class_name('next').click()

get_news_url(url_list)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ2페이지 끝(총 20개출력)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

driver.find_element_by_class_name('next').click()

get_news_url(url_list)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ3페이지 끝(총 30개출력)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

driver.find_element_by_class_name('next').click()

get_news_url(url_list)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ4페이지 끝(총 40개출력)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

driver.find_element_by_class_name('next').click()

get_news_url(url_list)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ5페이지 끝(총 50개출력)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

word_Cloud_Text = ''

for i in range(0,50):
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

# print(url_list)
print(word_Cloud_Text)
spliter = Okt()  # konlpy의 Okt
nouns = spliter.nouns(word_Cloud_Text) # nouns 함수를 통해서 text에서 명사만 분리/추출
count = {}
for i in nouns:
    wordCnt = nouns.count(i);  # 단어가 나온 횟수를 Count
    count[i] = wordCnt

# print(count)

f = open("wordCloud.txt",'w',encoding='utf8')
f.write(word_Cloud_Text)
f.close()

from PIL import Image
import numpy as np

alice_mask = np.array(Image.open("korea.png"))

wordcloud = WordCloud(
    font_path ='NanumBarunGothic.ttf',
    width = 800,
    height = 800,
    background_color="white",
    mask = alice_mask,
    max_words=200
)

wordcloud = wordcloud.generate_from_frequencies(count)
plt.figure(figsize=(40, 40))
plt.imshow(wordcloud, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
# plt.show()
plt.savefig('wordcloud_image_generated_korea.png')
