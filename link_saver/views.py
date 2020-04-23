import json
import re
import time

from urllib.parse import urlparse

import redis
from django.http import (
    HttpResponseNotFound,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from Funbox.settings import REDIS_HOST, REDIS_POST

url_regex = re.compile(
    r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}$')
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_POST, db=0)


def clean_links(links_list) -> list:
    """
    -------------------- RU --------------------
    Выделяет домен из ссылок.

    -------------------- ENG --------------------
    This function takes the domain of the links

    EXAMPLE: https://url.ru/some_page?get_param=param  -> url.ru

    :return: list of links
    """
    clean_list = []
    for index in range(len(links_list)):
        link = links_list[index]
        parsed = urlparse(link)
        link = parsed.netloc or parsed.path
        link = link.split('/')[0]
        if re.match(url_regex, link) is not None:
            clean_list.append(link)
    return clean_list


def remove_not_unique(links_list) -> list:
    """
    -------------------- RU --------------------
    Оставляет только уникальные ссылки в списке.

    -------------------- ENG --------------------
    Leaves only unique links in the list.

    :return: list of links
    """
    if len(links_list) > 0:
        links_list.sort()
        unique_links = [links_list[0]]
        i, j = 1, 0
        while i < len(links_list):
            if unique_links[j] != links_list[i]:
                unique_links.append(links_list[i])
                j += 1
            i += 1
        return unique_links
    return links_list


@csrf_exempt
def save_links(request):
    if request.method == 'POST':
        try:
            content = json.loads(request.body)
            cleaned_links = clean_links(content['links'])
            unique_links = remove_not_unique(cleaned_links)

            # saving in redis
            if unique_links:
                curr_time = round(time.time())
                r.sadd(curr_time, *unique_links)

            return JsonResponse(data={'status': 'ok'}, status=201)
        except KeyError:
            error_content = 'List "links" cant be empty!'
        except Exception as e:
            error_content = e

        return HttpResponseBadRequest(content=error_content)
    return HttpResponseNotFound()


@csrf_exempt
def print_links(request):
    if request.method == 'GET':
        try:
            start_time = int(request.GET.get('from'))
            end_time = int(request.GET.get('to')) + 1
            links = set()

            # get from redis
            for curr_time in range(start_time, end_time):
                if r.smembers(str(curr_time)):
                    links.update(r.smembers(str(curr_time)))

            domains = [link.decode('utf-8') for link in links]
            return JsonResponse(
                data={'status': 'ok',
                      'domains': domains},
                status=200,
            )
        except Exception as e:
            return HttpResponseBadRequest(content=e)
    return HttpResponseNotFound()
