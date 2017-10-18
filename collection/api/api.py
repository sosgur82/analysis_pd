import math
import sys
from datetime import datetime
from urllib.parse import urlencode

from collection.api.json_request import json_request

SERVICE_KEY = 'gPH8yCYOYdC2iBUdmjYWVjh0ogUpjQxmhnV8x7MW1VW%2FSJGOTcxbMq%2BPQE5UoVnl40lx7LMFT2mJ4QIGHTRsSQ%3D%3D'


def pd_gen_url(endpoint, **params):
    return '%s?%s&serviceKey=%s' % (endpoint, urlencode(params), SERVICE_KEY)


def pd_fetch_tourspot_visitor(
        district1='',
        district2='',
        tourspot='',
        year=0,
        month=0):

    endpoint = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'
    pageno = 1
    hasnext = True

    while hasnext:
        url = pd_gen_url(
            endpoint,
            YM='{0:04d}{1:02d}'.format(year, month),
            SIDO=district1,
            GUNGU=district2,
            RES_NM=tourspot,
            numOfRows=100,
            _type='json',
            pageNo=pageno)
        json_result = json_request(url=url)
        if json_result is None:
            break

        json_response = json_result.get('response')
        json_header = json_response.get('header')
        result_message = json_header.get('resultMsg')

        if 'OK' != result_message:
            print('%s : Error[%s] for Request(%s)' % (datetime.now(), result_message, url), file=sys.stderr)
            break

        json_body = json_response.get('body')

        numofrows = json_body.get('numOfRows')
        totalcount = json_body.get('totalCount')

        if totalcount == 0:
            break

        last_pageno = math.ceil(totalcount/numofrows)
        if pageno == last_pageno:
            hasnext = False
        else:
            pageno += 1

        json_items = json_body.get('items')
        yield json_items.get('item') if isinstance(json_items, dict) else None

def pd_fetch_foreign_visitor(country_code, year, month):
    endpoint2 = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    pageno = 1
    hasnext = True

    while hasnext:
        url = pd_gen_url(
            endpoint2,
            YM='{0:04d}{1:02d}'.format(year, month),
            NAT_CD=country_code,
            ED_CD='E',
            numOfRows=100,
            _type='json',
            pageNo=pageno)
        json_result = json_request(url=url)
        if json_result is None:
            break

        json_response = json_result.get('response')
        json_header = json_response.get('header')
        result_message = json_header.get('resultMsg')

        if 'OK' != result_message:
            print('%s : Error[%s] for Request(%s)' % (datetime.now(), result_message, url), file=sys.stderr)
            break

        json_body = json_response.get('body')

        numofrows = json_body.get('numOfRows')
        totalcount = json_body.get('totalCount')

        if totalcount == 0:
            break

        last_pageno = math.ceil(totalcount / numofrows)
        if pageno == last_pageno:
            hasnext = False
        else:
            pageno += 1

        json_items = json_body.get('items')
        yield json_items.get('item') if isinstance(json_items, dict) else None