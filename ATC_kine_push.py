from  androidtc import AndroidTC
import subprocess
from selenium.common.exceptions import WebDriverException


class AtcKinePush(AndroidTC):
    def __init__(self, tc, device,account,version1,version2,subTC,result_path):
        print("Init AtcKinePush")
        super().__init__( tc, device,account ,version1,version2,subTC,result_path)

        # self.capabilities = super().capabilities



    def install_tc(self, version, filename, localpath, remotepath,driver):
        self.driver = driver
        self.apk_install(version)
        try:
            self._push_file(localpath + filename, remotepath + filename)
        except subprocess.CalledProcessError as e:
            print(f"File upload failed: {e.stderr.decode('utf-8')}")
            return "fail"

        try:
            # 앱 활성화
            driver.activate_app('com.nexstreaming.app.kinemasterfree')
        except WebDriverException as e:
            print(f"앱을 활성화하는 데 실패했습니다: {e}")
            return "fail"
        # self.run_adb_command(
        #     f'adb -s {self.capabilities.get("udid")} shell am start -a android.intent.action.VIEW"')

        self.app_install_login(self.account,driver)
        self._create_new_project(driver)

        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
        el.click()
        return el.text



    def _create_new_project(self,driver):
        self.driver = driver
        el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
        el.click()

        el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(1)")
        el.click()
        el = self.find_button(driver,'ID',
                             "com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        el.click()
        # download 폴더 가기


        el = self.find_button(driver,'UI',"new UiSelector().description(\"Show roots\")")
        if el:
            el.click()
        udid = self.capabilities.get("udid")
        deviceName= self.get_device_name_by_udid(udid)
        device_value =  f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"{deviceName}\"]'
        el = self.find_button(driver,'xpath',device_value)
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_list\")")
        if not el:
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_grid\")")
            if el:
                el.click()

        el = self.find_button(driver,'UI',"new UiSelector().text(\"Download\")")
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().text(\"AutoTest\")")
        el.click()


        tc_string = f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"{self.subTC}\"]'
        el = self.find_button(driver,'xpath', tc_string)
        if el:
            el.click()

        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()

        # el = self.find_button(driver, 'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        # el.click()
        # el = self.find_button(driver, 'ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        # el.click()
        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        if el:
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            if el:
                el.click()

