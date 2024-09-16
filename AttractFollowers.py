from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Since the account I was working on had 80,000 followers, I had to first move on to transfer all of the followers to a file.
#In order not to be blocked by the Twitter server.

# WebDriver'ı başlatın
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Twitter'a gidin ve giriş yapın
    driver.get('https://twitter.com/')

    choose_login = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='loginButton']"))
    )
    driver.execute_script("arguments[0].click();", choose_login)

    username = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='text']"))
    )
    enter_user = input("Enter phone, username, or email: ")
    username.clear()
    username.send_keys(enter_user)
    username.send_keys(Keys.RETURN)

    password = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
    )
    enter_pass = input("Password: ")
    password.clear()
    password.send_keys(enter_pass)
    password.send_keys(Keys.RETURN)

    
    followers_section = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@data-testid='primaryColumn']//section"))
    )

    # Kullanıcının takipçilerini almak için hedef profili açın
    target_username = input("Enter the username of the target profile: ")
    driver.get(f"https://twitter.com/{target_username}/followers")

    time.sleep(180)     #3 saate 50 bin aşağı in

    all_followers=set()
    scroll_pause_time = 15
    scroll_amount = 2000  # Her kaydırmada sayfayı kaç piksel aşağı kaydıracağınızı belirleyin
    previous_height = 0
    sonmu=0
    
    while True:
        # Yeni takipçilerin yüklenmesini bekleyin
        followers = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='cellInnerDiv']//button/div/div/div/div/div/div/div/a/div/div/span"))
        )
        
        # Yeni takipçileri topla
        for follower in followers:
            #print(follower.text)
            all_followers.add(follower.text)
            print(len(all_followers))

        # Sayfayı belirli bir miktar kaydırın
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(scroll_pause_time)

        # Sayfanın yeni yüksekliğini kontrol edin
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Eğer sayfanın yüksekliği değişmediyse ve daha fazla içerik yüklenmiyorsa, döngüyü kır
        if new_height == previous_height:
                break

        previous_height = new_height


    # Takipçileri dosyaya yazdır
    
    with open("followers.txt", "a", encoding="utf-8") as file:
        for follower in all_followers:
            file.write(f"{follower}\n")

    print(f"Takipçiler '{"followers.txt"}' dosyasına başarıyla yazıldı.")



finally:
    #print(f"Toplam {len(all_followers)} takipçi alındı.")
    driver.quit()
