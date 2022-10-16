import pyupbit
import json

# Config.json 파일을 통해 관리 중인 Upbit Key 불러오기 
with open('config.json', 'r') as conf:
  config = json.load(conf)
access = config['DEFAULT']['ACCESS_KEY'] 
secret = config['DEFAULT']['SECRET_KEY']

def accessUpbit():
  return pyupbit.Upbit(access, secret)

def getTickers():
  return pyupbit.get_tickers(fiat="KRW")