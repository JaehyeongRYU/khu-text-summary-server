# NLP Model Server
**이 프로젝트는 자연어 처리(NLP) 모델을 활용한 웹 서비스를 제공한다.** `Flask` framework를 사용하여 구축되었으며, `fine-tuned KoBART` 모델을 통해 텍스트를 읽기 쉽게 요약하는 기능을 제공한다. 이를 통해 사용자는 긴 글을 입력하고, 해당 글에 대한 AI 기반의 요약 응답을 받을 수 있다.

<br>

## 기능
* **텍스트 요약**: 입력된 글에 대한 요약물 추출을 수행한다. `fine-tuned KoBART`를 사용하여 텍스트 요약 모델을 구현하였으며, pretrained model을 활용한다.
* **네이버 뉴스 크롤링**: 네이버 뉴스 랭킹에서 5개의 기사 제목, 내용, 링크들을 크롤링해온다. 해당 데이터는 뉴스 요약을 위해 사용된다.

<br>

## 2. 파일 구조
```
app
 ├── app.py
.gitignore
README.md
requirements.txt
```
* `app`: 애플리케이션 폴더
  * `app.py`: Flask application의 메인 파일. 웹 서비스의 endpoint와 핵심 기능이 구현되어 있다.
* `.gitignore`: Git으로 관리하지 않을 file 및 directory를 명시한 파일.
* `README.md`: 현재 문서
* `requirements.txt`: 프로젝트에 필요한 Python package들과 version 정보를 명시한 파일.

<br>

## 3. 사용 
1. 필요한 Python 패키지들을 설치하기 위해 다음 명령을 실행한다.
```
pip install -r requirements.txt
```

3. Flask application을 실행한다.
```
python app/app.py
```
4. Web browser에서 `http://localhost:5000` 으로 접속하여 NLP model service를 이용할 수 있다.
