import os
import shutil
import ssl
import time

import ffmpeg
import lpips
import natsort
import torch
from PIL import Image
from torchvision import transforms


class videoComapre:
    def __init__(self, inputVideo1,inputVideo2):
        self.inputVideo1 =inputVideo1
        self.inputVideo2 =inputVideo2
        ssl._create_default_https_context = ssl._create_unverified_context
        # Load LPIPS model
        self.loss_fn = lpips.LPIPS(net='alex',verbose=False)
        # You can use 'alex', 'vgg', or 'squeeze'

        # Define a transform to convert images to tensor and normalize
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),  # Resize to 256x256
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
    
    def extract_frames(self,inputfile):
         
        output_folder = os.path.dirname(inputfile)+'/' +os.path.splitext(os.path.basename(inputfile))[0]
        # output_folder삭제후 새로 생성
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        
        os.makedirs(output_folder)
        time.sleep(2)
        try:
            ffmpeg.input(inputfile).output(os.path.join(output_folder, 'frame_%04d.png')).run(capture_stdout=True, capture_stderr=True)
        except:
            time.sleep(2)

    def compare_frames(self):
        self.extract_frames(self.inputVideo1)
        self.extract_frames(self.inputVideo2)
        frames_dir1 = os.path.dirname(self.inputVideo1)+ '/'+os.path.splitext(os.path.basename(self.inputVideo1))[0]
        frames_dir2 = os.path.dirname(self.inputVideo2)+ '/'+os.path.splitext(os.path.basename(self.inputVideo2))[0]
        # List frame files
        #frames1 = sorted(os.scandir(frames_dir1))
        #frames2 = sorted(os.scandir(frames_dir2))
        frames1 = natsort.natsorted(os.listdir(frames_dir1))
        frames2 = natsort.natsorted(os.listdir(frames_dir2))
        
        # Ensure both directories have the same number of frames
        # print(f' {len(frames1)} LPIPS score: {len(frames2)}')
        #assert len(frames1) == len(frames2), "Different number of frames in each video {}"
        # Compare frames
        total_score = 0
        max_score = 0

        for frame1, frame2 in zip(frames1, frames2):
            if frame1!='.DS_Store' :
                img1 = Image.open(os.path.join(frames_dir1, frame1))
                img2 = Image.open(os.path.join(frames_dir2, frame1))
                

                # Apply transformations
                imgt1 = self.transform(img1).unsqueeze(0)  # Add batch dimension
                imgt2 = self.transform(img2).unsqueeze(0)  # Add batch dimension

                # Compute LPIPS score
                with torch.no_grad():
                    score = self.loss_fn(imgt1, imgt2)
                    if score>=max_score:
                        max_score = score
                        max_frame = frame1
                        Maximg2 =img2
                        Maximg1 = img1
                    # print(f' {frame1} LPIPS score: {score}')
                    total_score += score.item()

        # Calculate average score
        avg_score = total_score / len(frames1)
        # print(f'{os.path.basename(self.inputVideo1)} , {os.path.basename(self.inputVideo2)} Average LPIPS score: {avg_score} Max Score: {max_score} max_frame: {max_frame}')
        if max_score<0.01:
            shutil.rmtree(frames_dir1)
            shutil.rmtree(frames_dir2)
            # os.remove(self.inputVideo1)
            # os.remove(self.inputVideo2)


        return max_score,Maximg2,Maximg1

# lc = lpipsCompare('/Users/yk.moon/Downloads/note.mp4','/Users/yk.moon/Downloads/719.mp4')
# max,img1,img2 = lc.compare_frames()
# img1.save('/Users/yk.moon/Downloads/note.jpg')
# img2.save('/Users/yk.moon/Downloads/719.jpg')
# print(f' {max} LPIPS score: {max}')     

