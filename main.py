import os
import datetime
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messageBox
import tkinter.filedialog as filedialog
import webbrowser

import common
import strategies

def openFile():
  logsDirPath = os.path.dirname(os.path.abspath(__file__)) + "\\txnLogs\\"
  logFile = filedialog.askopenfilename(initialdir=logsDirPath, filetypes=(("Text files", "*.txt"),))

  with open(logFile, "r", encoding="utf8") as file :
      txtHead.delete("1.0", END)
      lines = ""
      while True :
        line = file.readline()
        if not line : break

        if "Log" in line :
          txtHead.insert(END, lines.strip() + "\n")
          break
        lines += line

      txtBody.delete("1.0", END)
      lines = ""
      while True :
        line = file.readline()
        if not line : break

        if "Result" in line :
          txtBody.insert(END, lines.strip() + "\n")
          break
        lines += line

      txtBottom.delete("1.0", END)
      txtBottom.insert(END, file.read().strip() + "\n")
  return

def saveFile():
  # 거래 이력이 있을 경우에만 파일 저장
  if txtHead.get("1.0", END).strip() + txtBottom.get("1.0", END).strip():
    logsDirPath = os.path.dirname(os.path.abspath(__file__)) + "\\txnLogs\\"
    logFileName = "log_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"

    logFile = logsDirPath + logFileName

    with open(logFile, "w", encoding="utf8") as file :
      file.write("#Status\n")
      file.write(txtHead.get("1.0", END))
      file.write("#Log\n")
      file.write(txtBody.get("1.0", END))
      file.write("#Result\n")
      file.write(txtBottom.get("1.0", END))
  return

# 거래 시작(버튼)
def startTrade():
  status = strategies.ttsMa.checkFlag()
  if status == True :
    messageBox.showwarning('거래중 알림', '이미 거래가 진행중입니다. 거래 종료 후 다시 시도해주세요.')
  else :
    upbit = common.utils.accessUpbit()
    amount = float(tBoxAmt.get()) # 프로그램 시작 금액

    if amount < 10000 :
      messageBox.showwarning('프로그램 시작 최소 금액 부족 알림',
                             '프로그램 시작 최소 금액 은 10,000원 입니다.\n현재 입력 금액 : ' + '{:,}'.format(round(amount)) + '원')
      tBoxAmt.delete('0', END)
      tBoxAmt.insert(END, '10000')
      amount = 0
      return

    # 계좌 잔고 부족 처리
    myBalance = common.utils.getBalance(upbit)

    if myBalance < 0 :
      messageBox.showwarning('프로그램 시작 에러',
                             'API Key 및 IP 주소가 제대로 등록되어 있는지 확인해 주세요.')
      return

    # fee = 0.05%
    if (amount * (1.0 - 0.05)) > myBalance :
      messageBox.showwarning('계좌 잔고 부족 알림',
                             '계좌 잔고가 부족합니다.\n최대 금액 : ' + '{:,}'.format(round(myBalance)) + '원')
      return

    ticker = cmbTickers.get() # 프로그램 적용 코인
    tikrBalance = upbit.get_balance(ticker)

    # 이미 보유하고 있는 코인에 대한 프로그램 사용 제한 처리
    if tikrBalance > 0 :
      messageBox.showwarning('기 보유 코인 사용 제한 알림',
                             '이미 보유한 코인에 대해서는 프로그램 사용이 제한됩니다.\n코인 코드 : ' + ticker + ', 기 보유 수량 : ' + str(tikrBalance) + '개')
      return

    timIntv = cmbTimIntv.get() # 봉 단위, ex) minute1 = 1분봉
    mvAvg = cmbMvAvg.get() # 이동평균선 적용 값
    # strategy = cmbStrategies.get()

    strategies.ttsMa.startTrading()
    strategies.ttsMa.main(upbit, ticker, timIntv, mvAvg[2:-2].split(', '), amount, txtHead, txtBody, txtBottom)
  return

