import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Fixture pour configurer et nettoyer le navigateur
@pytest.fixture(scope="function")
def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    driver.quit()

def test_checkbox_selection(setup_browser):
    driver = setup_browser
    driver.get("https://demoqa.com/checkbox")
    
    # Ouvrir l'arbre des checkbox
    driver.find_element(By.XPATH, "//button[@title='Toggle']").click()
    time.sleep(1)
    
    # Cliquez sur la flèche pour dérouler 'Desktop'
    driver.find_element(By.XPATH, "//button[@title='Toggle' and following-sibling::label[@for='tree-node-desktop']]").click()
    time.sleep(1)
    
    # Cliquez sur la flèche pour dérouler 'Documents'
    driver.find_element(By.XPATH, "//button[@title='Toggle' and following-sibling::label[@for='tree-node-documents']]").click()
    time.sleep(1)
    
    # Cliquez sur la flèche pour dérouler 'Downloads'
    driver.find_element(By.XPATH, "//button[@title='Toggle' and following-sibling::label[@for='tree-node-downloads']]").click()
    time.sleep(1)
    
    # Liste des checkbox à cliquer
    checkboxes = [
        "//label[@for='tree-node-excelFile']",
        "//label[@for='tree-node-wordFile']",
        "//label[@for='tree-node-office']",
        "//label[@for='tree-node-downloads']",
        "//label[@for='tree-node-documents']",
        "//label[@for='tree-node-desktop']",
        "//label[@for='tree-node-home']"
    ]
    
    # Cliquer sur chaque checkbox après l'avoir fait défiler dans la vue
    for checkbox in checkboxes:
        element = driver.find_element(By.XPATH, checkbox)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Délai pour s'assurer que l'élément est bien visible
        element.click()
        time.sleep(1)  # Ajouter un petit délai pour s'assurer que l'interface se met à jour
    
    # Vérifier le message de résultat
    result = driver.find_element(By.ID, "result").text
    expected_result = "You have selected :\nhome\ndesktop\nnotes\ncommands\ndocuments\nworkspace\nreact\nangular\nveu\noffice\npublic\nprivate\nclassified\ngeneral\ndownloads\nwordFile\nexcelFile"
    
    # Assertion pour vérifier si le test a réussi
    assert result == expected_result, f"Test échoué : attendu '{expected_result}', mais reçu '{result}'."

