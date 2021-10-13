import requests

def test_get_local_time_check_status_code_equals_200():
    response = requests.get("http://172.17.0.2:8080/api/get_local_time/Taylor")

    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/json'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_get_local_time_check_status_code_equals_500():
    response = requests.get("http://172.17.0.2:8080/api/get_local_time/Todd")

    assert response.status_code == 500
    
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_team_check_status_code_equals_200():
    response = requests.get("http://172.17.0.2:8080/api/team/Taylor")
    
    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/json'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_team_check_status_code_equals_404():
    response = requests.get("http://172.17.0.2:8080/api/team/aweasdasdfaw")
    
    assert response.status_code == 404
    
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_create_teammember_check_status_code_equals_200():
    name = "Test"
    city = "Phoenix"
    country = "America"
    email = "test@testemail.com"
    response = requests.get(f"http://172.17.0.2:8080/create-teammember/{name}?city={city}&country={country}&email={email}")
    
    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/json'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_create_teammember_check_status_code_equals_400():
    name = "Test"
    response = requests.get(f"http://172.17.0.2:8080/api/create-teammember/{name}")
    print(response.headers)
    assert response.status_code == 400
    
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'