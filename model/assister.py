from model.shared_model import Assister


def get_apprenti_by_id_session(id_session):
    return Assister.query.filter_by(id_session=id_session).all()

