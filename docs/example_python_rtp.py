import jetson.inference
import jetson.utils
from jetson.utils import (cudaDeviceSynchronize,saveImage	)

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("rtp://127.0.0.1:8001",['-input-codec=h264'])#"csi://0")
#display = jetson.utils.videoOutput("rtp://127.0.0.1:8002",['-headless','-output-codec=h264'])
#display = jetson.utils.videoOutput("./image.jpg",['-headless'])#,'-output-codec=h264'])



while True:
	img = camera.Capture()
	detections = net.Detect(img)
	for detection in detections:
		print(net.GetClassDesc(detection.ClassID))
	saveImage("./my_image.jpg",img)
	#display.render(img)


