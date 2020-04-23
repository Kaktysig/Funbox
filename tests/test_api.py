"""
    -------------------- RU --------------------
    Данные тесты проверяют работу API.

    -------------------- ENG --------------------
    These tests check how the API works.
"""
import time

import pytest

POST_URL = '/visited_links'
GET_URL = '/visited_domains'


def test_wrong_methods(client):
    response = client.get(POST_URL)
    assert response.status_code == 404
    response = client.post(GET_URL)
    assert response.status_code == 404


def test_check_post_errors(client):
    inputs = [
        None,  # full empty
        {},  # empty json
        b'{link: [[}',  # wrong json
        b'[]',  # non_json
    ]
    for data in inputs:
        response = client.post(POST_URL, data,
                               content_type='application/json')
        assert response.status_code == 400


def test_post_no_links(client):
    json_input = {'links': []}
    json_output = {'status': 'ok'}

    response = client.post(POST_URL, json_input,
                           content_type='application/json')
    assert response.status_code == 201
    assert response.json() == json_output


def test_save_links(client):
    json_input = {
        'links': [
            'https://ya.ru',
            'https://ya.ru?q=123',
            'funbox.ru',
            'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim'
            '-editor ',
        ],
    }
    json_output = {'status': 'ok'}

    response = client.post(POST_URL, json_input,
                           content_type='application/json')
    assert response.status_code == 201
    assert response.json() == json_output


def test_get_empty_links(client):
    json_output = {'status': 'ok', 'domains': []}

    response = client.get(GET_URL + '?from=0&to=1',
                          content_type='application/json',
                          )
    assert response.status_code == 200
    assert response.json() == json_output


@pytest.mark.parametrize('start, end', [
    (None, None),
    ('from=10', None),
    (None, 'to=10'),
    ('from=', 'to='),
    ('from=10', 'to='),
    ('from=', 'to=10'),
    ('from=a', 'to=b'),
])
def test_check_get_errors(client, start, end):
    response = client.get(
        GET_URL + '?{0}&{1}'.format(start, end),
        content_type='application/json',
    )
    assert response.status_code == 400


def test_post_and_get_links(client):
    json_input = {
        'links': [
            'https://ya.ru',
            'https://ya.ru?q=123',
            'funbox.ru',
            'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim'
            '-editor ',
        ],
    }
    curr_time = round(time.time())

    # post
    response = client.post(POST_URL, json_input,
                           content_type='application/json')
    assert response.status_code == 201

    # get
    response = client.get(
        GET_URL + '?from={}&to={}'.format(curr_time, curr_time+200),
        content_type='application/json',
    )
    assert response.status_code == 200
    domains = response.json()['domains']
    assert 'ya.ru' in domains
    assert 'funbox.ru' in domains
    assert 'stackoverflow.com' in domains
    assert domains.count('ya.ru') == 1

    # get somewhere after
    response = client.get(
        GET_URL + '?from={}&to={}'.format(curr_time + 200, curr_time + 500),
        content_type='application/json',
    )
    assert response.status_code == 200
    domains = response.json()['domains']
    assert 'ya.ru' not in domains
    assert 'funbox.ru' not in domains
    assert 'stackoverflow.com' not in domains
