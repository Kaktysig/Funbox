POST_URL = '/visited_links'
GET_URL = '/visited_domains'


def test_post_links(client):
    json_input = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
    json_output = {"status": "ok"}

    response = client.post(POST_URL, json_input)
    assert response.status_code == 201
    assert response.json() == json_output


def test_get_links(client):  # todo: fix time input
    json_output = {"status": "ok"}

    response = client.get(GET_URL + '?from=1545221231&to=1545217638')
    assert response.status_code == 201
    assert response.json() == json_output
