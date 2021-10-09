
import configparser
import crawlers.car_details
import json


cache = set()

config = configparser.ConfigParser()
config.read('../resources/rules.ini')


def populate_cache():
    with open('../data/car_details.json', 'r', encoding='utf-8') as car_details_json:
        cars = json.load(car_details_json)

    for car in cars:
        include = True

        for key in 'title', 'sub_title', 'price', 'details':
            if config[key]['exclude'] not in '':
                for ex in config[key]['exclude'].split(','):
                    if ex.strip() in ''.join(car[key]).lower():
                        include = False
                        break

            weights = config[key]['weights'].split(',')
            for i, priority in enumerate(['high', 'medium', 'low']):
                for key_priority in config[key][priority].split(','):
                    if type(car[key]) is str and key_priority.strip().lower() in car[key].lower():
                        car['relevance'] += int(weights[i].strip())
                    elif type(car[key]) is list and key_priority.strip().lower() in ''.join(car[key]).lower():
                        car['relevance'] += int(weights[i].strip())
        if include:
            hp = crawlers.car_details.instance(car)
            cache.add(hp)


def sort_cache():
    return sorted(cache, key=lambda car: (car.relevance, car.weight(), car.year, -1 * car.mileage, car.price))


def print_summary():
    count = len(list(filter(lambda hp: hp.relevance > 1 and hp.year > 0, cache)))
    print('#  ; match ; weight; price   ; year; miles  ; '
          'title                                                           ; sub title                       ;'
          'seller          ; location                        ; details')
    for i, car in enumerate(filter(lambda hp: hp.relevance > 1 and hp.year > 0, sort_cache())):
        print('{:3}; {:06d}; {:6.0f}; {:7}; {:4}; {:7}; {: <64}; {:32}; {:16}; {:32}; [{}]'.format(
            count - i,
            car.relevance,
            car.weight(),
            car.price.strip(),
            car.year,
            car.mileage,
            car.title.strip()[0:64],
            car.sub_title,
            car.seller[0:16],
            car.seller_location,
            ', '.join(car.details)
        ))
    print(f'count: [{count}]')


if __name__ == "__main__":
    populate_cache()
    print_summary()
