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

# First ask quote (시장가 매수 시 체결 위치 / 매도 1 호가)
def getMarketBuyPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["ask_price"]
# First bid quote (시장가 매도 시 체결 위치 / 매수 1 호가)
def getMarketSellPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["bid_price"]

with open('config.json', 'r') as conf:
  config = json.load(conf)

access = config['DEFAULT']['ACCESS_KEY'] 
secret = config['DEFAULT']['SECRET_KEY']

upbit = pyupbit.Upbit(access, secret)

def main(ticker, timIntv, mvAvg1, mvAvg2, amount):
  
  holding = False  # 현재 코인 보유 여부
  operMode = False # 시작 동시 매수 방지
  strtBalance = amount # 시작 잔고
  endBalance = strtBalance # 끝 잔고
  tikrBalance = 0.0 # 코인 잔고
  buyPrice = 0.0 # 매수가
  sellPrice = 0.0 # 매도가
  curPrice = 0.0 # 현재가
  fee = 0.0005 # 수수료

  # 잔고가 프로그램 최소 시작 금액보다 작으면 종료
  balance = upbit.get_balance("KRW")
  if (strtBalance * (1.0 - fee)) > balance:
    print("시작 금액이 부족합니다. ( 최대 가능 금액:", "{:,}".format(round(balance)), ")")
    exit()

  startTime = datetime.datetime.now()
  print("autotrade start - " + startTime.strftime("%H:%M:%S"))
  elapsedTime = (datetime.datetime.now() - startTime)

  while True:
    # 시작 동시 매수 방지: Sell condition은 MA1 <= MA2 이고 이 상태에서는 매수되지 않음
    if condxSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
      operMode = True

    # 매도
    # 해당 코인을 가지고 있고, 매도 조건이 True일 때
    if holding is True and operMode is True:
      if condxSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
        tikrBalance = upbit.get_balance(ticker)
        resp = upbit.sell_market_order(ticker, tikrBalance)
        sellPrice = getMarketSellPrice(ticker)
        endBalance = (tikrBalance * sellPrice) - (tikrBalance * sellPrice * fee)
        holding = False
        print("매도 발생 - 매도가:", sellPrice, "매도 총액:", round(endBalance))
        print("매도 주문 번호:", resp['uuid'])

    # 매수
    # 해당 코인을 가지고 있지 않고, 매수 조건이 True일 때
    if holding is False and operMode is True:
      if condxBuy(ticker, timIntv, mvAvg1, mvAvg2) is True:
        resp = upbit.buy_market_order(ticker, amount)
        buyPrice = getMarketBuyPrice(ticker)
        holding = True
        print("매수 발생 - 매수가:", buyPrice, "매수 총액:", round(endBalance))
        print("매수 주문 번호:", resp['uuid'])

    elapsedTime = (datetime.datetime.now() - startTime)
    curPrice = pyupbit.get_current_price(ticker)

    # 상태 출력
    print(f"{ticker} - MA:({mvAvg1}, {mvAvg2}) - 투자금: {strtBalance}원")
    print(f"현재가: {curPrice}원, 보유: {holding}, 경과: {elapsedTime}")

    time.sleep(1)