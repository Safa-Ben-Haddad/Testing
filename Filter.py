from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()

driver.get("https://www.saucedemo.com")


def login(username, password):
    username_input = driver.find_element(By.ID, "user-name") 
    password_input = driver.find_element(By.ID, "password")  
    login_btn = driver.find_element(By.ID, "login-button")  

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_btn.click()


#Filter Price High To Low
def test_filter_price_heigh_to_low(dir):
    try:
        options = driver.find_elements(by=By.TAG_NAME, value="option")
        options[3].click()

        prices = driver.find_elements(by=By.CLASS_NAME, value="inventory_item_price")

        time.sleep(1)

        if(
            float(prices[0].text.split("$")[1]) >= float(prices[1].text.split("$")[1]) and 
            float(prices[1].text.split("$")[1]) >= float(prices[2].text.split("$")[1]) and
            float(prices[2].text.split("$")[1]) >= float(prices[3].text.split("$")[1]) and
            float(prices[3].text.split("$")[1]) >= float(prices[4].text.split("$")[1]) and
            float(prices[4].text.split("$")[1]) >= float(prices[5].text.split("$")[1]) 
        ):
            print("\033[32m    [+] Filter Prices High To Low is Working Properly!!\033[0m")
        else:
            driver.get_screenshot_as_file(os.path.join(dir, "Prices_High_To_Low_Bug.png"))
            print("\033[31m    [-] Filter Prices High To Low is Not Working Properly!!\033[0m")
            print(f"\033[31m    [-] Checkout {dir}/Prices_High_To_Low_Bug.png\033[0m")
    except:
        driver.get_screenshot_as_file(os.path.join(dir, "Prices_High_To_Low_Bug.png"))
        print("\033[31m    [-] Filter Prices High To Low is Not Working Properly!!\033[0m")
        print(f"\033[31m    [-] Checkout {dir}/Prices_High_To_Low_Bug.png\033[0m")



# Filter Prices Low To High
def test_filter_price_low_to_high(dir):
    try:
        options = driver.find_elements(by=By.TAG_NAME, value="option")
        options[2].click()

        prices = driver.find_elements(by=By.CLASS_NAME, value="inventory_item_price")

        time.sleep(1)

        if(
            float(prices[0].text.split("$")[1]) <= float(prices[1].text.split("$")[1]) and 
            float(prices[1].text.split("$")[1]) <= float(prices[2].text.split("$")[1]) and
            float(prices[2].text.split("$")[1]) <= float(prices[3].text.split("$")[1]) and
            float(prices[3].text.split("$")[1]) <= float(prices[4].text.split("$")[1]) and
            float(prices[4].text.split("$")[1]) <= float(prices[5].text.split("$")[1]) 
        ):
            print("\033[32m    [+] Filter Prices Low To High is Working Properly!!\033[0m")
        else:
            driver.get_screenshot_as_file(os.path.join(dir, "Prices_Low_To_High_Bug.png"))
            print("\033[31m    [-] Filter Prices High To Low is Not Working Properly!!\033[0m")
            print(f"\033[31m    [-] Checkout {dir}/Prices_Low_To_High_Bug.png\033[0m")
    except:
        driver.get_screenshot_as_file(os.path.join(dir, "Prices_Low_To_High_Bug.png"))
        print("\033[31m    [-] Filter Prices High To Low is Not Working Properly!!\033[0m")
        print(f"\033[31m    [-] Checkout {dir}/Prices_Low_To_High_Bug.png\033[0m")



# Filter Z To A
def test_filter_z_to_a(dir):
    try:
        options = driver.find_elements(by=By.TAG_NAME, value="option")
        options[1].click()

        product_names = driver.find_elements(by=By.CLASS_NAME, value="inventory_item_name")

        time.sleep(1)

        if(
            ord(product_names[0].text[0]) >= ord(product_names[1].text[0]) and 
            ord(product_names[1].text[0]) >= ord(product_names[2].text[0]) and 
            ord(product_names[2].text[0]) >= ord(product_names[3].text[0]) and
            ord(product_names[3].text[0]) >= ord(product_names[4].text[0]) and 
            ord(product_names[4].text[0]) >= ord(product_names[5].text[0])
        ):
            print("\033[32m    [+] Filter Products Z To A is Working Properly!!\033[0m")
        else:
            driver.get_screenshot_as_file(os.path.join(dir, "Products_Z_To_A_Bug.png"))
            print("\033[31m    [-] Filter Products Z To A is Not Working Properly!!\033[0m")
            print(f"\033[31m    [-] Checkout {dir}/Products_Z_To_A_Bug.png\033[0m")
    except:
        print("\033[31m    [-] Filter Products Z To A is Not Working Properly!!\033[0m")
        print(f"\033[31m    [-] Checkout {dir}/Products_Z_To_A_Bug.png\033[0m")

