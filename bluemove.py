import time
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


def mint(values, isWindows):
    
    def selectWallet():
        print("Status - Selecting wallet")
        WebDriverWait(driver, 600).until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Connect Wallet')]")))
        connect = driver.find_element(
            By.XPATH, "//a[contains(text(),'Connect Wallet')]")
        connect.click()

        WebDriverWait(driver, 600).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Martian Wallet')]")))
        martian = driver.find_element(
            By.XPATH, "//div[contains(text(),'Martian Wallet')]")
        martian.click()

        WebDriverWait(driver, 600).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        password1 = driver.find_elements(By.XPATH, "//input[@type='password']")[0].send_keys('1234567890')

        WebDriverWait(driver, 600).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Unlock')]")))
        unlock = driver.find_element(
            By.XPATH, "//button[contains(text(),'Unlock')]")
        unlock.click()
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-kDvujY cpPtvm']")))
        approve = driver.find_element(By.XPATH, "//button[@class='sc-kDvujY cpPtvm']").click()
        time.sleep(5)
        WebDriverWait(driver, 600).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-kDvujY cpPtvm']")))
        approve = driver.find_element(By.XPATH, "//button[@class='sc-kDvujY cpPtvm']").click()
        print("Status - Finished Selecting Wallet")



    def avaitMint():
        print("Status - Waiting for mint")
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 600*600*24).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint')]")))
        mint_your_token = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Mint')]")
        driver.execute_script("arguments[0].click();", mint_your_token)

        original_window = driver.current_window_handle
        WebDriverWait(driver, 600).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 600).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Approve')]")))
        approve = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Approve')]")
        approve.click()
        time.sleep(50)

    def initWallet():
        print("Initializing wallet")
        original_window = driver.current_window_handle
        WebDriverWait(driver, 600).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//div[@class='MuiGrid-root css-owchxn']")))
        selectingType = driver.find_element(By.XPATH, "//div[@class='MuiGrid-root css-owchxn']").click()
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//div[@class='MuiGrid-root MuiGrid-item css-ochnpn']")))
        recovery_phrase = driver.find_element(By.XPATH, "//div[@class='MuiGrid-root MuiGrid-item css-ochnpn']").click()
		
        WebDriverWait(driver, 6000).until(EC.presence_of_element_located((By.XPATH, "//*[@name='0']")))
        for i in range(0, 12):
            driver.find_element(By.XPATH, f"//*[@name='{i}']").send_keys(values[1].split(' ')[i])
        driver.find_element(By.XPATH, "//div[@class='sc-dkrFOg FdmMC']").click()

        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password1 = driver.find_elements(By.XPATH, "//input[@type='password']")[0].send_keys('1234567890')
        password2 = driver.find_elements(By.XPATH, "//input[@type='password']")[1].send_keys('1234567890')
        check_box = driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sc-dkrFOg kmtnUS']")))
        selectingType = driver.find_element(By.XPATH, "//div[@class='sc-dkrFOg kmtnUS']").click()
        selectingType = driver.find_element(By.XPATH, "//div[@class='sc-dkrFOg FdmMC']").click()
        selectingType = driver.find_element(By.XPATH, "//div[@class='sc-dkrFOg FdmMC']").click()
        selectingType = driver.find_element(By.XPATH, "//div[@class='sc-dkrFOg FdmMC']").click()
        print("Finished Initializing wallet")
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)

        return main_window

    print("Bot started") 
    if isWindows:
        print("OS : Windows")
    else:
        print("OS : Mac")
    

    options = Options()
    options.add_extension("Martian.crx")
    options.add_argument("--disable-gpu")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    os.environ['WDM8LOCAL'] = '1'
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    print("Assertion - successfully found chrome driver")
    
    driver.get(values[0])

    main_window = initWallet()
    selectWallet()
    avaitMint()
    print("Minting Finished")
