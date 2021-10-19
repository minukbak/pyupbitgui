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
root.geometry("640x480") # 가로 * 세로 (+ x좌표 + y좌표)

# 로그 기록 파일
filename = "log.txt"

def open_file():
  if os.path.isfile(filename): # 파일 있으면 True, 없으면 False
    with open(filename, "r", encoding="utf8") as file:
      txt.delete("1.0", END) # 텍스트 위젯 본문 삭제
      txt.insert(END, file.read()) # 파일 내용을 본문에 입력

def save_file():
  with open(filename, "w", encoding="utf8") as file:
    file.write(txt.get("1.0", END)) # 모든 내용을 가져와서 저장

menu = Menu(root)

menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="열기", command=open_file)
menu_file.add_command(label="저장", command=save_file)
menu_file.add_separator()
menu_file.add_command(label="끝내기", command=root.quit)
menu.add_cascade(label="파일", menu=menu_file)

# 편집, 서식, 보기, 도움말
menu.add_cascade(label="편집")
menu.add_cascade(label="서식")
menu.add_cascade(label="보기")
menu.add_cascade(label="도움말")

# 본문 영역
txt = Text(root)
txt.pack(side="left", fill="both", expand=True)

root.config(menu=menu)

root.mainloop()