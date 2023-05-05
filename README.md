# seulsegown

## ⭐️ 프로젝트 주제 : 내가 사는 곳은 슬세권🩴인가?

<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236002002-13ca2ac0-cb85-4467-812d-1f8f3350f6cd.png" width="600" height="850"/>

## ⭐️ 프로젝트 개요

- 기간: 2023. 05. 01. ~ 2023. 05. 05.
- 팀원: 김수민, 김형준, 서대원, 안수빈, 이수영

## ⭐️ 프로젝트 시작법

```bash
# 저장소 클론
$ git clone https://github.com/my-sleeper-town/seulsegown.git
$ cd seulsegown

# 의존성 설치
$ pip install -r requirements.txt

# API 키 등록
$ export KAKAO_API='kakao_api_token'

# DB 마이그레이션
$ python manage.py migrate

# 편의시설 정보 크롤링
$ python manage.py crawl --all

# 서버 실행
$ python manage.py runserver

# localhost:8000 접속하여 확인
```

## ⭐️ resources

- a illustration clip by [Loose Drawing](https://loosedrawing.com/terms/)

## ⭐️ 프로젝트 구조도

### 1️⃣ 프로젝트 구조

<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236000654-a85dc143-3507-40e2-94ba-184b5e8d929d.png" width="800" height="600"/>

### 2️⃣ 데이터 모델링

<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236000480-36b2d7eb-e0c2-4eb4-bf8b-2f5aa1a9afcf.png" width="700" height="400"/>

### 3️⃣ Flow Chart

<p align="center"><img src="https://user-images.githubusercontent.com/54103240/236001750-ac2e3357-cbfc-4214-9e3f-122e3717e8c7.png" width="700" height="400"/>