# 거래 종료(버튼)
def endTrade():
  status = strategies.ttsMa.checkFlag()
  if status == True : # 프로그램이 가동 중일 경우
    res = messageBox.askokcancel('거래 종료', '거래를 종료하시겠습니까?')
    if res == True :
      strategies.ttsMa.stopTrading()
  else :
    saveFile()
    root.destroy()
  return

def exitButton():
  status = strategies.ttsMa.checkFlag()
  if status == True : # 프로그램이 가동 중일 경우
    res = messageBox.askokcancel('거래 종료', '거래를 종료하시겠습니까?')
    if res == True :
      strategies.ttsMa.stopTrading()
      saveFile()
      root.destroy()
  else :
    saveFile()
    root.destroy()
  return

def getUpbitAPI():
  webbrowser.open_new("https://upbit.com/mypage/open_api_management")

def goWhatIsMyIP():
  webbrowser.open_new("https://www.google.com/search?q=what+is+my+ip&oq=wh&aqs=chrome.1.69i57j69i59j35i39j0i131i433i512l2j69i60l2j69i61.2238j0j7&sourceid=chrome&ie=UTF-8")

def settingIP():
  dialog = Tk()
  dialog.title("Upbit Api 허용 IP 관리")
  dialog.geometry("300x240+250+200")
  
  dialogFrame = LabelFrame(dialog, bd=0)
  dialogFrame.pack(fill="both", expand=True)

  dialogText1 = Label(dialogFrame, text="\nIP Setting", font=("Arial", 12))
  dialogText1.pack()
  dialogText2 = Label(dialogFrame, text="\n아래 버튼을 통해 해당 사이트로 이동", font=("Arial", 11))
  dialogText2.pack()
  dialogText3 = Label(dialogFrame, text="\nAPI Key 발급 및 IP 주소 등록하기", font=("Arial", 10))
  dialogText3.pack()
  dialogBtn1 = Button(dialogFrame, text="발급 및 등록", font=("Arial", 10), cursor="hand2", command=getUpbitAPI)
  dialogBtn1.pack()
  dialogText4 = Label(dialogFrame, text="\n내 공인 IP 주소 확인하기", font=("Arial", 10))
  dialogText4.pack()
  dialogBtn2 = Button(dialogFrame, text="확인하기", font=("Arial", 10), cursor="hand2", command=goWhatIsMyIP)
  dialogBtn2.pack()

  dialog.resizable(False, False)
  dialog.mainloop()
  return

def welcomeTK():
  dialog = Tk()
  dialog.title("NOTICE")
  dialog.geometry("300x260+250+200")
  
  dialogFrame = LabelFrame(dialog, bd=0)
  dialogFrame.pack(fill="both", expand=True)

  dialogText1 = Label(dialogFrame, text="\nWELCOME!", font=("Arial", 12))
  dialogText1.pack()
  dialogText2 = Label(dialogFrame, text="\n안녕하세요.\n본 프로그램은 Upbit 자동 매매 프로그램입니다.", font=("Arial", 10))
  dialogText2.pack()
  dialogText2 = Label(dialogFrame, text="\n모든 선택이 성공적인 결과로 이어지길 기원하며,\n신중하게 사용하시여 주시길 바랍니다.", font=("Arial", 10))
  dialogText2.pack()
  dialogText3 = Label(dialogFrame, text="\n프로그램을 사용해주셔서 대단히 감사합니다.", font=("Arial", 10))
  dialogText3.pack()
  dialogText4 = Label(dialogFrame, text="\n\nMade by: Mubby", font=("Arial", 8))
  dialogText4.pack()

  dialog.resizable(False, False)
  dialog.mainloop()
  return

