import os
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messageBox

import strategies

# 직전 상태 기록 파일
fileStatus = "txt_status.txt"
# 직전 로그 기록 파일
fileLog = "txt_log.txt"
# 직전 결과 기록 파일
fileResult = "txt_result.txt"

def openFile():
  # status.txt 열기
  if os.path.isfile(fileStatus): # 파일 있으면 True, 없으면 False
    with open(fileStatus, "r", encoding="utf8") as file:
      txtHead.delete("1.0", END) # 텍스트 위젯 본문 삭제
      txtHead.insert(END, file.read()) # 파일 내용을 본문에 입력
  # log.txt 열기
  if os.path.isfile(fileLog):
    with open(fileLog, "r", encoding="utf8") as file:
      txtBody.delete("1.0", END)
      txtBody.insert(END, file.read())
  # result.txt 열기
  if os.path.isfile(fileResult):
    with open(fileResult, "r", encoding="utf8") as file:
      txtBottom.delete("1.0", END)
      txtBottom.insert(END, file.read())
  return

def saveFile():
  # status.txt 저장
  with open(fileStatus, "w", encoding="utf8") as file:
    file.write(txtHead.get("1.0", END)) # 모든 내용을 저장
  # log.txt 저장
  with open(fileLog, "w", encoding="utf8") as file:
    file.write(txtBody.get("1.0", END))
  # result.txt 저장
  with open(fileResult, "w", encoding="utf8") as file:
    file.write(txtBottom.get("1.0", END))
  return

# 거래 시작(버튼)
def startTrade():
  status = strategies.ttsMa.checkFlag()
  if status == True:
    messageBox.showwarning('거래중 알림', '이미 거래가 진행중입니다. 거래 종료 후 다시 시도해주세요.')
  else :
    upbit = strategies.util.accessUpbit()
    amount = float(tBoxAmt.get()) # 프로그램 시작 금액

    myBalance = strategies.util.getBalance(upbit, amount)
    if myBalance != False:
      messageBox.showwarning('계좌 잔고 부족', '계좌 잔고가 부족합니다.\n최대 금액 : ' + '{:,}'.format(round(myBalance)) + '원')
      return

    ticker = cmbTickers.get() # 프로그램 적용 코인
    timIntv = cmbTimIntv.get() # 봉 단위, minute1 = 1분봉
    mvAvg = cmbMvAvg.get() # 이동평균선 적용 값
    # strategy = cmbStrategies.get()

    strategies.ttsMa.startTrading()
    strategies.ttsMa.main(upbit, ticker, timIntv, mvAvg[2:-2].split(', '), amount, txtHead, txtBody, txtBottom)
  return

# 거래 종료(버튼)
def endTrade():
  status = strategies.ttsMa.checkFlag()
  if status == True:
    res = messageBox.askokcancel('거래 종료', '거래를 종료하시겠습니까?')
    if res == True:
      strategies.ttsMa.stopTrading()
  else:
    # saveFile()
    exit(0)
  return

######################################

### Trade GUI 생성 ###g
root = Tk()
root.title("UpbitAuto")
root.geometry("640x620+100+100") # 가로 * 세로 + x좌표 + y좌표

# Menu Bar
menuBar = Menu(root)
# 파일
menuFile = Menu(menuBar, tearoff=0)
menuFile.add_command(label="Previous Log", command=openFile)
menuFile.add_command(label="Save Log", command=saveFile)
menuFile.add_separator()
menuFile.add_command(label="Exit", command=root.quit)
menuBar.add_cascade(label="File", menu=menuFile)

# 도움말
menuHelp = Menu(menuBar, tearoff=0)
menuHelp.add_command(label="Welcome")
menuHelp.add_separator()
menuHelp.add_command(label="About")
menuBar.add_cascade(label="Help", menu=menuHelp)

# Option Frame
frameOption = LabelFrame(root, text=" Options ")
frameOption.pack(fill="both", padx=5, pady=5)

# Top Area Of Option Frame
frameOptionTop = Frame(frameOption)
frameOptionTop.pack(fill="x", padx=5)

