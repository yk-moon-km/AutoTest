from  AndroidTC import AndroidTC
from ATC_kine_push import AtcKinePush
import subprocess
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.mime.image import MIMEImage

SUCCESS_MAILCOUNT = 12*2
class ATC_Server(AndroidTC):
    def __init__(self, tc, device,account,version,folder='',subTC='',result_path='',count=0):
        print("Init ATC_Server")
        self.count = count
        super().__init__( tc, device,account ,version,folder,subTC,result_path)

    def server_check_tc(self, version, subbTC,driver,folder):
        self.driver = driver
        
        if self.count==0:
            self.apk_install(version,folder)
            # try:
            #     self._push_file(localpath + filename, remotepath + filename)
            # except subprocess.CalledProcessError as e:
            #     print(f"File upload failed: {e.stderr.decode('utf-8')}")
            #     return "fail"

            try:
                # 앱 활성화
                time.sleep(2)
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
            except WebDriverException as e:
                print(f"앱을 활성화하는 데 실패했습니다: {e}")
                return "fail"
            time.sleep(10)
            self.app_install_login(self.account,driver)
            time.sleep(10)
        return self.sever_check(driver)

    def send_email_with_embedded_image(self,to_email, subject, body, image_path):
        sender_email = self.mail_id
        sender_password = self.mail_pw

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # HTML 본문 (CID 참조)
        html_body = f"""
        <html>
        <body>
            <h2>🚨 테스트 알림</h2>
            <p><b>테스트 발생:</b> {body}</p>
            <p><b>시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <h3>📷 캡처된 스크린샷:</h3>
            <img src="cid:screenshot" width="500">
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        # CID 이미지 추가
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", "<screenshot>")
                msg.attach(img)

        # SMTP 서버에 연결하여 이메일 전송
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            print(f"✅ 이메일이 {to_email}로 성공적으로 전송되었습니다.")
        except Exception as e:
            print(f"❌ 이메일 전송 중 오류 발생: {e}")

# 기존 error_screenshot 함수 수정
    def error_screenshot(self, el, servertype,region):
        """
        - 성공이면 True 반환
        - 실패이면 False 반환 + 이메일 본문에 스크린샷 포함하여 전송
        """
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        success = bool(el)  # True면 성공, False면 실패

        status = "Success" if success else "Fail"

        # 저장할 스크린샷 파일 경로
        local_screenshot_path = f"{status}_{servertype}_{region}_{current_time_str}.jpg"

        # 스크린샷 저장
        screenshot = self.take_screenshot(
            f"/sdcard/DCIM/f{current_time_str}.png",
            local_screenshot_path
        )

        # 실패혹은 1000번에 한번씩 이메일 본문에 이미지 포함하여 전송
        if not success or self.count % SUCCESS_MAILCOUNT == 0:
        # if True:
            try:
                self.send_email_with_embedded_image(
                    to_email="yk.moon@kinemaster.com",
                    subject=f"[ALERT] Test {status}: {region}",
                    body=f"테스트 {status} 발생:  {region} \n서버 타입: {servertype}",
                    image_path=screenshot
                )
                print(f"🚨 실패 알림 이메일 전송 완료: {screenshot}")
                if not success:
                    return False
            except Exception as e:
                print(f"❌ 이메일 전송 실패: {e}")
                return False
        return True  # ✅ 성공이면 True, 실패이면 False
    def chaneg_region(self,driver,region):
        self.driver =driver
        
        driver.activate_app('com.surfshark.vpnclient.android')
        
        el = self.find_button(driver,'UI','new UiSelector().className("android.widget.ImageView")')
        if el:
            el.click()

        el = self.find_button(driver,'UI',f'new UiSelector().text(\"{region}\")')
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.Button\").instance(0)")
        if el:
            return True
        else:
            return False
        

    def sever_check(self,driver):
        self.driver =driver
        retvalue = True
        regions = ['Brazil','Egypt','Frankfurt am Main','Delhi','Seoul','United States']
        for region in regions:
            if self.chaneg_region(driver,region):
                try:
                    driver.terminate_app('com.nexstreaming.app.kinemasterfree')
                except WebDriverException as e:
                    driver.terminate_app('com.nexstreaming.app.kinemasterfree')
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
                time.sleep(5)
            #  change server
                try:
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(0)",30)
                    el.click()
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/iv_thumbnail\").instance(4)",30)
                    if self.error_screenshot(el, 'mix',region) is False:
                        retvalue = False
                        continue
                    el.click()  # 성공한 경우 다음 스텝 진행

                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)",30)
                    el.click()
                    el = self.find_button(driver,'UI','new UiSelector().text("Asset Store")',30)
                    el.click()  # 성공한 경우 다음 스텝 진행
                    
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/asset_store_image_h_list_asset_item_form_thumbnail\").instance(0)",30)
                    if self.error_screenshot(el, 'asset',region) is False:
                        retvalue = False
                        continue
                    el.click()  # 성공한 경우 다음 스텝 진행
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)",30)
                    el.click()
                    
                except Exception as e:
                    print(f"예외 발생: {e}")
                    self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail1_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
                    print("Version compare test failed")
                    retvalue = False
                    continue
            else:
                self.error_screenshot(False, 'vpn',region)
        return retvalue


    def run(self):
        self.driver = self._initialize_appium()
        
        try:
            # local_path = f'{self.current_folder}/Test/'
            # local_file = f'{self.subTC}'
            # remote_path = '/sdcard/Download/AutoTest/'
            return_val = self.server_check_tc( self.version[0],self.subTC,self.driver,self.folder)
            return return_val
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail2_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            return False

