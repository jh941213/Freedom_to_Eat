import ultralytics
from ultralytics import YOLO
import os
import sys
import subprocess

# pip install ultralytics
# pip3 install --upgrade ultralytics

model = YOLO('./static/fridge.pt')

dict_label = {0: '소고기', 1: '달걀', 2: '파', 3: '무', 4: '토마토'}

def predict(save_path):
    result_class = set()
    return_class = []
    if os.path.exists(save_path):
        # results = model.predict(save_path, save=True, save_txt=True)
        results = model(save_path)
        print(len(results), file=sys.stderr)
        for result in results:
            result_class.update(list(map(int, result.boxes.cls.tolist())))

        # dictionary reverse
        for cls in result_class:
            return_class.append(dict_label[cls])
        
    return return_class

def run_detect():
    cmd = ["python", "/home/pi/yolov5ss/detect.py",
    "—weights", "total.pt",
    "—img", "480",
    "—source", "0",
    "—save-txt",
    "—project", "/home/pi/yolov5ss/result"
    ]
    subprocess.run(cmd)
    
    