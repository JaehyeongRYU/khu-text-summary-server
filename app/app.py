from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import TextClassificationPipeline
import torch

app = Flask(__name__)
CORS(app)

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
        output = loaded_model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
        output = loaded_tokenizer.decode(output[0], skip_special_tokens=True)
        
    return output



# input: summarized_text => output: 요약된 텍스트 정리..?
def generate_answer(text):
    # need Something

    return text


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
    # Flask 애플리케이션 실행
    app.run(host='0.0.0.0')