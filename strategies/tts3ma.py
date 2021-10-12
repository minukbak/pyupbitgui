# Trend trading strategy using three moving averages
import pyupbit
import datetime
import time
import json
import pprint

# Calculate The Moving Average (이동 평균선 계산)
def calMvAvg(ticker, timIntv, cnt):
  df = pyupbit.get_ohlcv(ticker, timIntv, cnt+1)
  mvAvg = df['close'].rolling(cnt).mean().iloc[-2]
  return mvAvg

# Condition of Buying (매수 조건)
def condxBuy(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 >= calMvAvg2:
    return True
  return False

# Condition of Selling (매도 조건)
def condxSell(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 <= calMvAvg2:
    return True
  return False

with open('config.json', 'r') as conf:
  config = json.load(conf)

access = config['DEFAULT']['ACCESS_KEY'] 
secret = config['DEFAULT']['SECRET_KEY']

upbit = pyupbit.Upbit(access, secret)

def main(ticker, timIntv, mvAvg1, mvAvg2, amount):
  
  holding = False  # 현재 코인 보유 여부
  operMode = False # 시작 동시 매수 방지

  while True:
    now = datetime.datetime.now().strftime("%H:%M:%S")

    # 시작 동시 매수 방지: Sell condition은 MA1 <= MA2 이고 이 상태에서는 매수되지 않음
    if condxSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
      operMode = True

    # 매도
    # 해당 코인을 가지고 있고, 매도 조건이 True일 때
    if holding is True and operMode is True:
      if condxSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
        balTicker = upbit.get_balance(ticker)
        resp = upbit.sell_market_order(ticker, balTicker)
        holding = False
        pprint.pprint(resp)

    # 매수
    # 해당 코인을 가지고 있지 않고, 매수 조건이 True일 때
    if holding is False and operMode is True:
      if condxBuy(ticker, timIntv, mvAvg1, mvAvg2) is True:
        resp = upbit.buy_market_order(ticker, amount)
        holding = True
        pprint.pprint(resp)

    # 상태 출력
    print(f"현재시간 {now} / 적용코인: {ticker} / 적용MA: ({mvAvg1}, {mvAvg2}) / 보유상태: {holding}")

    time.sleep(1)