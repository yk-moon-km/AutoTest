# AutoTest

# 설치 순서
# 스크립트 실행 권한
chomod +x *.sh

# 섪치및 테스트 서버 실행 스크립트 실행 
./deploy.sh
설치가 완료 되면 3개의 콘솔이 실행 
1.appium(원격 디바이스 제어)
2.celery(테스크 관리)
3.flask(웹서버)

# 테스트 방법
1. Test를 하기위한 device연결
    1.1 디바이스 언어 설정 영어
    1.2 최초디바이스 연결시 kinemaster 실행 -> Edit -> new project -> import -> file browser download폴더 선택 -> 그리드 보기 상태로 적용
    1.3 테스트 디바이스에 이미 설치된 kinemaster는 삭제 하고 테스트를위한 버전으로 새로 설치됨
2. 브라우저에서 127.0.0.1:5000 접속
3. 맨 아레에 있는 Upload Apk로 테스트가 필요한 apk를 업로드 
4. upload TC를 통해서 테스트할 프로젝트 및 비교를 위한 결과 파일 업로드 
5. Main TC를 선택 
    5.1  Version Compare: 2개의 apk를 순차적으로 설치 후 경우 각각 저장한 비디오를 비교
    5.2  Result Compare : TC 업로드시 업로드된 영상파일과 선택한 버전에서 저장한 비디오를 비교
6. 테스트 진행할 디바이스 선택 
7. subTC 선택
8. submit
9. Test status에서 작업 리스트를 확인가능
10. 하나의 작업이 진행중일 경우 다른 테스트는 진행 하지말것
11. Test status 완료된 테스트에 대해서 결과 확인
