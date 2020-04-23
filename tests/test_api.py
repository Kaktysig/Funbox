"""
    -------------------- RU --------------------
    Данные тесты проверяют работу API.

    -------------------- ENG --------------------
    These tests check how the API works.
"""


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


def test_get_links(client):  # todo: fix time input
    json_output = {'status': 'ok'}

    response = client.get(GET_URL + '?from=1545221231&to=1545217638',
                          content_type='application/json',
                          )
    assert response.status_code == 200
    assert response.json() == json_output
