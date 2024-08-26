import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    # Configuration des options Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("headless")
    

    # Initialisation du driver
    driver = webdriver.Chrome(options=chrome_options)
    yield driver  # Retourne le driver pour les tests
    driver.quit()  # Ferme le navigateur après les tests


def test_radio_buttons(driver):
    # Ouvrir la page
    driver.get("https://demoqa.com/radio-button")

    # Attendre un peu que la page se charge (optionnel)
    time.sleep(2)

    # Trouver les boutons radio
    yes_radio = driver.find_element(By.XPATH, "//label[@for='yesRadio']")
    impressive_radio = driver.find_element(By.XPATH, "//label[@for='impressiveRadio']")
    no_radio_disabled = driver.find_element(By.XPATH, "//input[@id='noRadio']")

    # Cliquer sur le bouton radio "Yes" et vérifier la sélection
    yes_radio.click()
    time.sleep(1)
    selected_text = driver.find_element(By.CLASS_NAME, "text-success").text
    assert selected_text == "Yes", f"Expected 'Yes', but got {selected_text}"
    print("Test du bouton 'Yes' réussi.")

    # Cliquer sur le bouton radio "Impressive" et vérifier la sélection
    impressive_radio.click()
    time.sleep(1)
    selected_text = driver.find_element(By.CLASS_NAME, "text-success").text
    assert selected_text == "Impressive", f"Expected 'Impressive', but got {selected_text}"
    print("Test du bouton 'Impressive' réussi.")

    # Vérifier que le bouton radio "No" est désactivé
    assert not no_radio_disabled.is_enabled(), "Le bouton 'No' devrait être désactivé."
    print("Vérification du bouton 'No' désactivé réussie.")
