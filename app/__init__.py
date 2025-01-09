from flask import Flask
from app.functions.preprocess import preprocess_csv
from app.functions.setup_langchain import setuplangchain
from dotenv import load_dotenv
import os
def create_app():
    app = Flask(__name__)
    load_dotenv()
    #start preprocessing
    preprocess_csv()
    #setup langchain prompt
    setuplangchain()
    
    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app