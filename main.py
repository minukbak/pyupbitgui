import os
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

# Ticker Option

# TimIntv Option

# MvAvg Option

# Amount Option & Save Button

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

# Execute Frame
frame_execute = Frame(root)
frame_execute.pack(fill="x", padx=5, pady=5)

# Start Button

# End Button

root.config(menu=menu)

root.resizable(False, False)
root.mainloop()