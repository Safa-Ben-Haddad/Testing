import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Configuration
SAUCEDDEMO_URL = "https://www.saucedemo.com/"
USERS = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"},
]
SCREENSHOTS_DIR = "screenshots/RemoveExterieur"
DELAY_SECONDS = 3  # Temps d'attente pour visualisation des changements

def create_user_directory(user):
    """Créer un dossier pour l'utilisateur."""
    user_dir = os.path.join(SCREENSHOTS_DIR, user["username"])
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def take_screenshot(driver, user_dir, step_name):
    """Prendre une capture d'écran."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(user_dir, f"{step_name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)

def login(driver, username, password):
    """Connexion à Saucedemo."""
    driver.get(SAUCEDDEMO_URL)
    time.sleep(DELAY_SECONDS)  # Attente pour visualiser le chargement de la page
    try:
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
    except NoSuchElementException:
        print(f"Erreur : Éléments de connexion introuvables pour {username}.")
        return False
    time.sleep(DELAY_SECONDS)  # Attente après connexion
    return True

def add_and_remove_products(driver, user_dir):
    """Ajouter des produits au panier et les supprimer."""
    try:
        # Ajouter un produit
        add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        if not add_buttons:
            raise Exception("Aucun bouton Ajouter trouvé.")
        
        for button in add_buttons:
            button.click()
            time.sleep(DELAY_SECONDS)  # Attente pour chaque ajout

        # Vérifier l'état du panier
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        if int(cart_badge.text) != len(add_buttons):
            print("Nombre de produits dans le panier incorrect.")
            take_screenshot(driver, user_dir, "error_panier")

        # Supprimer les produits
        remove_buttons = driver.find_elements(By.CLASS_NAME, "btn_secondary")
        if not remove_buttons:
            print("Aucun bouton Supprimer trouvé.")
            take_screenshot(driver, user_dir, "BtnIntrouvable")
        
        for button in remove_buttons:
            button.click()
            time.sleep(DELAY_SECONDS)  # Attente pour chaque suppression

    except Exception as e:
        print(f"Erreur lors de l'ajout/suppression de produits : {e}")
        take_screenshot(driver, user_dir, "error")

def main():
    for user in USERS:
        print(f"Test en cours pour l'utilisateur : {user['username']}")
        user_dir = create_user_directory(user)
        
        # Initialiser une nouvelle instance du navigateur pour chaque utilisateur
        driver = webdriver.Chrome()

        try:
            if login(driver, user["username"], user["password"]):
                add_and_remove_products(driver, user_dir)
                time.sleep(7)
            
            else:
                print(f"Connexion échouée pour l'utilisateur {user['username']}.")
        finally:
            # Fermer le navigateur après le test
            driver.quit()

    print("Tests terminés.")

if __name__ == "__main__":
    main()
