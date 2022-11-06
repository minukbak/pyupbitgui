# Trend trading strategy using moving averages
import pyupbit
import datetime
import time
import json
import pprint

import tkinter.ttk as ttk
from tkinter import *

from . import util
upbit = util.accessUpbit()
flag = True

# 이동 평균선 계산
def calMvAvg(ticker, timIntv, cnt):
  df = pyupbit.get_ohlcv(ticker, timIntv, cnt+1)
  mvAvg = df['close'].rolling(cnt).mean().iloc[-2]
  return mvAvg

# 매수 조건
def condBuy(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 >= calMvAvg2:
    return True
  return False

# 매도 조건
def condSell(ticker, timIntv, mvAvg1, mvAvg2):
  calMvAvg1 = calMvAvg(ticker, timIntv, mvAvg1)
  calMvAvg2 = calMvAvg(ticker, timIntv, mvAvg2)
  if calMvAvg1 <= calMvAvg2:
    return True
  return False

# 시장가 매수 시 체결 위치 / 매도 1 호가
def getMBPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["ask_price"]

# 시장가 매도 시 체결 위치 / 매수 1 호가
def getMSPrice(ticker):
  return pyupbit.get_orderbook(ticker)[0]["orderbook_units"][0]["bid_price"]

# 트레이드 종료
def stopTrading(txtBottom):
  endTime = datetime.datetime.now().strftime("%H:%M:%S")
  txtBottom.insert(END, "종료시간: " + endTime + "\n")
  txtBottom.update()
  txtBottom.see(END)
  global flag
  flag = False
  return

def main(ticker, timIntv, mvAvg, amount, txtHead, txtBody):
  holding = False  # 현재 코인 보유 여부
  operMode = False # 시작 동시 매수 방지
  startBalance = amount # 시작 잔고
  endBalance = startBalance # 끝 잔고
  tikrBalance = 0.0 # 코인 잔고
  buyPrice = 0.0 # 매수가
  sellPrice = 0.0 # 매도가
  curPrice = 0.0 # 현재가
  fee = 0.0005 # 수수료
  
  mvAvg1 = int(mvAvg[0]) # 기준 이동평균선
  mvAvg2 = int(mvAvg[1])

  # 잔고가 프로그램 최소 시작 금액보다 작으면 종료
  myBalance = upbit.get_balance("KRW")
  if (startBalance * (1.0 - fee)) > myBalance:
    txtHead.delete('1.0', END)
    txtHead.insert(END, "계좌 잔고가 부족합니다. ( 최대 가능 금액:" + "{:,}".format(round(myBalance)) + "원 )\n")
    txtHead.update()
    txtHead.see(END)
    return

  basisTime = datetime.datetime.now()
  startTime = basisTime.strftime("%H:%M:%S")

  txtBody.delete('1.0', END)
  txtBody.insert(END, "autotrade start - " + startTime + "\n")
  txtBody.update()
  txtBody.see(END)

  while flag == True:
    # 시작 동시 매수 방지: Sell condition은 MA1 <= MA2 이고 이 상태에서는 매수되지 않음
    if condSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
      operMode = True

    # 매도
    # 해당 코인을 가지고 있고, 매도 조건이 True일 때
    if holding is True and operMode is True:
      if condSell(ticker, timIntv, mvAvg1, mvAvg2) is True:
        tikrBalance = upbit.get_balance(ticker)
        resp = upbit.sell_market_order(ticker, tikrBalance)
        sellPrice = getMSPrice(ticker)
        endBalance = (tikrBalance * sellPrice) - (tikrBalance * sellPrice * fee)
        holding = False
        txtBody.insert(END, f"\n매도 발생 - 매도가: {sellPrice}, 매도 총액: {round(endBalance)}\n")
        txtBody.insert(END, f"매도 주문 번호: {resp['uuid']}\n")
        txtBody.update()
        txtBody.see(END)

    # 매수
    # 해당 코인을 가지고 있지 않고, 매수 조건이 True일 때
    if holding is False and operMode is True:
      if condBuy(ticker, timIntv, mvAvg1, mvAvg2) is True:
        resp = upbit.buy_market_order(ticker, amount)
        buyPrice = getMBPrice(ticker)
        holding = True
        txtBody.insert(END, f"\n매수 발생 - 매수가: {buyPrice}, 매수 총액: {round(endBalance)}\n")
        txtBody.insert(END, f"매수 주문 번호: {resp['uuid']}\n")
        txtBody.update()
        txtBody.see(END)

    curPrice = pyupbit.get_current_price(ticker)
    elapsedTime = (datetime.datetime.now() - basisTime)

    status = [startTime, ticker, curPrice, startBalance, mvAvg, timIntv, elapsedTime]

    # 상태 출력
    txtHead.delete('1.0', END)
    txtHead.insert(END, f"\n시작시간: {status[0]}, 코인명: {status[1]}, 현재가: {status[2]}, 투자금: {status[3]}\n")
    txtHead.insert(END, f"MA: {status[4]}, 간격: {status[5]}, 경과: {status[6]}\n")
    txtHead.update()
    txtHead.see(END)

    time.sleep(0.8)