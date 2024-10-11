from androidtc import AndroidTC
import time
from selenium.common.exceptions import WebDriverException

class AtcMix(AndroidTC):
    def __init__(self, tc, device,account,version1,version2,subTC,result_path):
        print("Init AtcMix")
        super().__init__( tc, device,account ,version1,version2,subTC,result_path)
        # self.capabilities = super().capabilities

    def _create_mix_project(self,driver):
        self.driver =driver
        value = "//android.view.ViewGroup[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/mix_item_download\"]"

        el = self.find_button(driver,'xpath', value)
        if not el:
            value = "com.nexstreaming.app.kinemasterfree:id/tv_download"
            el = self.find_button(driver, 'ID', value)
        el.click()
        # el = self.find_button(driver,'ID',
        #                      "com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        # el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button")
        el.click()

        # el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        # el.click()
        # # download 폴더 가기
        el = self.find_button(driver, "xpath",
                                  "//android.widget.FrameLayout[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export\"]/android.widget.ImageView")
        el.click()

        # el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        # el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()

    def install_tc_mix(self, version, tc_url,driver):

        try:
            self.apk_install(version)

            try:
                # 앱 활성화
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
            except WebDriverException as e:
                print(f"앱을 활성화하는 데 실패했습니다: {e}")
                return "fail"

            self.app_install_login(self.account,driver)
            time.sleep(5)
            driver.terminate_app('com.nexstreaming.app.kinemasterfree')
        except Exception as e:  # 모든 예외를 처리하는 대신 Exception 클래스로 구체적인 정보를 출력
            print(f"Error occurred: {e}")

        self.run_adb_command(
            f'adb -s {self.capabilities.get("udid")} shell am start -a android.intent.action.VIEW -d "{tc_url}"')

        self._create_mix_project(driver)

        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
        el.click()
        return el.text

