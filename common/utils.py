import pyupbit
import json

def accessUpbit():
  # Config.json 파일을 통해 관리 중인 Upbit Key 불러오기 
  with open('config.json', 'r') as conf:
    config = json.load(conf)
  access = config['DEFAULT']['ACCESS_KEY'] 
  secret = config['DEFAULT']['SECRET_KEY']

  return pyupbit.Upbit(access, secret)

def getTickers():
  return pyupbit.get_tickers(fiat="KRW")

def getBalance(upbit, amount):
  fee = 0.0005 # 수수료
  balance = upbit.get_balance("KRW")

  return balance if (amount * (1.0 - fee)) > balance else False