from base import Model
import jetson.inference
import jetson.utils

class DetectNet(Model):
    
    is_running: bool

    def run(self):
        self.net = jetson.inference.detectNet(self.model_path)
        self.is_running=True

    def stop(self):
        self.is_running=False

    def __init__(self,model_path=""):
        if not model_path=="":
            self.model_path = model_path
        else:
            self.model_path = "ssd-mobilenet-v2"
        

    def run_inference(self, img):
        my_detections = []
        detections = self.net.Detect(img)

        for detection in detections:
            my_detections.append([net.GetClassDesc(detection.ClassID),detection.Confidence,round(detection.Top),round(detection.Bottom),
            round(detection.Left), round(detection.Right)])
            my_detections.append(img)
        
        return my_detections

