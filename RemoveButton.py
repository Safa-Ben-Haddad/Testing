import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from addToCartGeneral import add_to_cart

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

def create_user_directory(user):
    """Créer un dossier pour l'utilisateur."""
    user_dir = os.path.join(SCREENSHOTS_DIR, user["username"])
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def take_screenshot(driver, user_dir, step_name):
    """Prendre une capture d'écran."""
    screenshot_path = os.path.join(user_dir, f".png")
    driver.save_screenshot(screenshot_path)

def login(driver, username, password):
    """Connexion à Saucedemo."""
    driver.get(SAUCEDDEMO_URL)
    try:
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
    except NoSuchElementException:
        print(f"Erreur : Éléments de connexion introuvables pour {username}.")
        return False
    return True

def add_and_remove_products(driver, user_dir):
    """Ajouter des produits au panier et les supprimer."""
    try:
        add_to_cart(driver,user_dir)
        # Supprimer les produits du panier
        remove_buttons = driver.find_elements(By.CLASS_NAME, "btn_secondary")
        if not remove_buttons:
            print("Aucun bouton Supprimer trouvé.")
            take_screenshot(driver, user_dir, "error_suppression_btn_introuvable")
            return

        for index, button in enumerate(remove_buttons):
            try:
                # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)

                # Cliquer sur le bouton
                button.click()
                time.sleep

                # Vérifier le panier après chaque suppression
                try:
                    cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
                    if cart_badge:
                        cart_count = int(cart_badge[0].text)
                        if cart_count != len(remove_buttons) - (index + 1):
                            print(f"Produit {index + 1} non supprimé correctement.")
                            take_screenshot(driver, user_dir, f"error_suppression_{index + 1}")
                    else:
                        if index != len(remove_buttons) - 1:
                            print(f"Le panier est vide avant la suppression complète du produit {index + 1}.")
                            take_screenshot(driver, user_dir, f"error_suppression_incomplete_{index + 1}")
                except Exception as e:
                    print(f"Erreur lors de la vérification après suppression du produit {index + 1} : {e}")
                    take_screenshot(driver, user_dir, f"error_verification_suppression_{index + 1}")

            except Exception as e:
                print(f"Erreur lors de la suppression du produit {index + 1} : {e}")
                take_screenshot(driver, user_dir, f"error_suppression_produit_{index + 1}")

    except Exception as e:
        print(f"Erreur lors de l'ajout/suppression de produits : {e}")
        take_screenshot(driver, user_dir, "error_general")


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
