def test_health_check(app, client):
    res = client.get('/health_check')
    assert res.status_code == 200