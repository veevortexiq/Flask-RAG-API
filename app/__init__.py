from flask import Flask
from app.functions.preprocess import preprocess_csv
from app.functions.setup_langchain import setuplangchain
def create_app():
    app = Flask(__name__)
    
    #start preprocessing
    preprocess_csv()
    #setup langchain prompt
    setuplangchain()
    
    # Import and register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app