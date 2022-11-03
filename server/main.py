from flask import Flask, request, render_template, jsonify, send_file
from flask_restful import Api, Resource
from flask_cors import CORS
import sys
import jetson.utils
# appended models manager folder to sys path to be able to import from it
sys.path.append("..")
sys.path.append("../models_manager")
# import ModelManager
from models_manager.manager import ModelManager

app = Flask(__name__, template_folder='templates')
CORS(app)
api = Api(app)

# ModelManager instance
manager = ModelManager()

# global camera and instance variables, will be changed in launch endpoint
camera = None
camera_source =""
model = ""

class Server(Resource):

    def __init__(self, 
                 host: str = '127.0.0.1', 
                 port: int = 4040,
                 debug: bool = True):
        """
            class constructor
            :param host: set host ip for Flask server
            :param port: set port
            :param debug: set debug mode True or False
        """
        self.HOST = host
        self.PORT = port
        self.DEBUG = debug

        app.run(host=self.HOST, port=self.PORT, debug=self.DEBUG)

    @app.route("/", methods=['GET'])
    def index():
        """Serves the main entry point"""
        return render_template("index.html")

    @app.route("/launch", methods=['POST'])
    def launch():
        global model
        global camera
        global camera_source


        if not request.form['model'] in ModelManager.supported_models:
            return {"error": request.form['model']+" model is not supported"}
        # read request body params
        model = request.form['model']
        input = request.form['input']

        # check input parameter
        if input == "image": # if it is image, read file from request
            image = request.files.get('image','')
            image.save('./MyImage.jpg') # save it in filesystem
            image_cuda = jetson.utils.loadImage('./MyImage.jpg') # convert it into cuda image
        else:
            if not camera_source == input: # if camera source is different from the last used
                camera =jetson.utils.videoSource(input) # init new camera instance with new input
                camera_source=input # save the last camera source
            image_cuda = camera.Capture()  # get new cuda image from camera

        detections=manager.process(image=image_cuda,task_type=model) # send cuda image and model to manager
        if len(detections)>0:# if something was detected 
            jetson.utils.saveImageRGBA('./MyImage_det.jpg',detections[0]) # save image
        """Serves the main entry point"""

        
        return send_file('./MyImage_det.jpg')# send response with image
        #render_template("index.html")
    
    @app.route("/state", methods=['GET'])
    def state():
        global model
        global camera_source
        return {"running_model":model,"input_source":camera_source}
    
    @app.route("/info", methods=['GET'])
    def info():
        return ModelManager.supported_models

    @app.route("/video-stream", methods=['GET'])
    def video_stream():
        """Serves the main entry point"""
        return "the video is supposed to appear here... not implemented yet"
    

if __name__ == '__main__':

    api.add_resource(Server)
    Server(host='0.0.0.0')
