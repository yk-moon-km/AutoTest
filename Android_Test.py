
from datetime import datetime
from adbutils import device
import os

# TestClass
from ATC_kine_push_VC import AtcKinePushVc
from ATC_Kine_push_RG import AtcKinePushRg
from ATC_kine_push_reverse import AtcKinePushReverse
from ATC_Mix_VC import AtcMixVc
from ATC_Mix_RG import AtcMixRg
from ATC_Server import ATC_Server

from videoCompare import videoComapre


class AndroidTest:
    def __init__(self, tc,account ,version,folder ,device=""):
        print(f"AndroidTest Init")
        self.device = device
        self.tc = tc
        self.version = version
        self.folder = folder
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.current_folder = os.path.dirname(__file__)
        self.result_folder = f"{tc}_{current_time}"
        self.result_path = f"{self.current_folder}/Result/{self.result_folder}/"
        self.account = account
        result_prepath = f"{self.current_folder}/Result/"
        if not os.path.exists(result_prepath):
            os.mkdir(result_prepath)
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def set_subTC(self,subTC):
        test_type, test_case = subTC.split(',')
        self.subTC = test_case
        self.test_type = test_type

    def set_device(self, device):
        self.device = device


    def perform_actions(self,count=False):
        print(f"perform_actions  {self.tc} {self.test_type} {self.device}, {self.account},{self.version},{self.folder},{self.subTC},{self.result_path}")
        if self.test_type == 'kine':
            if self.tc == 'versioncompare':
                test= AtcKinePushVc("versioncompare_kine",self.device, self.account,self.version,self.folder,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcKinePushRg("regression_kine",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'reverse':
                test = AtcKinePushReverse("reverse_kine",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        elif self.test_type == 'mix':
            if self.tc == 'versioncompare':
                test= AtcMixVc("versioncompare_mix",self.device, self.account,self.version,self.folder,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcMixRg("regression_mix",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        elif self.test_type == 'server':
            if self.tc == 'server':
                test= ATC_Server("server",self.device, self.account,self.version,self.folder,self.subTC,self.result_path,count)
                return test.run()
        else:
            return "error"



# devices = ["9C241FFBA001L8"]#15151FDD4001GT"]# , "1A051FDF600BG0"]
# devices = ["15151FDD4001GT"]
# devices = ["15151FDD4001GT"]#15151FDD4001GT"]# , "9C241FFBA001L8"]
# platform = ["Android", "iOS"]
# TCS = ["versioncompare"]
# TCS = ["server"]

# # subTC = ["Test1"]
# # TCS = ["regression_kine"]
# # subTC = ["Test1"]
# # TCS = ["regression"]

# subTC = ['kine,KM-11790.kine']
# subTC = ['jira,key=']
# subTC = ['server,kr']

# # subTC = ['mix,https://kine.to/template/66e03a361098d00c48cf8933','kine,20240726.kine']
# FOLDER_PATH = 'uploads'
# failcount = 0
# Successcount = 0
# onetineTest_cnt = 0
# version1='uploads/7.5.1.33830.GP.apk'
# version2='uploads/7.5.16.34132.GP.apk'
# # version=['7.5.1.33830.GP.apk','7.5.16.34132.GP.apk','7.4.17.33410.GP.apk']
# # version=['7.5.16.34132.GP.apk','7.5.16.34132.GP1.apk']
# version=['7.5.17.34152.GP.apk']#,'7.4.17.33410.GP.apk']
#     # 'uploads/7.3.4.31612.GP.apk'
# # __init__(self, tc, device='', account="yk.moon@kinemaster.com", version1='7.4.12.33222.GP.apk',
# #          version2='7.4.17.33410.GP.apk'):
# #
# # def test_seting(self, tc, account="", device='9C241FFBA001L8', version1='7.4.12.33222.GP.apk',
# #                 version2='7.4.17.33410.GP.apk'):

# # test = AndroidTest(action, account="yk.moon@kinemaster.com", version1=file_path1, version2=file_path2)

# # file1 = './Test/7.5.1.33830.GP.apk_15151FDD4001GT_0.mp4'
# # file2 = './Test/7.5.16.34132.GP.apk_15151FDD4001GT_0.mp4'


# # lc = videoComapre(file1, file2)
# # print("compare_files1")
# # max_val, img1, img2 = lc.compare_audio()




# count =0
# retvalue = True
# for tc in TCS:
#     test = AndroidTest(tc, account="yk.moon@kinemaster.com", version=version, folder=FOLDER_PATH)
#     for count in subTC:
    
#         if onetineTest_cnt == 0 and tc == "downandup":
#             onetineTest_cnt = 1
#         elif onetineTest_cnt == 1 and tc == "downandup":
#             continue

#         for device in devices:
#             test.set_device( device)
#             test.set_subTC(count)
#             for c in range(1):
#                 try:
#                     retvalue = test.perform_actions(c)
#                     # retvalue = test.perform_actions()
#                 except Exception as e:
#                     print(f"예외 발생: {e}")

#                 if not retvalue:
#                     failcount += 1
#                 else:
#                     Successcount += 1
                

# print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")

