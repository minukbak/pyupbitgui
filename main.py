import os
import tkinter.ttk as ttk
from tkinter import *

from strategies import tts3ma

ticker = "KRW-STPT" # 프로그램 적용 코인
timIntv = "minute1" # 봉 단위, minute1 = 1분봉
mvAvg1 = 7 # 첫 번째 이동평균선 적용 값
mvAvg2 = 30 # 두 번째 이동평균선 적용 값
amount = 10000 # 프로그램 시작 금액

# tts3ma.main(ticker, timIntv, mvAvg1, mvAvg2, amount)

root = Tk()
root.title("UpbitAuto")
root.geometry("640x500+100+100") # 가로 * 세로 + x좌표 + y좌표

# 직전 로그 기록 파일
fileLog = "log.txt"
# 직전 결과 기록 파일
fileResult = "result.txt"

def open_file():
  # log.txt 열기
  if os.path.isfile(fileLog): # 파일 있으면 True, 없으면 False
    with open(fileLog, "r", encoding="utf8") as file:
      txt_log.delete("1.0", END) # 텍스트 위젯 본문 삭제
      txt_log.insert(END, file.read()) # 파일 내용을 본문에 입력
  # result.txt 열기
  if os.path.isfile(fileResult):
    with open(fileResult, "r", encoding="utf8") as file:
      txt_result.delete("1.0", END)
      txt_result.insert(END, file.read())

def save_file():
  # log.txt 저장
  with open(fileLog, "w", encoding="utf8") as file:
    file.write(txt_log.get("1.0", END)) # 모든 내용을 저장
  # result.txt 저장
  with open(fileResult, "w", encoding="utf8") as file:
    file.write(txt_result.get("1.0", END))

# 시작
def start():
  txt_log.insert(END, "\nStart!")
  txt_log.update()
  txt_log.see(END)

# 시작
def end():
  # loop 종료
  # result에 결과 출력
  txt_result.insert(END, "\nEnd!")
  txt_result.update()
  txt_result.see(END)

  # 결과 저장
  save_file()
  # 만약 프로그램이 실행하고 있지 않다면
  # root.quit()

menu = Menu(root)

# 파일
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="Open File...", command=open_file)
menu_file.add_separator()
# menu_file.add_command(label="Save", command=save_file)
# menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=menu_file)

# 도움말
menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label="Welcome")
menu_help.add_separator()
menu_help.add_command(label="About")
menu.add_cascade(label="Help", menu=menu_help)

# Option Frame
frame_option = LabelFrame(root, text=" Options ")
frame_option.pack(fill="x", padx=5, pady=5)
frame_option.option_add('*TCombobox*Listbox.Justify', 'center') 

# 1. Ticker Option
# Ticker Label
lbl_ticker = Label(frame_option, text="Ticker", width=6)
lbl_ticker.pack(side="left", padx=5, pady=5)
# Ticker Combobox
opt_ticker = ["BTC", "ETH", "DOT"]
cmb_ticker = ttk.Combobox(frame_option, state="readonly", justify="center", values=opt_ticker, width=8)
cmb_ticker.current(0)
cmb_ticker.pack(side="left", padx=5, pady=5)

# 2. TimIntv Option
# TimIntv Label
lbl_timIntv = Label(frame_option, text="TimIntv", width=6)
lbl_timIntv.pack(side="left", padx=5, pady=5)
# TimIntv Combobox
opt_timIntv = ["3", "7", "15", "30"]
cmb_timIntv = ttk.Combobox(frame_option, state="readonly", justify="center", values=opt_timIntv, width=8)
cmb_timIntv.current(0)
cmb_timIntv.pack(side="left", padx=5, pady=5)

# 3. MvAvg Option
# MvAvg Label
lbl_mvAvg = Label(frame_option, text="MvAvg", width=6)
lbl_mvAvg.pack(side="left", padx=5, pady=5)
# MvAvg Combobox
opt_mvAvg = ["3", "7", "20"]
cmb_mvAvg = ttk.Combobox(frame_option, state="readonly", justify="center", values=opt_mvAvg, width=8)
cmb_mvAvg.current(0)
cmb_mvAvg.pack(side="left", padx=5, pady=5)

# 4. Amount Option
# Amount Label
lbl_amount = Label(frame_option, text="Amount", width=6)
lbl_amount.pack(side="left", padx=5, pady=5)

# Amount TextBox
str = StringVar()
tBox_Amt = ttk.Entry(frame_option, textvariable=str, justify='right', width=14)
tBox_Amt.pack(side="left", padx=5, pady=5)

# Log Frame
frame_log = LabelFrame(root, text=" Log ")
frame_log.pack(fill="both", padx=5, pady=5)
# 스크롤 바
scrollbar = Scrollbar(frame_log)
scrollbar.pack(side="right", fill="y")

# 로그 영역
txt_log = Text(frame_log, height=20, yscrollcommand=scrollbar.set)
txt_log.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txt_log.yview)

# Result Frame
result_frame = LabelFrame(root, text=" Result ")
result_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

txt_result = Text(result_frame, height=5, yscrollcommand=scrollbar.set)
txt_result.pack(side="left", fill="both", expand=True)
scrollbar.config(command=txt_result.yview)

# Execute Frame
frame_execute = Frame(root)
frame_execute.pack(fill="x", padx=5, pady=5)

# End Button
btn_end = Button(frame_execute, padx=5, pady=5, width=12, text="End", command=end)
btn_end.pack(side="right", padx=5)

# Start Button
btn_start = Button(frame_execute, padx=5, pady=5, width=12, text="Start", command=start)
btn_start.pack(side="right", padx=5)

root.config(menu=menu)

root.resizable(False, False)
root.mainloop()