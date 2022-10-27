from .base import Model
import jetson.inference
import jetson.utils

from jetson.utils import cudaFont

class Imagenet(Model):
    
	is_running: bool

	def run(self):
		#self.net = jetson.inference.detectNet(self.model_path)
		self.is_running=True

	def stop(self):
		self.is_running=False
        
	def __init__(self,model_path=""):
		
		if not model_path=="":
			self.model_path = model_path
		else:
			self.model_path = "googlenet"
		self.net = jetson.inference.imageNet(self.model_path)
        
	def run_inference(self, img):
		my_inf_result = []
		
		
		print("=================classification=================")
		

		# classify the image
		class_idx, confidence = self.net.Classify(img)
		font = cudaFont()
		# find the object description
		class_desc = self.net.GetClassDesc(class_idx)
		font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)
		my_inf_result.append(img)
		
		
		my_inf_result.append([class_desc, confidence, class_idx])
		print(my_inf_result)
		return my_inf_result

