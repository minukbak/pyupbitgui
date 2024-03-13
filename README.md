### 업비트 자동 매매 프로그램 설명
- 프로젝트명 : pyupbitgui
- 사용 언어 : Python
- 자동 매매 전략 : TTS_MA(Trend trading strategy using moving averages)
	- 간격이 다른 두 개의 이동평균선(이평선) 교차를 이용한 매매 전략이다.  
    단기 이평선이 장기 이평선을 뚫고 올라가는 경우(Golden Cross)에 매수,  
    단기 이평선이 장기 이평선을 뚫고 내려가는 경우(Dead Cross) 매도하여  
    매매 추세를 이용한 차익 실현을 꿈꿨다. (단지 꿈만 꾸었다...)

	- 짧은 이평선과, 짧은 시간 간격을 선택해 추세를 이용할 수 있도록 한다.

- 매매 기록 관리
	- 프로그램 매매 종료 시 설정 옵션 값, 매매 히스토리, 수익 결과를 시간 단위 파일로 저장하여 관리한다.  
    프로그램 상단 File 메뉴의 Privious Log 옵션을 사용하여 이전 거래 내용을 프로그램 내에서 확인할 수 있다.

---

##### 프로그램 사용 방법
1. IP 주소 등록 및 API Key 발급
    - UPBIT 자동 매매 프로그램을 사용하시려면  
      공인 IP 주소를 Upbit 공식 홈페이지에 등록하고,  
      API Key를 발급 받아 설정 파일에 작성하셔야 합니다.  
      (프로그램 상단 Help/IP Setting 메뉴를 참고하세요.)

    - Key 예시(총 30자리의 Access Key와 Secret Key 발급)  
      Access key: AAAAAAAAAAbbbbbbbbbbCCCCCCCCCCdddddddddd  
      Secret key: aaaaaaaaaaBBBBBBBBBBccccccccccDDDDDDDDDD  
      (발급 받은 Key 개인 메모장에 보관할 것)

2. 메인 폴더에 'config.json' 파일 생성 후 올바른 위치에 발급 받은 Key 입력
    - 'help_config.txt' 내용을 위의 json 파일에 복사 및 붙여 넣기  
      (위 파일은 외부에 공유 되지 않습니다.)
    - 'help_config.txt' 파일 내용
      ```
      {
          "DEFAULT": {
            "ACCESS_KEY": "",
            "SECRET_KEY": ""
          }
      }
      ```
3. 프로그램 실행 후 옵션 설정
    - 옵션 설명  
      a. Strategies : 자동 매매 전략 (TTS_MA: 두 개의 이평선 교차를 이용한 매매 전략)  
      b. Ticker : 자동 매매에 사용할 코인 코드  
      c. Amount : 자동 매매 설정 금액 (최소 10,000원)  
      d. MvAvg : 기준 이동평균선  
      e. TimeIntv : 이동평균선 시간 간격 (이평선 산출 기준: 이평선 * 간격)  
        - ex) [3 * minute5, 10 * minute5] = [15 , 50]
  
4. 프로그램 하단 Start 버튼 클릭
   
---

##### 총평

- 파이썬으로 만들어본 첫 프로그램  
  소스 및 구조가 엉망이라 생각한다.  
  자동 매매 전략 또한 별 효과를 보지 못했다.  
  좋은 꿈이었다.
