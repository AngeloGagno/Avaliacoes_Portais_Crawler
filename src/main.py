from cookies.login import Login
from cookies.driver import Driver
from crawler.portal_reviews.request import Portal_Reviews
from crawler.portal_reviews.parser import AirbnbParser
from load.storage.google_drive import Loader
from contract.schema import Validator_Airbnb
from dotenv import load_dotenv
import os

_ = load_dotenv(override=True)
def pipeline_json():

    driver = Driver().get_driver()
    login = Login(driver)
    cookies = login.get_cookies()
    portal_reviews = Portal_Reviews(cookies)
    reviews = portal_reviews.request()['accommodations']
    parse = []
    for accommodation in range(0,len(reviews)):
        reviews_accommodations = AirbnbParser(reviews[accommodation]).parse_accommodation()
        validate = Validator_Airbnb(**reviews_accommodations)
        parse.append(validate.model_dump())

    return parse

def main():
    # Exemplo: chama o Loader com o portal_name passado por argumento
    Loader(portal_name=os.environ.get('PORTAL','airbnb')).upload_parquet(pipeline_json())

if __name__ == "__main__":
    main()