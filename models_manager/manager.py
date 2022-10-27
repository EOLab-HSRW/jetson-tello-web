from models.detectnet import DetectNet
from threading import Thread, Event
from multiprocessing import Process, Manager, Queue
from time import sleep
from ctypes import c_bool

class Module_Manager():
	

	def __init__(self,threshold=0.5):
		self.current_thread = None
		self.threshold = threshold
		self.network = None
		self.last_task_type=""
		
		self.thread_running = True
		self.result = []
		self.processed = False
		self.processing_requested = False
		self.img = None
		
		
	
	def process_thread(self,processing_requested,img,result,processed, thread_running, event):
		print("f3")
		network = DetectNet()
		while True:
			print("shit")
			print(processing_requested)
			if processing_requested[0]:
				print("f4")
				result.append(network.run_inference(img))
				print(result)
				processed[0] = True 
				print(processed)
			if event.is_set():#not thread_running:
				print("f5")
				break
			sleep(1)
		
	def kill(self):
		print("initiated process kill")
		self.event.set()
		self.current_thread = None
		#self.current_thread.join()
	
	def process(self, image,task_type="detection"):
		self.event = Event()
		try:
			print("a")
			# check whether this is a different task type
			if not self.last_task_type == task_type:
				print("b")
				# if different, check whether the thread is already running
				if not self.current_thread == None:
					#self.thread_running = False
					self.current_thread.terminate()
					print("c")
				processing_requested = [False]
				processed = [False]
				self.current_thread=Thread(target=self.process_thread, args=(processing_requested,image,self.result, processed, self.thread_running, self.event))
				self.current_thread.start()
				print("f1")
					#if task_type == "detection":
					#	self.network = DetectNet()
					#	print("f2")
					
				#self.current_thread.join()
					# else:
					# the task type is the same
				
				processed[0] = False
				processing_requested[0] = True
				print("set processing_requested  true in main process")				
				print("d")
				while True:
					print("e")
					sleep(1)
					print("processed in main thread")
					print(processed)
					if processed[0]:
						processing_requested[0] = False
						break
				print("f")
		except KeyboardInterrupt:
			self.event.set()
		return self.result
				
