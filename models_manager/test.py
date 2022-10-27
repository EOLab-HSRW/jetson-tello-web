import jetson.utils
from jetson.utils import (cudaDeviceSynchronize,saveImage	)
from manager import Module_Manager
from time import sleep

manager = Module_Manager()
camera = jetson.utils.videoSource("rtp://127.0.0.1:8001",['-input-codec=h264'])#"csi://0")
#display = jetson.utils.videoOutput("rtp://127.0.0.1:8002",['-headless','-output-codec=h264'])
#display = jetson.utils.videoOutput("./image.jpg",['-headless'])#,'-output-codec=h264'])




img = camera.Capture()
detections = manager.process(image=img,task_type="detection") #net.Detect(img)
detections = detections[0]
if len(detections) > 1:
	for detection in detections[1]:
		print(detection[0])

manager.kill()
saveImage("./my_image.jpg",detections[0])
print("image saved")
#display.render(img)
