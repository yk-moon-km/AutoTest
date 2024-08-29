import subprocess
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
from videoCompare import videoComapre
from pathlib import Path
from datetime import datetime
import os

class AndroidTest:
    def __init__(self, tc, device='',account = "yk.moon@kinemaster.com",version1='7.4.12.33222.GP.apk',version2='7.4.17.33410.GP.apk'):
        self.test_seting(tc, device,version1,version2)
        # self.capabilities = {
        #     "platformName": "Android",
        #     "automationName": "uiautomator2",
        #     "deviceName": "udid",
        #     "udid": device
        # }
        # self.tc = tc
        # self.version1 = version1
        # self.version2 = version2
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.current_folder = os.path.dirname(__file__)
        self.result_folder = f"{tc}_{current_time}"
        self.result_path =f"{self.current_folder}/Result/{self.result_folder}/"
        self.account = account
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def test_seting(self, tc, account  = "", device='9C241FFBA001L8',version1='7.4.12.33222.GP.apk',version2='7.4.17.33410.GP.apk'):
        self.tc = tc
        self.account = account
        self.version1 = version1
        self.version2 = version2
        self.capabilities = {
            "platformName": "Android",
            "automationName": "uiautomator2",
            "deviceName": "udid",
            "udid": device
        }
    def find_button(self, appium_type, locator):
        count = 0
        while count < 30:
            try:
                if appium_type == 'xpath':
                    return self.driver.find_element(by=AppiumBy.XPATH, value=locator)
                elif appium_type == 'ID':
                    return self.driver.find_element(by=AppiumBy.ID, value=locator)
                else:
                    return self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=locator)
            except:
                try :
                    if locator == f"new UiSelector().text(\"{self.account}\")":
                        el = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                      value="new UiSelector().text(\"minji.kim@kinemaster.com\")")
                        return el
                except:
                    time.sleep(1)
                # 팦업 제거
                try:
                    el = self.driver.find_element(by=AppiumBy.ID, value="com.nexstreaming.app.kinemasterfree:id/collapse_button")
                    if el !=None:
                        el.click()
                except:
                    time.sleep(1)
                count += 1
        print(f"Failed to find element: {locator}")
        return None


    def ProjectTc(self, filename, localpath, remotepath):
        self.driver.terminate_app('com.nexstreaming.app.kinemasterfree')
        self.driver.activate_app('com.nexstreaming.app.kinemasterfree')

        try:
            self._push_file(localpath + filename, remotepath + filename)
        except subprocess.CalledProcessError as e:
            print(f"File upload failed: {e.stderr.decode('utf-8')}")

        try:
            el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
            el.click()
            el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
            el.click()
            el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(1)")
            el.click()
            el = self.find_button('UI', "new UiSelector().resourceId(\"com.google.android.documentsui:id/icon_thumb\").instance(0)")
            el.click()
            el = self.find_button('UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
            el.click()
            el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
            el.click()
            el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
            testfile = el.text
            self._press_key(4)  # Back key
            self._press_key(4)
        except:
            return False
        return testfile

    def version_compare_tc(self, loacal_file, loacal_path, remote_path, count):
        file1 = self.install_tc(self.version1, loacal_file, loacal_path, remote_path,count)
        file2 = self.install_tc(self.version2, loacal_file, loacal_path, remote_path,count)
        return file1, file2

    def app_install_login(self, account):
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        el.click()
        el = self.find_button('ID', "com.android.permissioncontroller:id/permission_deny_button")
        el.click()
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(4)")
        el.click()
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/cl_loading_button_container\").instance(0)")
        el.click()
        ac_text = f"new UiSelector().text(\"{account}\")"
        el = self.find_button('UI', ac_text)
        el.click()

    def mix_download(self):
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(1)")
        el.click()
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/mix_item_download\")")
        el.click()
        el = self.find_button("ID", "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button("ID", "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button('UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/title_form_template_upload_button")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/upload_desc_edit_text")
        el.send_keys("test")
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/upload_arrow_right_image_view")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/my_space_check_box")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/touch_outside")
        el.click()
        time.sleep(10)
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/upload_button")
        el.click()

    def mix_upload_tc(self):
        self.apk_install(self.version1)
        self.driver.activate_app('com.nexstreaming.app.kinemasterfree')
        self.app_install_login(self.account)
        self.mix_download()

    def install_tc(self, version, filename, localpath, remotepath,count):
        self.apk_install(version)
        try:
            self._push_file(localpath + filename, remotepath + filename)
        except subprocess.CalledProcessError as e:
            print(f"File upload failed: {e.stderr.decode('utf-8')}")
            return "fail"

        self.driver.activate_app('com.nexstreaming.app.kinemasterfree')

        self.app_install_login(self.account)
        self._create_new_project(count)

        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
        el.click()
        return el.text

    def infinix_tc(self, count):
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/new_project_view_group_touch_area")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/project_name_edit_text")
        el.send_keys(f"{count}")
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/create_project_button")
        el.click()
        self.driver.terminate_app('com.nexstreaming.app.kinemasterfree')
        self.driver.activate_app('com.nexstreaming.app.kinemasterfree')

        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_thumbnail\").instance(0)")
        el.click()
        el = self.find_button('UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()
        time.sleep(2)
        testvideofileName2 = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name").text

        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/title_form_start_button_1_icon")
        el.click()
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_editor_action_icon\").instance(0)")
        el.click()

        return testvideofileName2

    def TC1(self):
        el = self.find_button('xpath', '(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]')
        el.click()
        self.find_button('xpath', '(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]').click()
        self.find_button('xpath', "(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]").click()
        self.find_button('xpath', '//android.widget.GridView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/create_fragment_project_list\"]/android.view.ViewGroup[1]').click()
        self.find_button('xpath', "//android.widget.FrameLayout[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export\"]/android.widget.ImageView").click()
        self.find_button('id', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save").click()
        testvideofileName = self.find_button('xpath', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name").text
        return testvideofileName

    def delete_files_in_remote_folder(self, remote_folder):
        try:
            command = f'adb -s {self.capabilities.get("udid")} shell rm -rf {remote_folder}/*'
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode('utf-8')}")

    def file_download(self, filename, count=0, version=0):
        remote_dir = '/sdcard/Movies/KineMaster/'
        local_dir = f'{self.current_folder}/Test/TC{count}/'
        local_path = local_dir + f'TC{count}_{self.capabilities.get("udid")}_{version}' + '.mp4'
        remote_path = remote_dir + filename + '.mp4'

        try:
            subprocess.run(['adb', '-s', self.capabilities.get('udid'), 'pull', remote_path, local_path],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return local_path
        except subprocess.CalledProcessError as e:
            print(f"File download failed: {e.stderr.decode('utf-8')}")
            return None

    def regression(self, count):
        self._initialize_appium()
        try:
            local_path = f'{self.current_folder}/Test/TC{count}/kine/'
            local_file = f'tc{count}.kine'
            remote_path = '/sdcard/Download/AutoTest/'
            testvideofileName1 = self.install_tc(self.version1, local_file, local_path, remote_path,count)
            self.delete_files_in_remote_folder(remote_path)
            self.driver.quit()

            file1 = self.file_download(testvideofileName1, count)
            file2 = f'{self.current_folder}/Test/TC{count}/mp4/tc{count}.mp4'
            return self.compare_files(file1, file2, count)
        except:
            self.take_screenshot(f"/sdcard/DCIM/f{count}.png", f'fail_{self.tc}_TC{count}_{self.capabilities.get("udid")}.jpg')
            print("Regression test failed")
            self.driver.quit()
            return False

    def downandup(self):
        self._initialize_appium()
        try:
            self.mix_upload_tc()
            self.driver.quit()
            return True
        except:
            self.take_screenshot(f"/sdcard/DCIM/mixuploadtc.png", f'fail_TCmixuploadtc_{self.capabilities.get("udid")}.jpg')
            self.driver.quit()
            return False

    def version_compare(self, count):
        self._initialize_appium()
        try:
            local_path = f'{self.current_folder}/Test/TC{count}/kine/'
            local_file = f'tc{count}.kine'
            remote_path = '/sdcard/Download/AutoTest/'
            version1fileName, version2fileName = self.version_compare_tc( local_file, local_path, remote_path, count)
            self.delete_files_in_remote_folder(remote_path)
            self.driver.quit()

            file1 = self.file_download(version1fileName, count, Path(self.version1).name)
            file2 = self.file_download(version2fileName, count, Path(self.version2).name)
            return_val =  self.compare_files(file1, file2, count)
            # file1 ,2 delete
            # os.remove(file1)
            # os.remove(file2)
            return return_val
        except:
            self.take_screenshot(f"/sdcard/DCIM/f{count}.png", f'fail_{self.tc}_TC{count}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            self.driver.quit()
            return False

    def perform_actions(self, count):
        # version1 = '7.4.12.33222.GP.apk'
        # version2 = '7.4.17.33410.GP.apk'
        if self.tc == 'versioncompare':
            return self.version_compare(count)
        elif self.tc == 'regression':
            return self.regression(count)
        elif self.tc == 'downandup':
            return self.downandup() if count <= 2 else True

    def compare_files(self, file1, file2, count):
        lc = videoComapre(file1, file2)
        max_val, img1, img2 = lc.compare_frames()
        threshold = 0.02 if self.tc != 'versioncompare' else 0

        if max_val.item() > threshold:
            img1.save(f'{self.result_path}fail_{self.tc}_TC{count}_{self.capabilities.get("udid")}-1.jpg')
            img2.save(f'{self.result_path}fail_{self.tc}_TC{count}_{self.capabilities.get("udid")}-2.jpg')
            return False
        else:
            img1.save(f'{self.result_path}Success_{self.tc}_TC{count}_{self.capabilities.get("udid")}.jpg')
            return True

    def run_adb_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"ADB Error: {result.stderr.strip()}")
            return None

    def apk_install(self, filename='7.4.12.33222.GP.apk'):
        local_path = f'{self.current_folder}/'
        package_name = 'com.nexstreaming.app.kinemasterfree'

        try:
            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} uninstall {package_name}")
            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} install {local_path}{filename}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def take_screenshot(self, device_path='/sdcard/screenshot.png', local_path='screenshot.png'):
        try:
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'shell', 'screencap', device_path], check=True)
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'pull', device_path, f"{self.result_path}{local_path}"], check=True)
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'shell', 'rm', device_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        return local_path

    def _initialize_appium(self):
        appium_options = AppiumOptions()
        appium_options.load_capabilities(self.capabilities)
        appium_server_url = 'http://localhost:4723'
        self.driver = webdriver.Remote(appium_server_url, options=appium_options)


    # def _push_file(self, local_path, remote_path):
    #     subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'push', local_path, remote_path],
    #                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _push_file(self, local_path, remote_path):
        # 원격 디렉토리 경로 추출
        remote_dir = remote_path.rsplit('/', 1)[0]

        # 원격 디렉토리 존재 여부 확인
        check_dir_command = ['adb', '-s', self.capabilities.get("udid"), 'shell','if [ ! -d "{0}" ]; then mkdir -p "{0}"; fi'.format(remote_dir)]

        # 디렉토리 생성 명령어 실행
        subprocess.run(check_dir_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 파일을 원격 장치로 푸시
        push_command = ['adb', '-s', self.capabilities.get("udid"), 'push', local_path, remote_path]
        subprocess.run(push_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _press_key(self, keycode):
        self.driver.execute_script('mobile: pressKey', {"keycode": keycode})

    def _create_new_project(self,count):
        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
        el.click()

        el = self.find_button('UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(1)")
        el.click()
        el = self.find_button('ID',
                             "com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        el.click()
        # download 폴더 가기


        el = self.find_button('UI',"new UiSelector().description(\"Show roots\")")
        if el:
            el.click()
        udid = self.capabilities.get("udid")
        deviceName= get_device_name_by_udid(udid)
        device_value =  f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"{deviceName}\"]'
        el = self.find_button('xpath',device_value)
        el.click()

        el = self.find_button('UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_list\")")
        if not el:
            el = self.find_button('UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_grid\")")
            if el:
                el.click()

        el = self.find_button('UI',"new UiSelector().text(\"Download\")")
        el.click()

        el = self.find_button('UI',"new UiSelector().text(\"AutoTest\")")
        el.click()


        tc_string = f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"tc{count}.kine\"]'
        el = self.find_button('xpath', tc_string)
        if el:
            el.click()

        el = self.find_button('ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button('ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button('UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        el.click()
        el = self.find_button('ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()


def get_device_name_by_udid(udid):
    result = subprocess.run(['adb', '-s', udid, 'shell', 'getprop', 'ro.product.model'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        device_name = result.stdout.strip()
        return device_name
    else:
        raise Exception(f"Failed to get device name for {udid}: {result.stderr}")





# devices = ["9C241FFBA001L8"]#15151FDD4001GT"]# , "9C241FFBA001L8"]
# platform = ["Android", "iOS"]
# TCS = ["regression"] #regression versioncompare
# subTC = list(range(1, 2))  # "Create"
# failcount = 0
# Successcount = 0
# onetineTest_cnt = 0
# version1='uploads/7.4.18.33462.GP.apk'
# version2='uploads/7.4.17.33410.GP.apk'
# # __init__(self, tc, device='', account="yk.moon@kinemaster.com", version1='7.4.12.33222.GP.apk',
# #          version2='7.4.17.33410.GP.apk'):
# #
# # def test_seting(self, tc, account="", device='9C241FFBA001L8', version1='7.4.12.33222.GP.apk',
# #                 version2='7.4.17.33410.GP.apk'):

# # test = AndroidTest(action, account="yk.moon@kinemaster.com", version1=file_path1, version2=file_path2)
# test = AndroidTest("regression", "device","yk.moon@kinemaster.com", version1, version2)
# for tc in TCS:
#     for count in subTC:
#         if onetineTest_cnt == 0 and tc == "downandup":
#             onetineTest_cnt = 1
#         elif onetineTest_cnt == 1 and tc == "downandup":
#             continue

#         for device in devices:
#             test.test_seting(tc,"yk.moon@kinemaster.com", device,version1,version2)
#             retvalue = test.perform_actions(count)

#             if not retvalue:
#                 failcount += 1
#             else:
#                 Successcount += 1

# print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")
