from flask import Flask
import sys
from census_income.exception import Acip_Exception
from census_income.logger import logging

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    try:
        pass
    except Exception as e:
        housing = Acip_Exception(e,sys)
        logging.info(housing.error_message)
        logging.info("This is a info message")
        return '<h1>Checking the functionality.</h1>'

if __name__=="__main__":
    app.run(debug=True)