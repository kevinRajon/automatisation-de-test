import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture(scope="function")
def driver():
    # Configuration des options Chrome pour désactiver la popup de sélection du moteur de recherche
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    # Initialisation du driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


def test_form_submission(driver):
    # Ouvrir la page de test
    driver.get("https://demoqa.com/text-box")
    
    # Remplir les champs du formulaire
    driver.find_element(By.ID, "userName").send_keys("John Doe")
    driver.find_element(By.ID, "userEmail").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "currentAddress").send_keys("123 Rue de Paris")
    driver.find_element(By.ID, "permanentAddress").send_keys("456 Rue de Lyon")
    
    # Défilement vers le bouton submit pour le rendre visible
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    
    # Soumettre le formulaire
    submit_button.click()
    
    # Vérifier les valeurs saisies
    assert "John Doe" in driver.find_element(By.ID, "name").text
    assert "john.doe@example.com" in driver.find_element(By.ID, "email").text
    assert "123 Rue de Paris" in driver.find_element(By.ID, "output").text
    assert "456 Rue de Lyon" in driver.find_element(By.ID, "output").text
