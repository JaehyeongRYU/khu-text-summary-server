from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import TextClassificationPipeline
import torch
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Naver news 크롤링
newsUrl = "https://news.naver.com/main/ranking/popularDay.naver"
newsHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}


newsRes = requests.get(newsUrl, headers=newsHeaders)
soup = BeautifulSoup(newsRes.text, 'html.parser')
newsBox = soup.select(".rankingnews_box")
def load_news():
    newsResult = []
    for news in newsBox:
        newsName = news.select_one(".rankingnews_name").text
        # if newsName != '중앙일보' :
        #     continue
        # else:
        news_list = news.findAll("li")
        for li in news_list:
            list_title = li.select_one(".list_title")
            try: news_title = list_title.text
            except: news_title = None
            try: news_link = list_title.get("href")
            except: news_link = None
            content_html = requests.get(news_link, headers=newsHeaders)
            content_soup = BeautifulSoup(content_html.text, 'html.parser')
            news_content = content_soup.select_one("#newsct_article").text.replace("\n","").replace("\t","")
            if len(news_content.encode()) > 2000 :
                continue
            else :
                newsResult.append({'news_title':news_title ,'news_link':news_link,'news_content':news_content})

        if len(newsResult) == 5 :
            break
        else :
            continue
        
    return(newsResult)
        
# KoBART_PATH: hugging-face에 올라가 있는 모델 (https://huggingface.co/ryubro/myKoBARTSummary)
MODEL_PATH = "ryubro/myKoBARTSummary"

global loaded_model
global loaded_tokenizer

# KoBART model을 사용할 수 있게 만들어주는 함수
def load_kobart():
    global loaded_model
    global loaded_tokenizer

    # summarization을 위한 tokenizer와 model 로드
    loaded_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    loaded_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    

def text_organize(text):
    return text

# input: text => KoBART => output: summary_text
def make_summary(text):
    global loaded_tokenizer
    global loaded_model
    # 입력한 text에 대한 model의 요약본 추출
    if text:
        input_ids = loaded_tokenizer.encode(text)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        output = loaded_model.generate(input_ids, eos_token_id=1, max_length=1024, num_beams=5)
        output = loaded_tokenizer.decode(output[0], skip_special_tokens=True)
        
    return output

@app.route('/news', methods=['GET'])
def loadNews():
    result = load_news()
    return (result)


@app.route('/summary', methods=['POST'])
def summary():
    # POST 요청에서 질문(question) 가져오기
    text = request.get_json()['text']
    # input: question => BERT => output: feel_list
    summarized_text = make_summary(text)
    # input: question+feel => GPT => output: answer
    return jsonify({'result': summarized_text})


if __name__ == '__main__':
    # KoBART model 로드
    load_kobart()
    # Naver news 로드
    loadNews()
    # Flask 애플리케이션 실행
    app.run(host='0.0.0.0')