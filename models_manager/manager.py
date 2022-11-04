from models.detectnet import DetectNet
from models.imagenet import Imagenet
from threading import Thread, Event
from multiprocessing import Process, Manager, Queue
from time import sleep
from ctypes import c_bool

class ModelManager():
	# the list of supported models with additional information
	supported_models ={
		"detection":{
			"networks":[
				"ssd-mobilenet-v2"
			]
		},
		"classification":{
			"networks":[
				"googlenet"
			]
		}
	}

	def __init__(self):
		self.current_thread = None # saves current thread of manager
		self.last_task_type="" # saves the last task type of manager
		
		self.result = [] # the inference result
		self.processed = [False] # flag to notify main thread about child thread completion
		self.processing_requested = [False] # flag to request inference in child thread
		self.inp = [None] # input image
		self.event = Event() # trigger to quit child thread
		
		
	def process_thread(self,processing_requested,inp,result,processed, event, task_type):
		"""
			thread target for inference
	
			attributes for data exchange between the threads
			
			processing_requested - flag to request inference in child thread
			inp - input image
			result - flag to request inference in child thread
			processed - flag to notify main thread about child thread completion
			event - trigger to quit child thread
			task_type - choose network
		"""
		# choose network to load
		if task_type == "detection":
			network = DetectNet()
		elif task_type == "classification":
			network = Imagenet()
			
		while True:
			# if processing was requested by main thread
			if processing_requested[0]:
				# run inference and append to result
				result.append(network.run_inference(inp[0]))
				# print result
				print("=====Result in child=====")
				print(result)
				print("set processed true in child")
				# set processed flag to True to notify main thread
				processed[0] = True
			# trigger to kill child process
			if event.is_set():
				print("killed child process "+ task_type)
				break	

	def kill(self):
		"""method kills the current thread"""
		print("initiated process kill")
		# set trigger
		self.event.set()
		self.current_thread = None
	
	def process(self, image,task_type="detection"):
		"""main processing method for inference"""
		# clear previous calls' result
		self.result.clear()
		# try catch for handling keyboard interrupt
		try:
			# check whether this is a different task type
			if not self.last_task_type == task_type:
				# if different, check whether the thread is already running
				if not self.current_thread == None:
					self.event.set() # set event to stop the currently running thread
					self.current_thread.join() # wait until the child thread quits
					self.current_thread = None
					self.event.clear() # reset trigger for future tasks
				
				# create new child thread and start it
				self.current_thread=Thread(target=self.process_thread, args=(self.processing_requested,self.inp,self.result, self.processed, self.event, task_type))
				self.current_thread.start()
				print("created child process "+ task_type)
				# save last task type in manager
				self.last_task_type = task_type
				
			# set input image and request/ response flags
			self.inp[0] = image
			self.processed[0] = False
			self.processing_requested[0] = True
			
			print("set processing_requested  true in main process")
			# wait while request is processed in child
			while True:
				if self.processed[0]:
					# cancel processing request
					self.processing_requested[0] = False
					break
		except KeyboardInterrupt:
			# kill the child thread
			self.event.set()
		
		# return inference results
		print("=======Results=======")
		print(self.result)
		return_result = self.result[0]
		return return_result
				
