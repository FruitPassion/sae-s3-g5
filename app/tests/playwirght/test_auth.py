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


@pytest.mark.parametrize("creation", [["d_apprenti"]], indirect=True)
def test_connexion_apprenti(live_server, page: Page, data_gen: dict):

    page.goto(url_for("auth.choix_connexion", _external=True))
    expect(page.locator("div").filter(has_text="Apprenti").nth(3)).to_be_visible()
    page.locator("div").filter(has_text="Apprenti").nth(3).click()
    expect(page.locator("p").filter(has_text=data_gen["d_formation"]["intitule"])).to_be_visible()
    page.locator("p").filter(has_text=data_gen["d_formation"]["intitule"]).click()
    expect(page.locator(f'p:has-text("{data_gen["d_apprenti"]["prenom"]}  {data_gen["d_apprenti"]["nom"]}")')).to_be_visible()
    page.locator(f'p:has-text("{data_gen["d_apprenti"]["prenom"]}  {data_gen["d_apprenti"]["nom"]}")').click()

    page.locator("#password").evaluate("(element, value) => element.value = value", f"{data_gen['d_apprenti']['password']}")
    page.locator("#send").evaluate("element => element.style.display = 'block'")
    page.locator("#send").click()

    expect(page.get_by_role("listitem")).to_contain_text("Connexion réussie.")
    page.get_by_role("search").click()
    expect(page.get_by_role("listitem")).to_contain_text("Déconnexion réussie.")


@pytest.mark.parametrize("creation", [["d_educ_admin"]], indirect=True)
def test_connexion_personnel_pin(live_server, page: Page, data_gen: dict):

    page.goto(url_for("auth.choix_connexion", _external=True))

    expect(page.locator("div").filter(has_text="Personnel").nth(3)).to_be_visible()
    page.locator("div").filter(has_text="Personnel").nth(3).click()
    expect(page.get_by_role("link", name="connexion pin")).to_be_visible()
    page.get_by_role("link", name="connexion pin").click()
    expect(page.get_by_label("Selectionnez")).to_contain_text(data_gen["d_educ_admin"]["login"])

    for i in range(0, 10):
        expect(page.get_by_role("button").get_by_text(str(i))).to_be_visible()

    pin = [int(i) for i in data_gen["d_educ_admin"]["password"]]
    for i in pin:
        page.locator(f"css=button:has-text('{i}')").click()

    expect(page.get_by_role("button", name="Valider")).to_be_visible()
    page.get_by_role("button", name="Valider").click()
    expect(page.get_by_role("listitem")).to_contain_text("Connexion réussie.")
    page.get_by_role("search").click()
    expect(page.get_by_role("listitem")).to_contain_text("Déconnexion réussie")


@pytest.mark.parametrize("creation", [["d_educ_admin"]], indirect=True)
def test_connexion_personnel_pin_echec(live_server, page: Page, data_gen: dict):
    """
    Test de connexion avec un pin incorrect
    """
    data_gen["d_educ_admin"]["password"] = "999999"
    connexion_personnel_pin(page, data_gen["d_educ_admin"])
    expect(page.get_by_role("listitem")).to_contain_text("Compte inconnu ou mot de passe invalide")


@pytest.mark.parametrize("creation", [["d_educ_admin"]], indirect=True)
def test_connexion_personnel_pin_blocage(live_server, page: Page, data_gen: dict):
    """
    Test de connexion avec un pin incorrect
    """
    data_gen["d_educ_admin"]["password"] = "999999"
    for _ in range(0, 3):
        page = connexion_personnel_mdp(page, data_gen["d_educ_admin"])
    expect(page.get_by_role("listitem")).to_contain_text("Compte bloqué, contacter un admin")


@pytest.mark.parametrize("creation", [["d_super_admin"]], indirect=True)
def test_connexion_personnel_mdp(live_server, page: Page, data_gen: dict):
    """
    Test de connexion avec un mot de passe et un login correct
    """
    page.goto(url_for("auth.choix_connexion", _external=True))
    expect(page.locator("div").filter(has_text="Personnel").nth(3)).to_be_visible()

    page.locator("div").filter(has_text="Personnel").nth(3).click()
    page.get_by_role("link", name="connexion mdp").click()
    page.locator("#login").click()
    page.locator("#login").fill(data_gen["d_super_admin"]["login"])
    page.locator("#password").click()
    page.locator("#password").fill(data_gen["d_super_admin"]["password"])
    page.get_by_role("button", name="Se connecter").click()
    expect(page.get_by_role("listitem")).to_contain_text("Connexion réussie.")
    page.get_by_role("search").click()
    expect(page.get_by_role("listitem")).to_contain_text("Déconnexion réussie.")


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


@pytest.mark.parametrize("creation", [["d_educ_admin"]], indirect=True)
def test_connexion_personnel_mdp_blocage(live_server, page: Page, data_gen: dict):
    """
    Test de connexion avec un mot de passe incorrect jusqu'à blocage du compte
    """
    data_gen["d_educ_admin"]["password"] = fake.password(length=10)
    for _ in range(0, 3):
        page = connexion_personnel_mdp(page, data_gen["d_educ_admin"])
    expect(page.get_by_role("listitem")).to_contain_text("Compte bloqué, contacter un admin")


def test_tear_down():
    assert 1
