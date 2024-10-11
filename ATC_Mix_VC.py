from atc_mix import AtcMix
from pathlib import Path

class AtcMixVc(AtcMix):
    def __init__(self, tc, device,account,version1,version2,subTC,result_path):
        print("Init AtcMixVc")
        super().__init__( tc, device,account ,version1,version2,subTC,result_path)
        # self.capabilities = super().capabilities

    def version_compare_tc_mix(self,driver):
        file1 = self.install_tc_mix(self.version1, self.subTC,driver)
        file2 = self.install_tc_mix(self.version2, self.subTC,driver)
        return file1, file2


    def run(self):
        self.driver = self._initialize_appium()
        try:
            version1fileName, version2fileName = self.version_compare_tc_mix(self.driver)
            #self.driver.quit()

            file1 = self.file_download(version1fileName, self.subTC.split("/")[-1], Path(self.version1).name)
            file2 = self.file_download(version2fileName, self.subTC.split("/")[-1], Path(self.version2).name)
            return_val =  self.compare_files(file1, file2, self.subTC.split("/")[-1])
            # file1 ,2 delete
            # os.remove(file1)
            # os.remove(file2)
            return return_val
        except:
            self.take_screenshot(f'/sdcard/DCIM/f{self.subTC.split("/")[-1]}.png', f'fail_{self.tc}_{self.subTC.split("/")[-1]}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            #self.driver.quit()
            return False