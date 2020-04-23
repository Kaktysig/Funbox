"""
    -------------------- RU --------------------
    Данные тесты проверяют работу внутренних функций.

    -------------------- ENG --------------------
    These tests check how the internal functions work.
"""
from link_saver.views import clean_links, remove_not_unique


def test_clean_url():
    link_list = [
        'url.ru', 'https://url.ru', 'http://url.ru',
        'url.ru/some_page/', 'url.ru/', 'url.ru/?getparam=0',
        'url.ru?getparam=0', 'http://url.ru/some_page?getparam=0',
    ]
    assert clean_links(link_list) == ['url.ru' for i in range(len(link_list))]

    link_with_symbols = [
        'https://u-r-l.ru/', 'https://u_r_l.ru/',
    ]
    assert clean_links(link_with_symbols) == ['u-r-l.ru']

    not_link_list = [
        'nonlink.', '.notlink', 'n.o.t.l.i.n.k', 'notlink',
    ]
    assert clean_links(not_link_list) == []


def test_unique_url():
    link_list = [
        'url.ru', 'url.ru', 'theurl.ru', 'url.ru',
    ]
    assert len(remove_not_unique(link_list)) == 2
