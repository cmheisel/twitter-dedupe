import pytest
from mock import Mock


@pytest.fixture
def meth():
    from twitterdedupe import lengthen_url
    return lengthen_url


def reqlib(url):
    reqlib = Mock(name="requests")
    response = Mock(name="response")
    response.url = url
    reqlib.get.return_value = response

    r = reqlib.get(url)
    assert r.url == url
    return reqlib


def test_normal_url(meth):
    url = "http://www.chrisheisel.com/"
    req = reqlib(url)
    result = meth(url, req)
    assert result == url


def test_sneaky_url(meth):
    url = "http://www.chrisheisel.com/?wpsrc=fol_tw"
    expected = "http://www.chrisheisel.com/"
    req = reqlib(url)
    result = meth(url, req)
    assert result == expected