# 1-1. Strategies Option (전략 설정)
# Strategies Label
lblStrategies = Label(frameOptionTop, text="Strategies", width=8)
lblStrategies.pack(side="left", padx=5)
# Ticker Combobox
optStrategies = ["TTS_MA"]

cmbStrategies = ttk.Combobox(frameOptionTop, state="readonly", justify="center", values=optStrategies, width=12)
cmbStrategies.current(0)
cmbStrategies.pack(side="left", padx=5)

# 1-2. Ticker Option (거래할 코인 설정)
# Ticker Label
lblTicker = Label(frameOptionTop, text="Ticker", width=8)
lblTicker.pack(side="left", padx=5)
# Ticker Combobox
optTickers = strategies.util.getTickers()

cmbTickers = ttk.Combobox(frameOptionTop, state="readonly", justify="center", values=optTickers, width=12)
cmbTickers.current(0)
cmbTickers.pack(side="left", padx=5)

# 2-3. Amount Option
# Amount TextBox
amount = StringVar()
tBoxAmt = ttk.Entry(frameOptionTop, textvariable=amount, justify='right', width=14)
tBoxAmt.insert(0, "10000")
tBoxAmt.pack(side="right", padx=5, pady=5)
# Amount Label
lblAmount = Label(frameOptionTop, text="Amount", width=8)
lblAmount.pack(side="right", padx=5, pady=5)

# Bottom Area Of Option Frame
frameOptionBottom = Frame(frameOption)
frameOptionBottom.pack(fill="x", padx=5, pady=5)

# 2-1. MvAvg Option (기준 이동평균선)
# MvAvg1 Label
lblMvAvg = Label(frameOptionBottom, text="MvAvg", width=8)
lblMvAvg.pack(side="left", padx=5, pady=5)

# MvAvg Combobox
optMvAvg = ["[ 7, 30 ]"]
cmbMvAvg = ttk.Combobox(frameOptionBottom, state="readonly", justify="center", values=optMvAvg, width=12)
cmbMvAvg.current(0)
cmbMvAvg.pack(side="left", padx=5, pady=5)

# 2-2. TimIntv Option (시간 간격, minute1 = 1분봉)
# TimIntv Label
lblTimIntv = Label(frameOptionBottom, text="TimIntv", width=8)
lblTimIntv.pack(side="left", padx=5, pady=5)
# TimIntv Combobox
optTimIntv = ["minute1"]
cmbTimIntv = ttk.Combobox(frameOptionBottom, state="readonly", justify="center", values=optTimIntv, width=12)
cmbTimIntv.current(0)
cmbTimIntv.pack(side="left", padx=5, pady=5)

# Status Frame
frameStatus = LabelFrame(root, text=" Status ")
frameStatus.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frameStatus)
scrollbar.pack(side="right", fill="y")

txtHead = Text(frameStatus, height=4, yscrollcommand=scrollbar.set)
txtHead.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtHead.yview)

# Log Frame
frameLog = LabelFrame(root, text=" Log ")
frameLog.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frameLog)
scrollbar.pack(side="right", fill="y")

txtBody = Text(frameLog, height=20, yscrollcommand=scrollbar.set)
txtBody.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtBody.yview)

# Result Frame
resultFrame = LabelFrame(root, text=" Result ")
resultFrame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(resultFrame)
scrollbar.pack(side="right", fill="y")

txtBottom = Text(resultFrame, height=4, yscrollcommand=scrollbar.set)
txtBottom.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtBottom.yview)

# Execute Frame
frameExecute = Frame(root)
frameExecute.pack(fill="x", padx=5, pady=5)

# End Button
btnEnd = Button(frameExecute, padx=5, pady=5, width=12, text="End", command=endTrade)
btnEnd.pack(side="right", padx=5)

# Start Button
btnStart = Button(frameExecute, padx=5, pady=5, width=12, text="Start", command=startTrade)
btnStart.pack(side="right", padx=5)

root.config(menu=menuBar)
root.resizable(False, False)

root.mainloop()

