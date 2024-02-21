# pyupbitgui

### 자동매매 프로그램 사용 방법
1. API Key 발급 및 IP 주소 등록
   
    - UPBIT 자동매매 프로그램을 사용하시려면
      공식 홈페이지를 통해 API Key를 발급 받고,
      공인 IP 주소를 Upbit에 등록하셔야 합니다.
      (프로그램 상단 Help/IP Setting 메뉴를 참고하세요.)

    - Key 예시(총 30자리의 Access Key와 Secret Key 발급)
      Access key: 2tcRERLAXffuW5ohipVxYEDvgWw36uxxxxxxxxxx
      Secret key: u0taIcQCdczTACmnaeTFIdK2NpORtZxxxxxxxxxx
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