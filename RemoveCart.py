import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from addToCartGeneral import add_to_cart, login, logout
from addToCartGeneral import create_user_screenshot_dir
# Configuration des captures d'écran
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(script_dir, "screenshots")
remove_error_dir = os.path.join(screenshot_dir, "removeFromCart")
os.makedirs(remove_error_dir, exist_ok=True)

def take_screenshot_error_remove(driver, user, name):
    """
    Prend une capture d'écran spécifique pour les erreurs de suppression
    et la sauvegarde dans un dossier utilisateur dans 'removeExterieurError'.
    """
    user_dir = os.path.join(remove_error_dir, user)
    os.makedirs(user_dir, exist_ok=True)
    screenshot_path = os.path.join(user_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran sauvegardée : {screenshot_path}")

def remove_from_cart(driver, user):
    """
    Supprime tous les produits du panier pour l'utilisateur donné.
    """
    try:
        # Accéder au panier
        cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_button.click()
        time.sleep(2)

        # Trouver et cliquer sur les boutons de suppression
        remove_buttons = driver.find_elements(By.CLASS_NAME, "cart_button")
        for button in remove_buttons:
            button.click()
            time.sleep(1)

        # Vérifier si le panier est vide
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, "Le panier n'est pas vide après suppression."
        print(f"Tous les articles ont été supprimés du panier pour {user}.")

    except AssertionError as e:
        print(e)
        take_screenshot_error_remove(driver, user, "cart_not_empty")

    except Exception as e:
        print(f"Erreur lors de la suppression du panier pour {user} : {e}")
        take_screenshot_error_remove(driver, user, "remove_from_cart_error")

def test_remove_from_cart():
    """
    Teste la suppression pour chaque utilisateur avec des instances séparées de navigateur.
    """
    users = [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "locked_out_user", "password": "secret_sauce"},
        {"username": "problem_user", "password": "secret_sauce"},
        {"username": "performance_glitch_user", "password": "secret_sauce"},
        {"username": "error_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"},
    ]

    for user in users:
        driver = webdriver.Chrome()
        try:
            driver.get("https://www.saucedemo.com/")
            time.sleep(2)

            if login(driver, user["username"], user["password"], create_user_screenshot_dir(user["username"])):
                add_to_cart(driver, create_user_screenshot_dir(user["username"]))  # Ajouter des produits avant de les supprimer
                remove_from_cart(driver, user["username"])
                if not logout(driver, create_user_screenshot_dir(user["username"])):
                    print(f"Déconnexion échouée pour {user['username']}.")
            else:
                print(f"Connexion échouée pour {user['username']}.")

        except Exception as e:
            print(f"Erreur dans le test pour {user['username']}: {e}")
            take_screenshot_error_remove(driver, user["username"], "unexpected_error")

        finally:
            driver.quit()

if __name__ == "__main__":
    try:
        test_remove_from_cart()
    except Exception as e:
        print(f"Erreur globale : {e}")
