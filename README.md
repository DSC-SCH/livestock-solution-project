# 한우 평균 경매금액 예측 앱 서비스
- 본 프로젝트의 최종적인 결과물은 한우 평균 경매금액을 예측하는 동시에 축산농가와 예비축산인들이 서로 소통할 수 있는 커뮤니티를 제공하는 모바일 앱 서비스 입니다.

- 하지만 <strong>이 레포지토리에서는 한우 평균 경매금액을 예측하는 모델링에 대한 내용만을 포함하고 있습니다.</strong>

## 0. 프로젝트 참여 멤버
- 데이터 분석, 예측 모델링
  * 박성아(Seong A Park)
  * 조영훈(Young Hun Jo)

- 백엔드 개발
  * 홍나단(Nathan Hong)
  * 유지민(Jimin U)

- 프론트 개발
  * 황상범(Sang Beom Hwang)

- 앱 디자이너
  * 김유나(You Na Kim)

## 1. 문제 정의
- 1주일 후의 한우 평균 경매금액을 예측하는 모델링

## 2. 문제의 필요성
- 한우 경매 책정금액에 대한 정보가 부족한 축산농가에게 예측된 평균 경매금액 정보를 제공함으로써 축산농가의 생산성 향상과 경영안정을 도모하기 위함

## 3. 사용된 변수 데이터
- 기본적으로 하단의 모든 데이터들은 2001년 01월 01일부터 최근날짜의 시계열 데이터
- 최근날짜의 데이터를 지속적으로 수집하기 위해 작업 스케줄러를 설정해 매주 토요일에 사용된 모든 시계열 데이터 크롤링 자동화 설정해준 상태
- 데이터 명세서
  1. 종관기상관측일자료 데이터(지역별로 평균기온, 최고기온, 최저기온, 일강수량, 합계 일조시간, 최대 순간 풍속, 최대 풍속, 합계 일사, 평균 지면 온도, 최소 상대 습도, 평규 상대 습도, 1시간 최대알사량, 평균 풍속)
  2. 축산물 실시간 경매시황중계정보 데이터
      * 지육상장을 제외한 한우가격 데이터 사용
  3. 축산물 실시간 경매시황중계정보 데이터에서 파생되어 나온 lag 데이터

## 4. 변수 선정 이유
- 종관기상관측일자료 데이터 : 한우 경매금액 책정에 있어서 중요한 기준 중 하나는 한우의 상태이다. 
한우의 상태는 한우가 성장하는 환경과 직접 연결되어 있다. 환경은 날씨 상태에 따라 크게 좌우되기 때문에 기상관측 자료를 선택했다.


## 📂 Directory structure
``` 
  |-FeatureEngineering           
  |  |-02-1. feature 선택-참고용.ipynb               # feature 선택하는 코드 
  |  |-02. 파생변수 생성.ipynb            # 모델 적용 전 파생변수를 생성하는 코드 
  |  |-03.resetting_feature_y.ipynb       # 목적에 맞게 y를 재설정하는 코드 
  |  |-data_collect_saturday.py               # 매주 토요일마다 정기적으로 데이터 수집 후 DB에 저장하는 코드 
  |  |-hanwoo_price_collection.py     # 한우 가격을 전처리한 후 DB에 저장하는 코드 
  |  |-week_price.py      # 주별 데이터로 변환한 후 DB에 저장하는 코드
  |
  |-Modeling
  |  |-04. 모델링.ipynb                      # feature를 바꿔가며 MLP 모델을 적용하는 코드 
  |  |-ARIMA.ipynb              # arima 모델을 적용하는 코드 
  |  |-LSTM_organized.ipynb       # LSTM 양방향 모델을 적용하는 코드 
  |  |-model.py                         # DB 에서 데이터를 추출하여 모델 적용을 위한 전처리 및 모델 적용 후 미래의 y값을 추출하는 코드 
  |
  |-data_collection  # 데이터 수집 
  |  |-hanwoo_price.py                 # openapi로 부터 한우 가격을 수집하는 코드
  |  |-holiday.ipynb            # openapi를 이용하여 특일정보를 수집하는 코드
  |  |-가축사육 통계제공 서비스_축종별 통계 정보.py               # openapi를 이용하여 가축사육 통계 제공 서비스 데이터 수집하는 코드
  |  |-가축사육현황_한국유통수출협회(crawling).R       # 가축사육현황을 크롤링하는 코드
  |  |-전세계 수입현황.py                         # 전세계 한우 수입 현황을 크롤링하는 코드 
  |
  |-eda    # 데이터 탐색 
  |  |-Domain_knowledge.ipynb                 # Domain 지식을 쌓기 위한 참고용 
  |  |-README.md                     
  |  |-World_economic_growth_rate_EDA.ipynb                # 경제성장률 EDA 코드 
  |  |-all_merged_data-revise.ipynb          # 수집된 데이터를 합치는 코드 
  |  |-cow_disease_EDA.ipynb                          # 한우 가격 EDA하는 코드
  |  |-hanwoo_pig_price_hoilday.ipynb                    # 한우가격, 돼지가격, 공휴일 간 EDA하는 코드 
  |  |-livestock_breeding_status.ipynb          # 가축사육현황 EDA하는 코드 
  |  |-weather_EDA(week).ipynb       # 주별 날씨 EDA하는 코드 
  |
  |-.gitignore                               
  |
  |-README.md                           # 해당 문서
  |
  |-requirements.txt                    # 사전 설치 목록
  |
```
## 💻 Getting Started (Installation)
```
pip3 install -r requirements.txt
```
### How to use
```
1. data_collect_saturday.py  # 작업스케줄러를 이용하여 매주 토요일 특정 시각에 데이터가 수집되도록 설정 
2. model.py  # 작업 스케줄러를 이용하여 데이터가 수집된 후 모델을 적용할 수 있도록 설정 
```
- 실행 전 수정 필요 

> engine = create_engine("mysql+mysqldb://root:" + "password" + "@localhost/ddd", encoding='utf-8')   
db_host: MySQL HOST 주소   
db_user: MySQL 아이디  (root)   
db_passwd: MySQL 패스워드   (password)   
db_port: MySQL 포트  (@localhost)   
db_name: DB name명    (ddd)    

> request = urllib.request.Request(
        "http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=#&auctDate=" + str(
            date_) + "&auctFlag=2")   
 serviceKey: openapi 서비스키 (#)

