# content of test_sample.py
import pytest
import requests


def make_url(path):
    return "http://scrapper:9080/crawl.json?url=http://test_data:80/{path}&spider_name=analyzer".format(path=path)


def test_un_reachable_doc():
    response = requests.get('http://scrapper:9080/crawl.json?url=http://www.inaccessible_link.com&spider_name=analyzer')
    assert 'splash/render.html/response_count/502' in response.json()['stats'].keys()


@pytest.mark.skip(reason="known bug https://github.com/scrapy-plugins/scrapy-splash/issues/146")
def test_path_not_found_doc():
    # FIXME
    response = requests.get(make_url('not_found_path'))
    assert 'splash/render.html/response_count/404' in response.json()['stats'].keys()
    assert 404 == response.json()['items'][0]['_status']


def test_html5_doc():
    response = requests.get(make_url('html5_test_doc.html'))
    expected = [{
        # '_status': 200,
        'external_links': 2,
        'h1': 3,
        'h2': 3,
        'h3': 3,
        'h4': 3,
        'h5': 2,
        'h6': 0,
        'inaccessible_links': 1,
        'internal_links': 2,
        'login-form': False,
        'title': u'Title',
        'version': 'HTML5'
    }]

    assert response.json()['items'] == expected


def test_html4_doc():
    response = requests.get(make_url('html4_test_doc.html'))
    expected = [{
        # '_status': 200,
        'external_links': 0,
        'h1': 0,
        'h2': 0,
        'h3': 0,
        'h4': 0,
        'h5': 0,
        'h6': 0,
        'inaccessible_links': 0,
        'internal_links': 0,
        'login-form': False,
        'title': None,
        'version': 'HTML4'
    }]
    assert response.json()['items'] == expected


def test_xhtml_doc():
    response = requests.get(make_url('xhtml_test_doc.xhtml'))
    expected = [{
        # '_status': 200,
        'external_links': 0,
        'h1': 0,
        'h2': 0,
        'h3': 0,
        'h4': 0,
        'h5': 0,
        'h6': 0,
        'inaccessible_links': 0,
        'internal_links': 0,
        'login-form': False,
        'title': None,
        'version': 'XHTML1'
    }]
    assert response.json()['items'] == expected


def test_non_html_doc():
    response = requests.get(make_url('non_html_doc.txt'))
    expected = [{
        # '_status': 200,
        'external_links': 0,
        'h1': 0,
        'h2': 0,
        'h3': 0,
        'h4': 0,
        'h5': 0,
        'h6': 0,
        'inaccessible_links': 0,
        'internal_links': 0,
        'login-form': False,
        'title': None,
        'version': 'UNKNOWN'
    }]

    assert response.json()['items'] == expected


def test_has_login_form():
    response = requests.get(make_url('test_login_form.html'))
    expected = [{
        # '_status': 200,
        'external_links': 0,
        'h1': 0,
        'h2': 0,
        'h3': 0,
        'h4': 0,
        'h5': 0,
        'h6': 0,
        'inaccessible_links': 0,
        'internal_links': 1,
        'login-form': True,
        'title': None,
        'version': 'HTML5'
    }]

    assert response.json()['items'] == expected

    response = requests.get(make_url('test_signup_form.html'))
    expected = [{
        # '_status': 200,
        'external_links': 0,
        'h1': 0,
        'h2': 0,
        'h3': 0,
        'h4': 0,
        'h5': 0,
        'h6': 0,
        'inaccessible_links': 0,
        'internal_links': 1,
        'login-form': False,
        'title': None,
        'version': 'HTML5'
    }]

    assert response.json()['items'] == expected
