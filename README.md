# seulsegown



## ⭐️ 프로젝트 주제 : 내가 사는 곳은 슬세권🩴인가?
<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236002002-13ca2ac0-cb85-4467-812d-1f8f3350f6cd.png" width="600" height="850"/>

<br></br>
## ⭐️ 프로젝트 개요
### 1. 내용
슬세권 프로젝트는 1~2인 가구가 증가하면서 생긴 신조어인 [슬세권](https://namu.wiki/w/%EC%8A%AC%EC%84%B8%EA%B6%8C)에서 착안한 위치기반 서비스로,<br>
생활 반경 내 편의점 분포를 통해 거주 지역의 생활 편의성 점수를 매겨주는 프로젝트입니다.


### 2. 기간 : 2023. 5. 1. ~ 2023. 5. 5.

### 3. 팀원
|이름|역할|
|:---:|:---:|
|김수민|크롤러, 백엔드|
|김형준|크롤러, 프론트|
|서대원|크롤러, 백엔드|
|안수빈|크롤러, 프론트|
|이수영|크롤러, 백엔드|

### 4. 기술스택
- Back-end : Python, Django
- DB : SQLite
- Crawler : Selenium, BeautifulSoup, Requests
- Front-end : CSS, Javascript, JQuery
- Common : Slack, GitHub, Figma

<br></br>
## ⭐️ 프로젝트 설치 및 실행방법


1. 상단의 Code 버튼을 눌러 경로를 복사한 후, 레포지토리를 복제합니다.
   ```sh
   git clone https://github.com/my-sleeper-town/seulsegown.git
   ```
2. 프로젝트 폴더로 경로를 이동합니다.
    ```sh
   cd seulsegown
   ```
3. 패키지를 설치합니다.
   ```sh
   pip install -r requirements.txt
   ```
4. DB를 마이그레이트합니다.
   ```sh
   python manage.py migrate
   ```
5. 카카오 개발자페이지에서 REST API 키를 발급받습니다. [https://developers.kakao.com/](https://developers.kakao.com/)

6. 발급받은 API 키를 환경변수로 저장합니다.
   ```sh
   export KAKAO_TOKEN="발급받은 키"
   ```
7. django mangement 명령어를 통해 편의점 데이터를 다운받습니다. 
   ```sh
   python manage.py crawl --all
   ```
   - 키워드를 통해 특정 브랜드의 편의점만 데이터만 다운받을 수도 있습니다.
   - cu, emart24, ministop, seveneleven, gs25
   ```sh
   python manage.py crawl --brand [brand_name]
   ```
8. 명령어를 통해 서버를 실행합니다. 
   ```sh
   python manage.py runserver
   ```


<br></br>

## ⭐️ 평가 점수 계산 방식
 

슬세권 점수는 편의점 개수 X 거리 점수로 합산합니다.<br>
거리 점수는 편의점의 위치에 따라 200m 이내는 3점, 300m는 2점, 400m는 1점으로 계산합니다.<br>
만점은 10점이며, 만점을 넘은 점수는 모두 10점으로 표기합니다.

|거리|점수|
|:---:|:---:|
|200m|3점|
|300m|2점|
|400m|1점|

<br></br>

## ⭐️ resources

- a illustration clip by [Loose Drawing](https://loosedrawing.com/terms/)

<br></br>

## ⭐️ 프로젝트 진행 과정
### 1️⃣ 프로젝트 구조
<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236000654-a85dc143-3507-40e2-94ba-184b5e8d929d.png" width="800" height="600"/>
<br></br>

### 2️⃣ 데이터 모델링
<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236000480-36b2d7eb-e0c2-4eb4-bf8b-2f5aa1a9afcf.png" width="700" height="400"/>
<br></br>

### 3️⃣ Flow Chart
<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236001750-ac2e3357-cbfc-4214-9e3f-122e3717e8c7.png" width="700" height="400"/>
