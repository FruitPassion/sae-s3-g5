
def test_auth_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<label id='labelEleve'>Eleve</label>" in response.data
    assert b"<label id='labelProf'>Educateur</label>" in response.data
