import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration du dossier pour les captures d'écran
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(script_dir, "screenshots")
error_login_dir = os.path.join(screenshot_dir, "error_login")  # Sous-dossier pour les erreurs de login
os.makedirs(error_login_dir, exist_ok=True)

# Configurer le navigateur
driver = webdriver.Chrome()

def take_screenshot_error_login(name):
    """
    Prend une capture d'écran spécifique pour les erreurs de login
    et la sauvegarde dans le dossier 'error_login'.
    """
    screenshot_path = os.path.join(error_login_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran sauvegardée : {screenshot_path}")

def login(driver, username, password):
    """
    Fonction pour se connecter avec les identifiants fournis.
    Retourne True si la connexion réussit, False sinon.
    Mesure également le temps pris après le clic sur le bouton login.
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
        
        # Démarrer le chronomètre
        start_time = time.time()
        login_button.click()

        # Vérifier si l'utilisateur est redirigé vers inventory.html
        WebDriverWait(driver, 5).until(
            EC.url_to_be("https://www.saucedemo.com/inventory.html")
        )
        print(f"Connexion réussie pour {username}")
        return True

    except Exception as e:
        print(f"Erreur lors de la tentative de connexion pour {username} : {e}")
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
        take_screenshot_error_login(f"{username}_logout_error")
        return False


def test_users():
    """
    Teste la connexion pour chaque utilisateur, y compris les cas d'erreurs.
    """
    # Liste des utilisateurs avec des combinaisons valides et invalides
    users = [
        {"username": "standard_user", "password": "secret_sauce"},  # Correct
        {"username": "locked_out_user", "password": "secret_sauce"},  # Locked
        {"username": "invalid_user", "password": "secret_sauce"},  # Username faux
        {"username": "performance_glitch_user", "password": "secret_sauce"},  # Correct
        {"username": "error_user", "password": "secret_sauce"},
        {"username": "visual_user", "password": "secret_sauce"},   # Faux cas ajouté pour test
    ]

    # URL de base
    base_url = "https://www.saucedemo.com/"

    for user in users:
        username = user["username"]
        password = user["password"]

        try:
            # Naviguer vers la page de connexion
            driver.get(base_url)

            # Effectuer la connexion
            if login(driver, username, password):
                # Vérifier que l'utilisateur est bien sur inventory.html
                current_url = driver.current_url
                if current_url == "https://www.saucedemo.com/inventory.html":
                    print(f"Utilisateur {username} correctement dirigé vers {current_url}.")
                else:
                    print(f"Redirection inattendue pour {username}, URL actuelle : {current_url}")
                    take_screenshot_error_login(f"{username}_unexpected_redirect")

                # Effectuer la déconnexion
                if not logout(driver, username):
                    print(f"Déconnexion échouée pour {username}, reste sur {driver.current_url}")
            else:
                print(f"Impossible de tester pour {username} (échec de connexion).")
                take_screenshot_error_login(f"{username}_echec")

        except Exception as e:
            print(f"Erreur lors du traitement de l'utilisateur {username} : {e}")
            take_screenshot_error_login(f"{username}_test_error")

if __name__ == "__main__":
    try:
        # Appeler la fonction principale
        test_users()
    except Exception as e:
        print(f"Erreur globale : {e}")
        take_screenshot_error_login("global_error")
    finally:
        # Fermer le navigateur
        driver.quit()
