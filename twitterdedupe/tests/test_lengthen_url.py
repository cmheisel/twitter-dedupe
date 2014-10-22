import pytest
from mock import Mock


@pytest.fixture
def meth():
    from twitterdedupe import lengthen_url
    return lengthen_url


def reqlib(url):
    reqlib = Mock()
    retval = Mock()
    retval.url.return_value = url
    reqlib.get.return_value = retval


def test_normal_url(meth):
    url = "http://chrisheisel.com/"
    req = reqlib(url)
    result = meth(url, req)
    assert result == url
