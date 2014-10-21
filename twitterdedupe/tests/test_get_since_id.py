import pytest
from mock import Mock


@pytest.fixture
def get_since_id():
    from .. import get_since_id
    return get_since_id


@pytest.fixture
def api():
    from mock import Mock
    return Mock()


def test_no_tweets(get_since_id, api):
    api.user_timeline = Mock(return_value=[])
    status_id = get_since_id(api, "cmheisel")
    assert status_id == 1


def test_one_tweet(get_since_id, api):
    mock_timeline = [
        Mock(),
    ]
    i = 111
    for s in mock_timeline:
        s.id = i
        i += 1
    api.user_timeline = Mock(return_value=mock_timeline)
    status_id = get_since_id(api, "cmheisel")
    assert status_id == 111


def test_returns_last_id(get_since_id, api):
    mock_timeline = [
        Mock(),
        Mock(),
        Mock(),
    ]
    i = 111
    for s in mock_timeline:
        s.id = i
        i += 1
    api.user_timeline = Mock(return_value=mock_timeline)
    status_id = get_since_id(api, "cmheisel")
    assert status_id == 113
