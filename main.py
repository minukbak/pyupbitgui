from strategies import tts3ma

ticker = "KRW-STPT" # 프로그램 적용 코인
interval = "minute1" # 봉 단위, minute1 = 1분봉
MA1 = 7 # 첫 번째 이동평균선 적용 값
MA2 = 30 # 두 번째 이동평균선 적용 값
amount = 10000 # 프로그램 시작 금액

tts3ma.main(ticker,interval, MA1, MA2, amount)