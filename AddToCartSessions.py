import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuration des dossiers pour les captures d'écran
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(script_dir, "screenshots")
add_to_cart_dir = os.path.join(screenshot_dir, "AddToCart")
os.makedirs(add_to_cart_dir, exist_ok=True)

def ensure_user_directory(username):
    """
    Garantit que chaque utilisateur dispose d'un sous-dossier pour les captures d'écran.
    """
    user_dir = os.path.join(add_to_cart_dir, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def capture_screenshot(driver, name, username):
    """
    Prend une capture d'écran pour un utilisateur spécifique et sauvegarde dans son sous-dossier.
    """
    user_dir = ensure_user_directory(username)
    screenshot_path = os.path.join(user_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran sauvegardée : {screenshot_path}")

def login(driver, username, password):
    """
    Fonction pour se connecter avec les identifiants fournis.
    Retourne True si la connexion réussit, False sinon.
    """
    try:
        # Localiser les champs username et password
        username_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        password_field = driver.find_element(By.ID, "password")

        # Entrer les identifiants
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Cliquer sur le bouton de connexion
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Vérifier si l'utilisateur est redirigé vers inventory.html
        WebDriverWait(driver, 5).until(
            EC.url_to_be("https://www.saucedemo.com/inventory.html")
        )
        print(f"Connexion réussie pour {username}.")
        return True

    except TimeoutException:
        print(f"Connexion échouée pour {username}.")
        capture_screenshot(driver, f"{username}_login_failed", username)
        return False

    except Exception as e:
        print(f"Erreur lors de la tentative de connexion pour {username} : {e}")
        capture_screenshot(driver, f"{username}_login_error", username)
        return False

def logout(driver, username):
    """
    Effectue la déconnexion en utilisant le menu latéral.
    Retourne True si la déconnexion réussit, False sinon.
    """
    try:
        menu_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        )
        menu_button.click()

        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_button.click()

        # Vérifier que l'utilisateur est redirigé vers la page de connexion
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        print(f"Déconnexion réussie pour {username}.")
        return True

    except Exception as e:
        print(f"Erreur lors de la déconnexion pour {username} : {e}")
        capture_screenshot(driver, f"{username}_logout_error", username)
        return False


def add_all_products_to_cart(driver, username):
    """
    Parcourt tous les produits et tente de les ajouter au panier.
    Capture les erreurs si le produit est déjà ajouté ou si une mise à jour échoue.
    """
    try:
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for index, product in enumerate(products):
            try:
                add_button = product.find_element(By.CLASS_NAME, "btn_inventory")
                button_text = add_button.text.lower()
                if button_text == "Remove":
                    print(f"Produit {index + 1} déjà ajouté pour {username}.")
                    time.sleep(3)
                    capture_screenshot(driver, f"product_{index + 1}_already_added", username)
                    continue
            

                # Sinon, tenter de l'ajouter
                add_button.click()

                # Pause pour visualiser l'ajout du produit
                time.sleep(2)

                # Vérifier la mise à jour du panier
                cart_badge = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
                )
                print(f"Produit {index + 1} ajouté pour {username}. Articles dans le panier : {cart_badge.text}.")

                # Pause pour observer la mise à jour
                time.sleep(2)

            except TimeoutException:
                print(f"Erreur de mise à jour du panier pour le produit {index + 1} de {username}.")
                capture_screenshot(driver, f"product_{index + 1}_cart_update_failed", username)
            except Exception as e:
                print(f"Erreur inconnue pour le produit {index + 1} de {username} : {e}")
                capture_screenshot(driver, f"product_{index + 1}_error", username)
    except Exception as e:
        print(f"Erreur lors de l'ajout des produits au panier pour {username} : {e}")
        capture_screenshot(driver, "add_all_products_error", username)

def test_add_to_cart():
    """
    Teste la fonctionnalité d'ajout au panier pour chaque utilisateur.
    """
    # Liste des utilisateurs et leurs mots de passe
    users = [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "locked_out_user", "password": "secret_sauce"},
        {"username": "problem_user", "password": "secret_sauce"},
        {"username": "performance_glitch_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"},
        {"username": "error_user", "password": "secret_sauce"},

    ]

    # URL de base
    base_url = "https://www.saucedemo.com/"

    # Configurer une seule instance du navigateur
    driver = webdriver.Chrome()

    try:
        for user in users:
            username = user["username"]
            password = user["password"]

            try:
                # Naviguer vers la page de connexion
                driver.get(base_url)

                # Effectuer la connexion
                if login(driver, username, password):
                    # Ajouter tous les produits au panier
                    add_all_products_to_cart(driver, username)

                    # Effectuer la déconnexion
                    if not logout(driver, username):
                        print(f"Déconnexion échouée pour {username}, reste sur {driver.current_url}")
                else:
                    print(f"Impossible de tester pour {username} (échec de connexion).")

            except Exception as e:
                print(f"Erreur lors du traitement de l'utilisateur {username} : {e}")
                capture_screenshot(driver, f"{username}_test_error", username)

    except Exception as e:
        print(f"Erreur globale : {e}")
        capture_screenshot(driver, "global_error", "global")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_add_to_cart()
