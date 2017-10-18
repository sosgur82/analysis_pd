import json

import pandas as pd

with open('../__results__/crawling/서울특별시_tourspot_2017_2017.json', 'r', encoding='utf-8') as infile:
    json_string =  infile.read()

    json_data = json.loads(json_string)
    tour_table = pd.DataFrame(json_data, columns=['count_foreigner', 'date', 'tourist_spot'])
    print(tour_table)


