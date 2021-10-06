# Trend trading strategy using three moving averages
import pyupbit
import datetime
import time
import json
import pprint

# Calculate The Moving Average
def calMvAvg(ticker, interval, amount):
  avg = 0
  df = pyupbit.get_ohlcv(ticker, interval)
  for i in range(-1-amount, -1):
    avg += (df.iloc[i]['close'] / amount)
  return avg

# Condition of Buying
def condxBuy(ticker, interval, MA1, MA2):
  valueMA1 = calMvAvg(ticker, interval, MA1)
  valueMA2 = calMvAvg(ticker, interval, MA2)
  if valueMA1 >= valueMA2:
    return True
  return False

# Condition of Selling
def condxSell(ticker, interval, MA1, MA2):
  valueMA1 = calMvAvg(ticker, interval, MA1)
  valueMA2 = calMvAvg(ticker, interval, MA2)
  if valueMA1 <= valueMA2:
    return True
  return False

with open('config.json', 'r') as conf:
  config = json.load(conf)

access = config['DEFAULT']['ACCESS_KEY'] 
secret = config['DEFAULT']['SECRET_KEY']

upbit = pyupbit.Upbit(access, secret) # class instance, object

def main(ticker, interval, MA1, MA2, amount):
  
  hold = False  # 현재 코인 보유 여부
  op_mode = False # 시작 동시 매수 방지

  while True:
    now = datetime.datetime.now().strftime("%H:%M:%S")

    # 시작 동시 매수 방지: Sell condition은 MA1 <= MA2 이고 이 상태에서는 매수되지 않음
    if condxSell(ticker, interval, MA1, MA2) is True:
      op_mode = True

    # 매도 시도
    # 매도 조건이 True이고, 해당 코인을 가지고 있을 때
    if hold is True and op_mode is True:
      if condxSell(ticker, interval, MA1, MA2) is True:
        ticker_balance = upbit.get_balance(ticker)
        resp = upbit.sell_market_order(ticker, ticker_balance)
        hold = False
        pprint.pprint(resp)

    # 매수 시도
    # 매수 조건이 True이고, 해당 코인을 가지고 있지 않을 때
    if hold is False and op_mode is True:
      if condxBuy(ticker, interval, MA1, MA2) is True:
        resp = upbit.buy_market_order(ticker, amount)
        hold = True
        pprint.pprint(resp)

    # 상태 출력
    print(f"현재시간 {now} / 적용코인: {ticker} / 적용MA: ({MA1}, {MA2}) / 보유상태: {hold}")

    time.sleep(1)