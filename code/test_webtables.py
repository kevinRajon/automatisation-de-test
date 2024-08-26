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

def test_add_new_user(setup_browser):
    driver = setup_browser
    driver.get("https://demoqa.com/webtables")

    # Ajouter un nouvel utilisateur
    driver.find_element(By.ID, "addNewRecordButton").click()
    driver.find_element(By.ID, "firstName").send_keys("Kevin")
    driver.find_element(By.ID, "lastName").send_keys("Rajon")
    driver.find_element(By.ID, "userEmail").send_keys("kr@mail.fr")
    driver.find_element(By.ID, "age").send_keys("36")
    driver.find_element(By.ID, "salary").send_keys("50000")
    driver.find_element(By.ID, "department").send_keys("IT")
    driver.find_element(By.ID, "submit").click()

    # Vérification des informations dans la liste des utilisateurs
    rows = driver.find_elements(By.CLASS_NAME, "rt-tr-group")
    user_info = ["Kevin", "Rajon", "kr@mail.fr", "36", "50000", "IT"]

    # Parcourir les lignes pour trouver la correspondance
    found = False
    for row in rows:
        if all(info in row.text for info in user_info):
            found = True
            break

    # Assert pour vérifier que l'utilisateur a bien été ajouté
    assert found, "Les informations de l'utilisateur ne sont pas présentes dans la liste des utilisateurs."

def test_search_user(setup_browser):
    driver = setup_browser
    driver.get("https://demoqa.com/webtables")

    # Rechercher un utilisateur
    driver.find_element(By.ID, "searchBox").click()
    driver.find_element(By.ID, "searchBox").send_keys("ierra")
    
    # Vérifier que l'utilisateur apparaît dans le résultat de la recherche
    rows = driver.find_elements(By.CLASS_NAME, "rt-tr-group")

    # Vérifier que "Cierra" et "Kierra" apparaissent dans les résultats de recherche
    cierra_found = False
    kierra_found = False

    for row in rows:
        if "Cierra" in row.text:
            cierra_found = True
        if "Kierra" in row.text:
            kierra_found = True

    # Assertions pour vérifier que les deux utilisateurs sont trouvés
    assert cierra_found, "L'utilisateur 'Cierra' n'apparaît pas dans les résultats de recherche."
    assert kierra_found, "L'utilisateur 'Kierra' n'apparaît pas dans les résultats de recherche."
    
def test_delete_user(setup_browser):
    driver = setup_browser
    driver.get("https://demoqa.com/webtables")

    # Rechercher l'utilisateur "Cierra" dans la table
    rows = driver.find_elements(By.CLASS_NAME, "rt-tr-group")
    user_found = False

    for row in rows:
        if "Cierra" in row.text:
            user_found = True
            # Cliquer sur le bouton de suppression pour cette ligne
            delete_button = row.find_element(By.CSS_SELECTOR, "span[title='Delete']")
            delete_button.click()
            break

    # Vérifier que l'utilisateur a été trouvé et supprimé
    assert user_found, "L'utilisateur 'Cierra' n'a pas été trouvé dans la table avant suppression."

    # Vérifier que "Cierra" n'apparaît plus dans la table
    rows_after_deletion = driver.find_elements(By.CLASS_NAME, "rt-tr-group")
    cierra_still_present = any("Cierra" in row.text for row in rows_after_deletion)

    assert not cierra_still_present, "L'utilisateur 'Cierra' est toujours présent dans la table après suppression."
    
def test_edit_user(setup_browser):
    driver = setup_browser
    driver.get("https://demoqa.com/webtables")

    # Rechercher l'utilisateur "Kierra" dans la table
    rows = driver.find_elements(By.CLASS_NAME, "rt-tr-group")
    user_found = False

    for row in rows:
        if "Kierra" in row.text:
            user_found = True
            # Cliquer sur le bouton d'édition pour cette ligne
            edit_button = row.find_element(By.CSS_SELECTOR, "span[title='Edit']")
            edit_button.click()
            break

    # Vérifier que l'utilisateur a bien été trouvé
    assert user_found, "L'utilisateur 'Kierra' n'a pas été trouvé dans la table avant édition."

    # Modifier les informations de l'utilisateur
    driver.find_element(By.ID, "firstName").clear()
    driver.find_element(By.ID, "firstName").send_keys("NewFirstName")

    driver.find_element(By.ID, "lastName").clear()
    driver.find_element(By.ID, "lastName").send_keys("NewLastName")

    driver.find_element(By.ID, "userEmail").clear()
    driver.find_element(By.ID, "userEmail").send_keys("newemail@example.com")

    driver.find_element(By.ID, "age").clear()
    driver.find_element(By.ID, "age").send_keys("35")

    driver.find_element(By.ID, "salary").clear()
    driver.find_element(By.ID, "salary").send_keys("90000")

    driver.find_element(By.ID, "department").clear()
    driver.find_element(By.ID, "department").send_keys("NewDepartment")

    driver.find_element(By.ID, "submit").click()

    # Vérifier que les informations ont bien été modifiées
    rows = driver.find_elements(By.CLASS_NAME, "rt-tr-group")
    user_info = ["NewFirstName", "NewLastName", "newemail@example.com", "35", "90000", "NewDepartment"]

    user_found = False
    for row in rows:
        if all(info in row.text for info in user_info):
            user_found = True
            break

    assert user_found, "Les informations de l'utilisateur n'ont pas été correctement mises à jour."