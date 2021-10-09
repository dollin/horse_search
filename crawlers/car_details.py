
import json
import logging
import re


def instance(car_details):
    return CarDetails(car_details['title'].strip(),
                      car_details['sub_title'],
                      car_details['details'],
                      car_details['seller'],
                      car_details['seller_location'],
                      car_details['price'],
                      car_details['year'],
                      car_details['mileage'],
                      car_details['relevance'])


def write_to_file(title, sub_title, details, seller, seller_location, price, year, mileage, car_details_file):
    car_details = CarDetails(title=title,
                             sub_title=sub_title,
                             details=details,
                             seller=seller,
                             seller_location=seller_location,
                             price=price,
                             year=year,
                             mileage=mileage)
    logging.info(car_details)
    car_details_file.write(json.dumps(car_details.__dict__, indent=4))
    car_details_file.write(',')


class CarDetails:

    def __init__(self, title, sub_title, details, seller, seller_location, price, year, mileage, relevance=0):
        self.title = title
        self.sub_title = sub_title
        self.details = details
        self.seller = seller
        self.seller_location = seller_location
        self.price = price
        self.year = year
        self.mileage = mileage
        self.relevance = relevance

    def __hash__(self):
        return hash(self.title) ^ hash(self.price) ^ hash(self.seller)

    def __eq__(self, other):
        return self.title == other.title \
               and self.price == other.price \
               and self.seller == other.seller

    def __str__(self):
        return '{\n\ttitle: ' + self.title \
               + '\n\tsub_title: ' + self.sub_title \
               + '\n\tdetails: ' + ",".join(self.details) \
               + '\n\tseller: ' + self.seller \
               + '\n\tseller_location: ' + self.seller_location \
               + '\n\tprice: ' + self.price \
               + '\n\tyear: ' + str(self.year) \
               + '\n\tmileage: ' + str(self.mileage) \
               + '\n}'

    def weight(self):
        return float(re.sub(r'\D', '',  self.mileage)) / (2021 - self.year) * 1000 / float(re.sub(r'\D', '', self.price))
