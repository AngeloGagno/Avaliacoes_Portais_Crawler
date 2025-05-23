from cookies.login import Login
from cookies.driver import Driver
from crawler.portal_reviews.request import Portal_Reviews
from crawler.portal_reviews.parser import AccommodationParser
import pandas as pd
def main():
    driver = Driver().get_driver()
    login = Login(driver)
    cookies = login.get_cookies()
    portal_reviews = Portal_Reviews(cookies)
    reviews = portal_reviews.request()['accommodations']
    parse = []
    for accommodation in range(0,len(reviews)):
        reviews_accommodations = AccommodationParser(reviews[accommodation]).parse_accommodation()
        print(reviews_accommodations)
        parse.append(reviews_accommodations)
    pd.DataFrame(parse).to_csv('teste.csv')
if __name__ == '__main__':
    main()