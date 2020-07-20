# 한우 평균 경매금액 예측 앱 서비스>
- 본 프로젝트의 최종적인 결과물은 한우 평균 경매금액을 예측하는 동시에 축산농가와 예비축산인들이 서로 소통할 수 있는 커뮤니티를 제공하는 모바일 앱 서비스 입니다.

- 하지만 <strong>이 레포지토리에서는 한우 평균 경매금액을 예측하는 모델링에 대한 내용만을 포함하고 있습니다.</strong>

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
