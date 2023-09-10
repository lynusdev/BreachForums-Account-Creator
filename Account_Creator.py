from selenium.webdriver.common.by import By
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from random import randint
from datetime import datetime

warnings.simplefilter("ignore")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2})
chrome_options.add_argument("--mute-audio")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--lang=en-US")

with open("usernames.txt", "r") as f:
    names = f.read().splitlines()

accounts = []
proxies = [
    "IP:PORT", "IP:PORT", "IP:PORT"
]
proxyrotator = 0

counter = 0

while counter < len(names):
    if proxyrotator == 7:
        proxyrotator = 0
    chrome_options.add_argument("proxy-server="+proxies[proxyrotator])
    proxyrotator = proxyrotator+1

    driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    driver.maximize_window()
    breachedwindow = driver.current_window_handle
    try:
        driver.get("https://breached.to/member.php?action=register")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body")))
        start_time = time.time()
    except:
        print("Proxy not working, moving on...")
        continue

    try:
        driver.find_element(By.NAME, "agree")
    except:
        print("IP blocked, moving on...")
        continue
    else:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, "agree"))).click()

    driver.switch_to.new_window('tab')
    mailwindow = driver.current_window_handle
    time.sleep(0.5)
    driver.get("https://mail.tm")
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "DontUseWEBuseAPI")))
    while True:
        if not driver.find_element(By.ID, "DontUseWEBuseAPI").get_attribute('value') == "...":
            email = driver.find_element(
                By.ID, "DontUseWEBuseAPI").get_attribute('value')
            break
        time.sleep(0.1)

    username = names[counter]+str(randint(0, 99))
    password = names[counter]+"Kr"+str(randint(1000, 9999))

    driver.switch_to.window(breachedwindow)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.NAME, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.NAME, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.NAME, "password2"))).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email2"))).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "hideemail"))).click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "receivepms"))).click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "imagestring"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.NAME, "imagestring"))).send_keys("X")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "invisible"))).click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "imagestring"))).clear()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "imagestring"))).click()

    while True:
        if time.time() - start_time > 17:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "answer"))).send_keys("4")
            driver.find_element(By.NAME, "imagestring").click()
            break
        time.sleep(0.1)

    while True:
        try:
            WebDriverWait(driver, 0.1).until(
                EC.visibility_of_element_located((By.NAME, "imagestring-error")))
        except:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "regsubmit"))).click()
            break

    driver.switch_to.window(mailwindow)
    for i in range(10):
        try:
            driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div[2]/ul/li/a").click()
        except:
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/nav/a[2]"))).click()
            resend = 1
        else:
            resend = 0
            break
    if resend == 1:
        driver.switch_to.window(breachedwindow)
        driver.get("https://breached.to/member.php?action=resendactivation")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))).send_keys(email)
        while True:
            if not driver.title == "BreachForums - Resend Account Activation":
                break
            time.sleep(0.1)
        driver.switch_to.window(mailwindow)
        for i in range(10):
            try:
                driver.find_element(
                    By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div[2]/ul/li/a").click()
            except:
                time.sleep(2)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/nav/a[2]"))).click()
                worked = 0
            else:
                worked = 1
                break
        if worked == 0:
            print("Cant receive email, skipping account")
            continue

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "iFrameResizer0")))
    driver.switch_to.frame(iframe)
    verifylink = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/p[3]"))).text
    driver.get(verifylink)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "panel")))
    driver.quit()
    accounts.append(str(username+":"+password+":"+email+":" +
                    datetime.today().strftime('%Y-%m-%d')))
    print(counter+1, str(username+":"+password+":" +
          email+":"+datetime.today().strftime('%Y-%m-%d')))
    with open("accounts_breached.to_softreg_"+datetime.today().strftime('%Y-%m-%d')+".txt", "w") as f:
        for account in accounts:
            f.write("%s\n" % account)
    counter = counter+1

open('usernames.txt', 'w').close()
input("Press ENTER to close")
