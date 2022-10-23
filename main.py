import os
import tkinter.ttk as ttk
from tkinter import *

import strategies

# 직전 로그 기록 파일
fileLog = "log.txt"
# 직전 결과 기록 파일
fileResult = "result.txt"

def openFile():
  # log.txt 열기
  if os.path.isfile(fileLog): # 파일 있으면 True, 없으면 False
    with open(fileLog, "r", encoding="utf8") as file:
      txtLog.delete("1.0", END) # 텍스트 위젯 본문 삭제
      txtLog.insert(END, file.read()) # 파일 내용을 본문에 입력
  # result.txt 열기
  if os.path.isfile(fileResult):
    with open(fileResult, "r", encoding="utf8") as file:
      txtResult.delete("1.0", END)
      txtResult.insert(END, file.read())

def saveFile():
  # log.txt 저장
  with open(fileLog, "w", encoding="utf8") as file:
    file.write(txtLog.get("1.0", END)) # 모든 내용을 저장
  # result.txt 저장
  with open(fileResult, "w", encoding="utf8") as file:
    file.write(txtResult.get("1.0", END))

# 거래 시작(버튼)
def startTrade():
  ticker = cmbTickers.get() # 프로그램 적용 코인
  timIntv = cmbTimIntv.get() # 봉 단위, minute1 = 1분봉
  mvAvg = cmbMvAvg.get() # 이동평균선 적용 값
  amount = float(tBoxAmt.get()) # 프로그램 시작 금액  
  
  strategies.ttsMa.main(ticker, timIntv, mvAvg[2:-2].split(', '), amount, txtStatus, txtLog) 

# 거래 종료(버튼)
def endTrade():
  # result에 결과 출력
  strategies.ttsMa.stopTrading(txtResult)

  # 결과 저장
  saveFile()
  # 만약 프로그램이 실행하고 있지 않다면
  # root.quit()

######################################

### Trade GUI 생성 ###g
root = Tk()
root.title("UpbitAuto")
root.geometry("660x580+100+100") # 가로 * 세로 + x좌표 + y좌표

# Menu Bar
menuBar = Menu(root)
# 파일
menuFile = Menu(menuBar, tearoff=0)
menuFile.add_command(label="Open File...", command=openFile)
menuFile.add_separator()
# menuFile.add_command(label="Save", command=saveFile)
# menuFile.add_separator()
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
frameOption.pack(fill="x", padx=5, pady=5)

# 콤보리스트 가운데 정렬
# frameOption.option_add('*TCombobox*Listbox.Justify', 'center')

# 1. Ticker Option (거래할 코인 설정)
# Ticker Label
lblTicker = Label(frameOption, text="Ticker", width=6)
lblTicker.pack(side="left", padx=5, pady=5)
# Ticker Combobox
optTickers = strategies.util.getTickers()
cmbTickers = ttk.Combobox(frameOption, state="readonly", justify="center", values=optTickers, width=12)
cmbTickers.current(0)
cmbTickers.pack(side="left", padx=5, pady=5)

# 2. TimIntv Option (시간 간격, minute1 = 1분봉)
# TimIntv Label
lblTimIntv = Label(frameOption, text="TimIntv", width=6)
lblTimIntv.pack(side="left", padx=5, pady=5)
# TimIntv Combobox
optTimIntv = ["minute1"]
cmbTimIntv = ttk.Combobox(frameOption, state="readonly", justify="center", values=optTimIntv, width=8)
cmbTimIntv.current(0)
cmbTimIntv.pack(side="left", padx=5, pady=5)

# 3. MvAvg Option (기준 이동평균선)
# MvAvg1 Label
lblMvAvg = Label(frameOption, text="MvAvg", width=6)
lblMvAvg.pack(side="left", padx=5, pady=5)

# MvAvg Combobox
optMvAvg = ["[ 7, 30 ]"]
cmbMvAvg = ttk.Combobox(frameOption, state="readonly", justify="center", values=optMvAvg, width=10)
cmbMvAvg.current(0)
cmbMvAvg.pack(side="left", padx=5, pady=5)

# 4. Amount Option
# Amount Label
lblAmount = Label(frameOption, text="Amount", width=6)
lblAmount.pack(side="left", padx=5, pady=5)

# Amount TextBox
amount = StringVar()
tBoxAmt = ttk.Entry(frameOption, textvariable=amount, justify='right', width=12)
tBoxAmt.insert(0, "10000")
tBoxAmt.pack(side="left", padx=5, pady=5)

# Status Frame
frameStatus = LabelFrame(root, text=" Status ")
frameStatus.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frameStatus)
scrollbar.pack(side="right", fill="y")

txtStatus = Text(frameStatus, height=4, yscrollcommand=scrollbar.set)
txtStatus.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtStatus.yview)

# Log Frame
frameLog = LabelFrame(root, text=" Log ")
frameLog.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frameLog)
scrollbar.pack(side="right", fill="y")

txtLog = Text(frameLog, height=20, yscrollcommand=scrollbar.set)
txtLog.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtLog.yview)

# Result Frame
resultFrame = LabelFrame(root, text=" Result ")
resultFrame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(resultFrame)
scrollbar.pack(side="right", fill="y")

txtResult = Text(resultFrame, height=5, yscrollcommand=scrollbar.set)
txtResult.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txtResult.yview)

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

