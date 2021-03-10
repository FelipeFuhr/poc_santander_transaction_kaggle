def test_app_created(app):
    assert app.name == 'app'

def test_health_check(client):
    res = client.get('/health_check')
    assert res.status_code == 200
