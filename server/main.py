from flask import Flask, request, render_template
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)
api = Api(app)

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

    @app.route("/video-stream", methods=['GET'])
    def video_stream():
        """Serves the main entry point"""
        return "the video is supposed to appear here... not implemented yet"
    

if __name__ == '__main__':

    api.add_resource(Server)
    Server(host='0.0.0.0')
