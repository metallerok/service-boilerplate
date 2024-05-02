from src.lib.api_resource import url


def test_sync_api(api_fx):
    URL = url('/api-info')
    result = api_fx.simulate_get(URL)

    assert result.status_code == 200
