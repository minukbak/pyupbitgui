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
root.geometry("640x480+100+100") # 가로 * 세로 + x좌표 + y좌표

# 로그 기록 파일
filename = "log.txt"

def open_file():
  if os.path.isfile(filename): # 파일 있으면 True, 없으면 False
    with open(filename, "r", encoding="utf8") as file:
      log_file.delete("1.0", END) # 텍스트 위젯 본문 삭제
      log_file.insert(END, file.read()) # 파일 내용을 본문에 입력

def save_file():
  with open(filename, "w", encoding="utf8") as file:
    file.write(log_file.get("1.0", END)) # 모든 내용을 가져와서 저장

menu = Menu(root)

# 파일
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="Open File...", command=open_file)
menu_file.add_separator()
menu_file.add_command(label="Save", command=save_file)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=menu_file)

# 도움말
menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label="Welcome")
menu_help.add_separator()
menu_help.add_command(label="About")
menu.add_cascade(label="Help", menu=menu_help)

# Option Frame
frame_option = Frame(root)
frame_option.pack(padx=5, pady=5, ipady=5)

# 1. Ticker Option
# Ticker Label
lbl_ticker = Label(frame_option, text="Ticker", width=8)
lbl_ticker.pack(side="left", padx=5, pady=5)
# Ticker Combobox
opt_ticker = ["BTC", "ETH", "DOT"]
cmb_ticker = ttk.Combobox(frame_option, state="readonly", values=opt_ticker, width=10)
cmb_ticker.current(0)
cmb_ticker.pack(side="left", padx=5, pady=5)

# 2. TimIntv Option
# TimIntv Label
lbl_timIntv = Label(frame_option, text="TimIntv", width=8)
lbl_timIntv.pack(side="left", padx=5, pady=5)
# TimIntv Combobox
opt_timIntv = ["3", "7", "15", "30"]
cmb_timIntv = ttk.Combobox(frame_option, state="readonly", values=opt_timIntv, width=10)
cmb_timIntv.current(0)
cmb_timIntv.pack(side="left", padx=5, pady=5)

# 3. MvAvg Option
# MvAvg Label
lbl_mvAvg = Label(frame_option, text="MvAvg", width=8)
lbl_mvAvg.pack(side="left", padx=5, pady=5)
# MvAvg Combobox
opt_mvAvg = ["3", "7", "20"]
cmb_mvAvg = ttk.Combobox(frame_option, state="readonly", values=opt_mvAvg, width=10)
cmb_mvAvg.current(0)
cmb_mvAvg.pack(side="left", padx=5, pady=5)

# 4. Amount Option & Save Button
lbl_amount = Label(frame_option, text="Amount", width=8)
lbl_amount.pack(side="left", padx=5, pady=5)

btn_save = Button(frame_option, padx=5, pady=5, width=12, text="Save")
btn_save.pack(side="right")

# Log Frame
frame_log = Frame(root)
frame_log.pack(fill="both", padx=5, pady=5)
# 스크롤 바
scrollbar = Scrollbar(frame_log)
scrollbar.pack(side="right", fill="y")

# 로그 영역
log_file = Text(frame_log, height=15, yscrollcommand=scrollbar.set)
log_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=log_file.yview)

# Result Frame
result_frame = Frame(root)
result_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_file = Text(result_frame, height=10, yscrollcommand=scrollbar.set)
result_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=result_file.yview)

# Execute Frame
frame_execute = Frame(root)
frame_execute.pack(fill="x", padx=5, pady=5)

# Start Button
btn_start = Button(frame_execute, padx=5, pady=5, width=12, text="Start")
btn_start.pack(side="left")

# End Button
btn_end = Button(frame_execute, padx=5, pady=5, width=12, text="End")
btn_end.pack(side="right")


root.config(menu=menu)

root.resizable(False, False)
root.mainloop()