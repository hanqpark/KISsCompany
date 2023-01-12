# 개요

![Untitled](./Untitled.png)

- KOSPI, KOSDAQ, KONEX 상장 기업에 대한 개요를 간단하게 검색할 수 있는 텔레그램 챗봇입니다.

# 주제 선정 이유

- 뉴스에서, 혹은 지나가다가 들은 기업이 어떤 사업을 하는지 갑자기 궁금할때 그 기업의 개요에 대해 간단하게 검색할 수 있는 채널이 있으면 어떨까?
- 대한민국 상장회사가 2600개 넘는데, 이 기업이 어떤 사업을 하고 있는지 랜덤으로 추천받으면 사업아이템에 대한 인사이트가 더 넓어지지 않을까?
- 검색한 회사 혹은 추천받은 회사의 유사 업종 또한 같이 파악할 수 있다면 투자에 관한 식견이 더 넓어지지 않을까?

# 플랫폼 선정 이유

| 플랫폼       | 금전적 이슈 | 검수 필요 | 이용자 수 | API 지원 |
| ------------ | ----------- | --------- | --------- | -------- |
| 카카오톡     | O           | O         | 많음      | 중       |
| FB Messenger | X           | O         | 많음      | 하       |
| Slack        | X           | X         | 적음      | 상       |
| Telegram     | X           | X         | 적음      | 상       |

# 구현 기능

- [x] /help 명령어 만들어서 사용설명서 배포
- [x] 서버 구현 시, local list에 상장기업명 826개 전부 저장
      ~~→ DB로 저장하면 가장 편하기는 하나.. 나중에 구현해보도록 하자~~
      → KRX KIND에서 상장기업정보 csv 파일 local에 저장하였음

## 회사 검색 기능

- [x] 사용자로부터 회사 이름 입력받기
  - [x] 회사 이름이 전혀 겹치지 않으면 “검색 결과가 없습니다” return
  - [x] 회사 이름이 조금이라도 겹치면 겹치는 기업명 return
  - [x] 회사 이름이 완벽히 일치하면
    - [x] 네이버 증권 → 종목 → 종목분석 → 기업개요를 scraping
    - [x] 기업명(티커) 하이퍼링크 return
    - [x] 기업 개요 return
      - [x] CSV에 있는 내용도 담아서 보낼 예정
    - [x] 곧바로 이어서 유사 업종 기업 항목 랜덤으로 5개 정도 return

## 상장기업 랜덤 추천 기능

- [x] 사용자로부터 /random 명령어 입력받기
- [x] 네이버 증권 → 종목 → 종목분석 → 기업개요를 scraping
- [x] 기업명(티커) 하이퍼링크 return
- [x] 기업 개요 return
  - [x] CSV에 있는 내용도 담아서 보낼 예정
- [x] 곧바로 이어서 유사 업종 기업 항목 랜덤으로 5개 정도 return

# 사용 라이브러리

- pandas → DataFrame
- Beautifulsoup4
- python-telegram-bot
  [GitHub - python-telegram-bot/python-telegram-bot: We have made you a wrapper you can't refuse](https://github.com/python-telegram-bot/python-telegram-bot)

# Trouble Shooting

[echobot.py - python-telegram-bot v20.0](https://docs.python-telegram-bot.org/en/stable/examples.echobot.html)

telegram bot의 버전이 업데이트 되면서 기존의 클래스를 활용할 수 없게 되어 용례를 확인함

[대한민국 대표 기업공시채널 KIND](https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage)

pykrx로 가져오는 대신 kind에서 xls 파일 다운받아서 DB처럼 사용했음 → Google spreadsheet에서 csv로 변환해서 사용

[파이썬으로 텔레그램 메시지 보낼 때, 하이퍼링크 넣는 방법 (markdown)](https://investory123.tistory.com/428)

종목명에 하이퍼링크를 넣는 방법 → 메세지 양식을 보다 더 보기 좋게 변경

[Python - 숫자(String) 앞에 0 채우기](https://codechacha.com/ko/python-zero-fill/)

종목코드가 숫자 형태로 저장되면서 앞의 0이 사라지기 때문에 필요했음

[리눅스 백그라운드 파이썬 실행 nohup 사용법](https://blkcoding.blogspot.com/2018/03/nohup.html)

goorm io에서 무중단으로 서버 돌릴 때 nohup 활용

# 참고

[https://github.com/INVESTAR/StockAnalysisInPython](https://github.com/INVESTAR/StockAnalysisInPython)

[점프 투 파이썬](https://wikidocs.net/92180)

[온라인기업정보 - 기업모니터 - 기업개요(엘앤에프)](https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=066970)
