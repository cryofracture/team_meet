import requests

def test_get_local_time_check_status_code_equals_200():
    response = requests.get("http://172.17.0.2:8080/get_local_time/Taylor")

    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/json'

    assert response.headers['Server'] == 'Werkzeug/2.0.2 Python/3.9.7'

def test_team_check_status_code_equals_200():
    response = requests.get("http://172.17.0.2:8080/team/Taylor")
    
    assert response.status_code == 200
    
    assert response.headers['Content-Type'] == 'application/json'

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