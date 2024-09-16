from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
import time
import re
from datetime import datetime
import winsound

# WebDriver'ı başlatın
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def is_bot_account(username):
    driver.get(f"https://twitter.com/{username}")
    time.sleep(3)

    # Katılma tarihini kontrol etmek için span'ların XPath'lerini belirleyin
    span_xpaths = [
        "//*[@id='react-root']/div/div/div/main/div/div/div/div/div/div/div/div/div/div/div/div/div/span[1]",
        "//*[@id='react-root']/div/div/div/main/div/div/div/div/div/div/div/div/div/div/div/div/span[2]",
        "//*[@id='react-root']/div/div/div/main/div/div/div/div/div/div/div/div/div/div/div/div/span[3]",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/span/span",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/span/span",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span/span",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div/span/span",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div/span[4]/span"
    ]

    join_year = None

    for xpath in span_xpaths:
        try:
            span_text = driver.find_element(By.XPATH, xpath).text
            if 'Joined' in span_text:
                join_year = span_text[-4:]  # Son 4 karakteri (yıl) al
                break  # Eğer bulduysak döngüden çık
        except:
            continue  # Eğer bir span bulunamazsa, bir sonrakine geç


    following_xpaths = [
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[5]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[4]/div[1]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[5]/div[1]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[5]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[4]/div[1]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div[1]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[6]/div[1]/a"
    ]
    following = None
    for xpath in following_xpaths:
        try:
            span_text = driver.find_element(By.XPATH, xpath).text
            if 'Following' in  span_text:
                following=span_text.split(" ")[0]         
                break  # Eğer bulduysak döngüden çık
        except:
            continue  # Eğer bir span bulunamazsa, bir sonrakine geç


    follower_xpaths = [
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[4]/div[2]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[4]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[5]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[4]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[5]/div[2]/a",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[5]/div[2]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[4]/div[2]/button",
        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[6]/div[2]/a"
    ]

    follower = None
    for xpath in follower_xpaths:
        try:
            span_text = driver.find_element(By.XPATH, xpath).text
            if 'Followers' in  span_text or 'Follower' in span_text:
                follower=span_text.split(" ")[0]
                break  # Eğer bulduysak döngüden çık
        except:
            continue  # Eğer bir span bulunamazsa, bir sonrakine geç

    try:
        span_text = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div").text
        postnumber=span_text.split(" ")[0]
    except:
        postnumber=None

    if follower==None or follower==None or postnumber==None or join_year==None :
        print("None")
        with open('NONE.txt', 'a' ) as file:
            file.write(f"{username}\n")
        winsound.Beep(1000, 500)
        return False


    if "K" in follower:
        follower=follower.replace(".", "")
        follower=follower.replace("K", "")
        follower=int(follower)*100
    elif "," in follower:
        follower =follower.replace(",", "")  # Virgülü kaldır

    if "K" in following:
        following=following.replace(".", "")
        following=following.replace("K", "")
        following=int(following)*1000
    elif "," in following:
        following =following.replace(",", "")  # Virgülü kaldır
    
    if "K" in postnumber:
        postnumber=postnumber.replace(".", "")
        postnumber=int(postnumber.replace("K", "000"))
    elif "," in postnumber:
        postnumber=postnumber.replace(",", "")



    
    if(int(following)-int(follower))>1000 and int(follower)<150 :
        print("type1") 
        with open('type1gece.txt' , 'a' ) as file:
                file.write(f"{username}\n")
        #return True
    elif (datetime.today().year - int(join_year))>4 and int(follower)<10:
        print("type2")
        with open('type2gece.txt' , 'a' ) as file:
                file.write(f"{username}\n")
        #return True
    elif (datetime.today().year - int(join_year))>4 and int(postnumber)<10:
        print("type3")
        with open('type3gece.txt' , 'a' ) as file:
                file.write(f"{username}\n")
    elif (datetime.today().year - int(join_year))>=7 and int(postnumber)<100:
        print("type4")
        with open('type4.txt' , 'a' ) as file:
                file.write(f"{username}\n")
    else:
     return False 


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
    

    start_line=11001
    end_line=15000

    all_followers=set()

    with open('followers.txt' , 'r' ) as file:
        for current_line, line in enumerate(file, start=1):
            if start_line<= current_line<=end_line:
                all_followers.add(line.strip())
    print(f"Toplam {len(all_followers)} follower çekildi.")
    
    

    #Her bir takipçiyi analiz et
    for username in all_followers:
        print(f"Analyzing {username}...")
        #if is_bot_account(username):
        is_bot_account(username)
        """ with open('BOTLAR.txt' , 'a' ) as file:
                file.write(f"{username}\n") """
        
        time.sleep(6)
            # Kullanıcıyı engelle
            #more_options = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/div/div/div/main/div/div/div/div/div/div/div/div/div/div/div/div/button"))
            # )                                 
            #more_options.click()
            # block_option = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[4]/div[2]/div/span"))
            # )
            # block_option.click()
            # confirm_block = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/button"))
            # )
            # confirm_block.click()

finally:
    #print(f"Toplam {len(all_followers)} takipçi alındı.")
    winsound.Beep(1000, 500)  # 1000 Hz frekansında 500 milisaniye boyunca bip sesi
    driver.quit()