# Filter A To Z
def test_filter_a_to_z(dir):
    try:
        options = driver.find_elements(by=By.TAG_NAME, value="option")
        options[1].click()

        product_names = driver.find_elements(by=By.CLASS_NAME, value="inventory_item_name")

        time.sleep(1)

        if(
            ord(product_names[0].text[0]) <= ord(product_names[1].text[0]) and 
            ord(product_names[1].text[0]) <= ord(product_names[2].text[0]) and 
            ord(product_names[2].text[0]) <= ord(product_names[3].text[0]) and
            ord(product_names[3].text[0]) <= ord(product_names[4].text[0]) and 
            ord(product_names[4].text[0]) <= ord(product_names[5].text[0])
        ):
            print("\033[32m    [+] Filter Products A To Z is Working Properly!!\033[0m")
        else:
            driver.get_screenshot_as_file(os.path.join(dir, "Products_A_To_Z_Bug.png"))
            print("\033[31m    [-] Filter Products A To Z is Not Working Properly!!\033[0m")
            print(f"\033[31m    [-] Checkout {dir}/Products_A_To_Z_Bug.png\033[0m")
    except:
        driver.get_screenshot_as_file(os.path.join(dir, "Products_A_To_Z_Bug.png"))
        print("\033[31m    [-] Filter Products A To Z is Not Working Properly!!\033[0m")
        print(f"\033[31m    [-] Checkout {dir}/Products_A_To_Z_Bug.png\033[0m")

def main():
    # Testing Standard User
    print("\033[38;5;208m[i] TESTING FILTER FUNCTIONALITY FOR STANDARD USER ...\033[0m")
    login("standard_user", "secret_sauce")
    os.makedirs(os.path.join(os.getcwd(), "standard_user_bugs"), exist_ok=True)
    test_filter_price_low_to_high(os.path.join(os.getcwd(), "standard_user_bugs"))
    test_filter_price_heigh_to_low(os.path.join(os.getcwd(), "standard_user_bugs"))
    test_filter_z_to_a(os.path.join(os.getcwd(), "standard_user_bugs"))
    test_filter_a_to_z(os.path.join(os.getcwd(), "standard_user_bugs"))

    driver.get("https://www.saucedemo.com")
    time.sleep(1)

    # TESTING PROBLEM USER
    print("\033[38;5;208m[i] TESTING FILTER FUNCTIONALITY FOR PROBLEM USER ...\033[0m")
    login("problem_user", "secret_sauce")
    os.makedirs(os.path.join(os.getcwd(), "problem_user_bugs"), exist_ok=True)
    test_filter_price_low_to_high(os.path.join(os.getcwd(), "problem_user_bugs"))
    test_filter_price_heigh_to_low(os.path.join(os.getcwd(), "problem_user_bugs"))
    test_filter_z_to_a(os.path.join(os.getcwd(), "problem_user_bugs"))
    test_filter_a_to_z(os.path.join(os.getcwd(), "problem_user_bugs"))

    driver.get("https://www.saucedemo.com")
    time.sleep(1)

    # TESTING PERFORMANCE GLITCH USER
    print("\033[38;5;208m[i] TESTING FILTER FUNCTIONALITY FOR PERFORMACE GLITCH USER ...\033[0m")
    login("performance_glitch_user", "secret_sauce")
    os.makedirs(os.path.join(os.getcwd(), "performance_glitch_user_bugs"), exist_ok=True)
    test_filter_price_low_to_high(os.path.join(os.getcwd(), "performance_glitch_user_bugs"))
    test_filter_price_heigh_to_low(os.path.join(os.getcwd(), "performance_glitch_user_bugs"))
    test_filter_z_to_a(os.path.join(os.getcwd(), "performance_glitch_user_bugs"))
    test_filter_a_to_z(os.path.join(os.getcwd(), "performance_glitch_user_bugs"))

    driver.get("https://www.saucedemo.com")
    time.sleep(1)

    # TESTING ERROR USER
    print("\033[38;5;208m[i] TESTING FILTER FUNCTIONALITY FOR ERROR USER ...\033[0m")
    login("error_user", "secret_sauce")
    os.makedirs(os.path.join(os.getcwd(), "error_user_bugs"), exist_ok=True)
    test_filter_price_low_to_high(os.path.join(os.getcwd(), "error_user_bugs"))
    test_filter_price_heigh_to_low(os.path.join(os.getcwd(), "error_user_bugs"))
    test_filter_z_to_a(os.path.join(os.getcwd(), "error_user_bugs"))
    test_filter_a_to_z(os.path.join(os.getcwd(), "error_user_bugs"))

    driver.get("https://www.saucedemo.com")
    time.sleep(1)

    # TESTING VISUAL USER
    print("\033[38;5;208m[i] TESTING FILTER FUNCTIONALITY FOR VISUAL USER ...\033[0m")
    login("visual_user", "secret_sauce")
    os.makedirs("visual_error_user_bugs", exist_ok=True)
    test_filter_price_low_to_high("visual_error_user_bugs")
    test_filter_price_heigh_to_low("visual_error_user_bugs")
    test_filter_z_to_a("visual_error_user_bugs")
    test_filter_a_to_z("visual_error_user_bugs")

if __name__ == "__main__":
    main()

driver.quit()
