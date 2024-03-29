# Trend trading strategy using moving averages
import pyupbit
import datetime
import time
import json
import pprint

# 이동 평균선 계산
def calMvAvg(ticker, timIntv, cnt):
  df = pyupbit.get_ohlcv(ticker, timIntv, cnt+1)
  mvAvg = df['close'].rolling(cnt).mean().iloc[-2]
  return mvAvg

# 매수 조건
def condBuy(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 >= calMvAvg2 :
    return True
  return False

# 매도 조건
def condSell(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 <= calMvAvg2 :
    return True
  return False

# 시장가 매수 시 체결 위치 / 매도 1 호가
def getMkBuyPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["ask_price"]

# 시장가 매도 시 체결 위치 / 매수 1 호가
def getMkSellPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["bid_price"]

# 거래 출력
def printHistory(areaCase, txtArea, parts):
  if areaCase == "head" :
    txtArea.delete('1.0', 'end')
    txtArea.insert('end', f"- 시작 시간: {parts[0]}, 코인 코드: {parts[1]}, 현재가: {parts[2]}, 투자금: {parts[3]}\n")
    txtArea.insert('end', f"  MA: {parts[4]}, 간격: {parts[5]}, 경과: {parts[6]}\n")
    txtArea.update()
    txtArea.see('end')
  elif areaCase == "body" :
    txtArea.insert('end', f"- 거래 시간: {parts[0]}, 상태: {parts[1]}, 가격: {parts[2]}, 총액: {parts[3]}\n")
    txtArea.insert('end', f"  주문 번호: {parts[4]}\n")
    txtArea.update()
    txtArea.see('end')
  elif areaCase == "bottom" :
    txtArea.insert('end', f"- 종료 시간: {parts[0]}, 시작 금액: {parts[1]}, 종료 금액: {parts[2]}\n")
    txtArea.insert('end', f"  수익금: {parts[3]}원, 수익 비율: {parts[4]}\n")
    txtArea.update()
    txtArea.see('end')
  else :
      return
  return

# 트레이드 루프 시작 종료 flag 관리
global flag
flag = False
def checkFlag():
  return flag
def startTrading():
  global flag
  flag = True
  return
def stopTrading():
  global flag
  flag = False
  return

def main(upbit, ticker, timIntv, mvAvg, amount, txtHead, txtBody, txtBottom):

  # 모든 텍스트 입력 박스 초기화
  txtHead.delete('1.0', 'end')
  txtHead.update()
  txtBody.delete('1.0', 'end')
  txtBody.update()
  txtBottom.delete('1.0', 'end')
  txtBottom.update()

  holding = False  # 현재 코인 보유 여부
  operMode = False # 시작 동시 매수 방지
  startBalance = amount # 시작 잔고
  endBalance = startBalance # 끝 잔고
  tikrBalance = 0.0 # 코인 잔고
  buyPrice = 0.0 # 매수가
  sellPrice = 0.0 # 매도가
  curPrice = 0.0 # 현재가
  fee = 0.0005 # 수수료
  setSleep = 0.8 # 과트래픽 방지
  mvAvg1 = int(mvAvg[0]) # 기준 이동평균선
  mvAvg2 = int(mvAvg[1])

  basisTime = datetime.datetime.now()
  startTime = basisTime.strftime("%H:%M:%S")

  while flag is True :
    now = datetime.datetime.now().strftime("%H:%M:%S")

    # 시작 동시 매수 방지: Sell condition은 MA1 <= MA2 이고 이 상태에서는 매수되지 않음
    if condSell(ticker, timIntv, mvAvg1, mvAvg2) is True :
      operMode = True

    # 매도
    # 해당 코인을 가지고 있고, 매도 조건이 True일 때
    if holding is True and operMode is True :
      if condSell(ticker, timIntv, mvAvg1, mvAvg2) is True :
        tikrBalance = upbit.get_balance(ticker)
        resp = upbit.sell_market_order(ticker, tikrBalance)
        uuid = resp['uuid']
        sellPrice = getMkSellPrice(ticker)
        endBalance = round((tikrBalance * sellPrice) - (tikrBalance * sellPrice * fee), 1)
        holding = False
        state = "Sold"

        transaction = [now, state, sellPrice, endBalance, uuid]
        printHistory("body", txtBody, transaction)

        time.sleep(setSleep)

    # 매수
    # 해당 코인을 가지고 있지 않고, 매수 조건이 True일 때
    if holding is False and operMode is True :
      if condBuy(ticker, timIntv, mvAvg1, mvAvg2) is True :
        resp = upbit.buy_market_order(ticker, amount)
        uuid = resp['uuid']
        buyPrice = getMkBuyPrice(ticker)
        holding = True
        state = "Bought"

        transaction = [now, state, buyPrice, endBalance, uuid]
        printHistory("body", txtBody, transaction)

        time.sleep(setSleep)

    curPrice = pyupbit.get_current_price(ticker)
    elapsedTime = (datetime.datetime.now() - basisTime)

    status = [startTime, ticker, curPrice, startBalance, mvAvg, timIntv, elapsedTime]
    printHistory("head", txtHead, status)

    time.sleep(setSleep)

  # 거래 종료 시점 보유 중일 때 전량 매도
  if flag is False and holding is True :
    now = datetime.datetime.now().strftime("%H:%M:%S")

    tikrBalance = upbit.get_balance(ticker)
    resp = upbit.sell_market_order(ticker, tikrBalance)
    uuid = resp['uuid']
    sellPrice = getMkSellPrice(ticker)
    endBalance = round((tikrBalance * sellPrice) - (tikrBalance * sellPrice * fee), 1)
    state = "Sold"

    transaction = [now, state, sellPrice, endBalance, uuid]
    printHistory("body", txtBody, transaction)
  
  endTime = datetime.datetime.now().strftime("%H:%M:%S")

  settlement = [endTime, startBalance, endBalance, round(endBalance - startBalance, 1), round(endBalance / startBalance, 3)]
  printHistory("bottom", txtBottom, settlement)

  return