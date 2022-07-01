from census_income.pipeline.pipeline import Pipeline
from census_income.exception import Acip_Exception
from census_income.logger import logging
def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()