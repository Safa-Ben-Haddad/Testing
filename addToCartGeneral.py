import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# Configuration des captures d'écran
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(script_dir, "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)

def create_user_screenshot_dir(username):
    """
    Crée un sous-dossier pour chaque utilisateur dans le dossier 'cart_error'.
    """
    user_dir = os.path.join(screenshot_dir, "AddCartGeneral", username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def take_screenshot(driver, path, name):
    """
    Prend une capture d'écran et la sauvegarde dans le chemin spécifié.
    """
    screenshot_path = os.path.join(path, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran sauvegardée : {screenshot_path}")

def login(driver, username, password, user_dir):
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
        time.sleep(1)
        password_field.clear()
        time.sleep(1)

        username_field.send_keys(username)
        time.sleep(2)
        password_field.send_keys(password)
        time.sleep(2)

        # Cliquer sur le bouton de connexion
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(2)

        # Vérifier si l'utilisateur est redirigé vers inventory.html
        WebDriverWait(driver, 5).until(
            EC.url_to_be("https://www.saucedemo.com/inventory.html")
        )
        print(f"Connexion réussie pour {username}.")
        return True

    except TimeoutException:
        print(f"Connexion échouée pour {username}.")
        return False

    except Exception as e:
        print(f"Erreur lors de la tentative de connexion pour {username} : {e}")
        take_screenshot(driver, user_dir, "login_error")
        return False
def add_to_cart(driver, user_dir):
    """
    Ajouter des produits au panier.
    """
    try:
        # Localiser les boutons Ajouter
        add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        if not add_buttons:
            raise Exception("Aucun bouton Ajouter trouvé.")

        # Ajouter chaque produit au panier et vérifier après chaque ajout
        for index, button in enumerate(add_buttons):
            try:
                # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)
                time.sleep(1)  # Pause pour le défilement

                # Cliquer sur le bouton
                button.click()
                time.sleep(1)  # Pause pour simuler l'utilisateur

                # Vérifier le panier après chaque ajout
                try:
                    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
                    cart_count = int(cart_badge.text) if cart_badge else 0

                    if cart_count != index + 1:
                        print(f"Produit {index + 1} non ajouté au panier correctement.")
                        take_screenshot(driver, user_dir, f"error_ajout_verification_{index + 1}")
                except Exception as e:
                    print(f"Erreur lors de la vérification après ajout du produit {index + 1} : {e}")
                    take_screenshot(driver, user_dir, f"error_verification_produit_{index + 1}")

            except Exception as e:
                print(f"Erreur lors de l'ajout du produit {index + 1} : {e}")
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)
                time.sleep(1)  # Pause pour le défilement
                take_screenshot(driver, user_dir, f"error_ajout_produit_{index + 1}")

    except Exception as e:
        print(f"Erreur générale lors de l'ajout de produits au panier : {e}")
        take_screenshot(driver, user_dir, "error_general")


def logout(driver, user_dir):
    """
    Effectue la déconnexion.
    """
    try:
        menu_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        )
        menu_button.click()
        time.sleep(2)

        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_button.click()
        time.sleep(2)

        # Vérifier que l'utilisateur est redirigé vers la page de connexion
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        print("Déconnexion réussie.")
        return True
    except Exception as e:
        print(f"Erreur lors de la déconnexion : {e}")
        take_screenshot(driver, user_dir, "logout_error")
        return False

def test_user(username, password):
    """
    Teste la connexion, l'ajout au panier et la déconnexion pour un utilisateur spécifique.
    Chaque utilisateur utilise une instance de navigateur différente.
    """
    driver = webdriver.Chrome()
    user_dir = create_user_screenshot_dir(username)

    try:
        driver.get("https://www.saucedemo.com/")
        time.sleep(2)

        if login(driver, username, password, user_dir):
            add_to_cart(driver,user_dir)
            if not logout(driver, user_dir):
                print(f"Déconnexion échouée pour {username}.")
        else:
            print(f"Connexion échouée pour {username}.")

    except Exception as e:
        print(f"Erreur dans le test pour {username}: {e}")
        take_screenshot(driver, user_dir, "unexpected_error")

    finally:
        driver.quit()

def test_users():
    """
    Teste tous les utilisateurs avec des instances séparées de navigateur.
    """
    users = [
        {"username": "standard_user", "password": "secret_sauce"},
        {"username": "problem_user", "password": "secret_sauce"},
        {"username": "performance_glitch_user", "password": "secret_sauce"},
        {"username": "error_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"},
    ]

    for user in users:
        test_user(user["username"], user["password"])

if __name__ == "__main__":
    try:
        test_users()
    except Exception as e:
        print(f"Erreur globale : {e}")