def manualTK():
  dialog = Tk()
  dialog.title("MANUAL")
  dialog.geometry("400x560+250+150")
  
  dialogFrame = LabelFrame(dialog, bd=0)
  dialogFrame.pack(fill="both", expand=True)

  dialogText1 = Label(dialogFrame, text="\nMANUAL", font=("Arial", 12))
  dialogText1.pack()

  dialogText2 = Label(dialogFrame, text="\n1. API Key 발급 및 IP 주소 등록", font=("Arial", 11))
  dialogText2.pack()

  dialogText3 = Label(dialogFrame, text="\nUPBIT 자동 매매 프로그램을 사용하시려면\n공인 IP 주소를 Upbit 공식 홈페이지에 등록하고,\nAPI Key를 발급 받아 설정 파일에 작성하셔야 합니다.\n(프로그램 상단 Help/IP Setting 메뉴를 참고하세요.)", font=("Arial", 10))
  dialogText3.pack()

  dialogText4 = Label(dialogFrame, text="\n- Key 예시(총 30자리의 Access Key와 Secret Key 발급)\nAccess key: 2tcRERLAXffuW5ohipVxYEDvgWw36uxxxxxxxxxx\nSecret key: u0taIcQCdczTACmnaeTFIdK2NpORtZxxxxxxxxxx\n(발급 받은 Key 개인 메모장에 보관할 것)", font=("Arial", 10))
  dialogText4.pack()

  dialogText5 = Label(dialogFrame, text="\n2. 메인 폴더에 'config.json' 파일 생성 후 Key 입력", font=("Arial", 11))
  dialogText5.pack()

  dialogText6 = Label(dialogFrame, text="\n'help_config.txt' 내용을 위의 json 파일에 복사 및 붙여 넣기\n('config.json' 파일은 외부에 공유 되지 않습니다.)", font=("Arial", 10))
  dialogText6.pack()

  dialogText7 = Label(dialogFrame, text="\n용어 정리", font=("Arial", 12))
  dialogText7.pack()

  dialogText8 = Label(dialogFrame, text="\nStrategies = 사용 가능한 자동 매매 전략", font=("Arial", 10))
  dialogText8.pack()

  dialogText9 = Label(dialogFrame, text="Ticker = 자동 매매에 사용할 코인 코드", font=("Arial", 10))
  dialogText9.pack()

  dialogText10 = Label(dialogFrame, text="Amount = 자동 매매 설정 금액 (최소 10,000원)", font=("Arial", 10))
  dialogText10.pack()

  dialogText11 = Label(dialogFrame, text="MvAvg = 사용하는 이동평균선 기준", font=("Arial", 10))
  dialogText11.pack()

  dialogText12 = Label(dialogFrame, text="TimeIntv = 이동평균선 시간 간격", font=("Arial", 10))
  dialogText12.pack()

  dialog.resizable(False, False)
  dialog.mainloop()
  return

######################################

### Trade GUI 생성 ###g
root = Tk()
root.title("UpbitAuto")
root.geometry("640x620+100+100") # 가로 * 세로 + x좌표 + y좌표
root.protocol("WM_DELETE_WINDOW", exitButton)

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
menuHelp.add_command(label="Welcome", command=welcomeTK)
menuHelp.add_separator()
menuHelp.add_command(label="Manual", command=manualTK)
menuHelp.add_command(label="IP Setting", command=settingIP)
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
optTickers = common.utils.getTickers()

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
optMvAvg = ["[ 3, 7 ]", "[ 3, 10 ]", "[ 3, 30 ]", "[ 3, 60 ]" \
            , "[ 7, 10 ]", "[ 7, 30 ]", "[ 7, 60 ]" \
            , "[ 10, 30 ]", "[ 10, 60 ]" \
            , "[ 30, 60 ]"]
cmbMvAvg = ttk.Combobox(frameOptionBottom, state="readonly", justify="center", values=optMvAvg, width=12)
cmbMvAvg.current(0)
cmbMvAvg.pack(side="left", padx=5, pady=5)

# 2-2. TimIntv Option (시간 간격, ex) minute1 = 1분봉)
# TimIntv Label
lblTimIntv = Label(frameOptionBottom, text="TimIntv", width=8)
lblTimIntv.pack(side="left", padx=5, pady=5)
# TimIntv Combobox
optTimIntv = ["minute1", "minute3", "minute5", "minute10", "minute15", "minute30", "minute60", "minute240"]
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

