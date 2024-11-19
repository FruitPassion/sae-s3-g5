import pytest
from faker import Faker
from flask import url_for
from playwright.sync_api import Page, expect
from tests.utils import (
    connexion_personnel_mdp,
    connexion_personnel_pin,
    restitue_classes,
)

fake = Faker(["fr_FR"])


@pytest.mark.parametrize("creation", [["d_super_admin"]], indirect=True)
def test_connexion_personnel_mdp_echec(live_server, page: Page, data_gen: dict):
    """
    Test de connexion avec un mot de passe incorrect et un login correct
    """
    data_gen["d_super_admin"]["password"] = fake.password(length=10)
    page = connexion_personnel_mdp(page, data_gen["d_super_admin"])
    expect(page.get_by_role("listitem")).to_contain_text("Compte inconnu ou mot de passe invalide")

    data_gen["d_super_admin"]["login"] = "MAO10"
    page = connexion_personnel_mdp(page, data_gen["d_super_admin"])
    expect(page.get_by_role("listitem")).to_contain_text("Compte inconnu ou mot de passe invalide")


def test_tear_down():
    assert 1
