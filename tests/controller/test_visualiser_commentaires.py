from flask import url_for

def test_visualisation_commentaires(eleve): 
    response = eleve.get(url_for("cip.visualiser-commentaires"))
    assert response.status_code == 200
    assert response.request.path == "/cip/<apprenti>/<idFiche>/visualiser-commentaires"

    html = response.get_data(as_text=True)
    print(html)

    # mettre tous les identifiants de la page visualiser-commentaires
    listeids = ['"id1"', '"id2"', '"id3"']
    for name in listeids:
        assert 'id=' + name in html

