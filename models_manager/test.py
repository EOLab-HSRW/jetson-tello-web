import jetson.utils
from jetson.utils import (cudaDeviceSynchronize,saveImage	)
from manager import ModelManager
from time import sleep

manager = ModelManager()
camera = jetson.utils.videoSource("rtp://127.0.0.1:8001",['-input-codec=h264'])#"csi://0")
#display = jetson.utils.videoOutput("rtp://127.0.0.1:8002",['-headless','-output-codec=h264'])
#display = jetson.utils.videoOutput("./image.jpg",['-headless'])#,'-output-codec=h264'])



# take image from camera
img = camera.Capture()
# get detection from manager
detections = manager.process(image=img,task_type="detection")
if len(detections) > 1:
	detection_result=detections[1:]
	for detection in detection_result:
		print(detection)

saveImage("./my_image1.jpg",detections[0])
print("image saved")



img = camera.Capture()
detections = manager.process(image=img,task_type="detection")
if len(detections) > 1:
	detection_result=detections[1:]
	for detection in detection_result:
		print(detection)
		
saveImage("./my_image2.jpg",detections[0])
print("image saved")


img = camera.Capture()
classification_results = manager.process(image=img,task_type="classification")
if len(classification_results) > 1:
	classification_results_data=classification_results[1:]
	for classification_result_d in classification_results_data:
		print(classification_result_d)
		
saveImage("./my_image3.jpg",classification_results[0])
print("image saved")
manager.kill()

#display.render(img)
