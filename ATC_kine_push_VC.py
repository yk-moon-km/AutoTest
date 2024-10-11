from atc_kine_push import AtcKinePush
from pathlib import Path

class AtcKinePushVc(AtcKinePush):
    def __init__(self, tc, device,account,version1,version2,subTC,result_path):
        super().__init__( tc, device,account ,version1,version2,subTC,result_path)
        print("Init AtcKinePushVc")
        # self.capabilities = super().capabilities

    def version_compare_tc(self, loacal_file, loacal_path, remote_path, subTC):
        file1 = self.install_tc(self.version1, loacal_file, loacal_path, remote_path,self.driver)
        file2 = self.install_tc(self.version2, loacal_file, loacal_path, remote_path,self.driver)
        return file1, file2


    def run(self):
        self.driver = self._initialize_appium()
        try:
            local_path = f'{self.current_folder}/Test/'
            local_file = f'{self.subTC}'
            remote_path = '/sdcard/Download/AutoTest/'
            version1fileName, version2fileName = self.version_compare_tc( local_file, local_path, remote_path, self.subTC)
            self.delete_files_in_remote_folder(remote_path)
            #self.driver.quit()

            file1 = self.file_download(version1fileName, Path(self.version1).name)
            file2 = self.file_download(version2fileName, Path(self.version2).name)
            return_val =  self.compare_files(file1, file2, self.subTC)
            # file1 ,2 delete
            # os.remove(file1)
            # os.remove(file2)
            return return_val
        except:
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            #self.driver.quit()
            return False