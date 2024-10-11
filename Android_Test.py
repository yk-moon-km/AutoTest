
from datetime import datetime
from adbutils import device
import os

# TestClass
from atc_kine_push_vc import AtcKinePushVc
from atc_kine_push_rg import AtcKinePushRg
from atc_mix_vc import AtcMixVc
from atc_mix_rg import AtcMixRg


class AndroidTest:
    def __init__(self, tc, device='',account = "",version1='',version2=''):
        print(f"AndroidTest Init")
        self.device = device
        self.tc = tc
        self.version1 = version1
        self.version2 = version2
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.current_folder = os.path.dirname(__file__)
        self.result_folder = f"{tc}_{current_time}"
        self.result_path = f"{self.current_folder}/Result/{self.result_folder}/"
        self.account = account
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def set_subTC(self,subTC):
        test_type, test_case = subTC.split(',')
        self.subTC = test_case
        self.test_type = test_type

    def set_device(self, device):
        self.device = device


    def perform_actions(self):
        print(f"perform_actions  {self.tc} {self.test_type} {self.device}, {self.account},{self.version1},{self.version2},{self.subTC},{self.result_path}")
        if self.test_type == 'kine':
            if self.tc == 'versioncompare':
                test= AtcKinePushVc("versioncompare_kine",self.device, self.account,self.version1,self.version2,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcKinePushRg("regression_kine",self.device, self.account, self.version1, self.version2, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        elif self.test_type == 'mix':
            if self.tc == 'versioncompare':
                test= AtcMixVc("versioncompare_mix",self.device, self.account,self.version1,self.version2,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcMixRg("regression_mix",self.device, self.account, self.version1, self.version2, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        else:
            return "error"

        # elif self.tc == 'downandup':
        #     return self.downandup() if count <= 2 else True

    #
    #
    # def ProjectTc(self, filename, localpath, remotepath):
    #     self.driver.terminate_app('com.nexstreaming.app.kinemasterfree')
    #     self.driver.activate_app('com.nexstreaming.app.kinemasterfree')
    #
    #     try:
    #         self._push_file(localpath + filename, remotepath + filename)
    #     except subprocess.CalledProcessError as e:
    #         print(f"File upload failed: {e.stderr.decode('utf-8')}")
    #
    #     try:
    #         el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
    #         el.click()
    #         el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
    #         el.click()
    #         el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(1)")
    #         el.click()
    #         el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.google.android.documentsui:id/icon_thumb\").instance(0)")
    #         el.click()
    #         el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
    #         el.click()
    #         el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
    #         el.click()
    #         el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
    #         testfile = el.text
    #         self._press_key(4)  # Back key
    #         self._press_key(4)
    #     except:
    #         return False
    #     return testfile
    #
    #
    #

    #
    #
    #
    # def infinix_tc(self, count):
    #     el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
    #     el.click()
    #     el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/new_project_view_group_touch_area")
    #     el.click()
    #     el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/project_name_edit_text")
    #     el.send_keys(f"{count}")
    #     el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/create_project_button")
    #     el.click()
    #     self.driver.terminate_app('com.nexstreaming.app.kinemasterfree')
    #     self.driver.activate_app('com.nexstreaming.app.kinemasterfree')
    #
    #     el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_thumbnail\").instance(0)")
    #     el.click()
    #     el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
    #     el.click()
    #     el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
    #     el.click()
    #     time.sleep(2)
    #     testvideofileName2 = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name").text
    #
    #     el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/title_form_start_button_1_icon")
    #     el.click()
    #     el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_editor_action_icon\").instance(0)")
    #     el.click()
    #
    #     return testvideofileName2
    #
    # def TC1(self):
    #     el = self.find_button(driver,'xpath', '(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]')
    #     el.click()
    #     self.find_button(driver,'xpath', '(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]').click()
    #     self.find_button(driver,'xpath', "(//android.widget.ImageView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\"])[3]").click()
    #     self.find_button(driver,'xpath', '//android.widget.GridView[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/create_fragment_project_list\"]/android.view.ViewGroup[1]').click()
    #     self.find_button(driver,'xpath', "//android.widget.FrameLayout[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export\"]/android.widget.ImageView").click()
    #     self.find_button(driver,'id', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save").click()
    #     testvideofileName = self.find_button(driver,'xpath', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name").text
    #     return testvideofileName
    #
    #
    #


    # def downandup(self):
    #     self._initialize_appium()
    #     try:
    #         self.mix_upload_tc()
    #         #self.driver.quit()
    #         return True
    #     except:
    #         self.take_screenshot(f"/sdcard/DCIM/mixuploadtc.png", f'fail_TCmixuploadtc_{self.capabilities.get("udid")}.jpg')
    #         #self.driver.quit()
    #         return False











    # def _push_file(self, local_path, remote_path):
    #     subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'push', local_path, remote_path],
    #                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # def _press_key(self, keycode):
    #     self.driver.execute_script('mobile: pressKey', {"keycode": keycode})




#
#
#
# devices = ["9C241FFBA001L8"]#15151FDD4001GT"]# , "9C241FFBA001L8"]
# platform = ["Android", "iOS"]
# TCS = ["versioncompare"]
# # subTC = ["Test1"]
# # TCS = ["regression_kine"]
# # subTC = ["Test1"]
# # TCS = ["regression"]
# subTC = [ 'kine,20240726.kine']
# # subTC = ['mix,https://kine.to/template/66e03a361098d00c48cf8933','kine,20240726.kine']
#
# failcount = 0
# Successcount = 0
# onetineTest_cnt = 0
# version1='uploads/7.4.18.33462.GP.apk'
# version2='uploads/7.4.18.33463.GP.apk'
#
#     # 'uploads/7.3.4.31612.GP.apk'
# # __init__(self, tc, device='', account="yk.moon@kinemaster.com", version1='7.4.12.33222.GP.apk',
# #          version2='7.4.17.33410.GP.apk'):
# #
# # def test_seting(self, tc, account="", device='9C241FFBA001L8', version1='7.4.12.33222.GP.apk',
# #                 version2='7.4.17.33410.GP.apk'):
#
# # test = AndroidTest(action, account="yk.moon@kinemaster.com", version1=file_path1, version2=file_path2)
#
# for tc in TCS:
#     test = AndroidTest(tc, account="yk.moon@kinemaster.com", version1=version1, version2=version2)
#     for count in subTC:
#         if onetineTest_cnt == 0 and tc == "downandup":
#             onetineTest_cnt = 1
#         elif onetineTest_cnt == 1 and tc == "downandup":
#             continue
#
#         for device in devices:
#             test.set_device( device)
#             test.set_subTC(count)
#             retvalue = test.perform_actions()
#
#             if not retvalue:
#                 failcount += 1
#             else:
#                 Successcount += 1
#
# print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")
