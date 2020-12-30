from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


def cracker(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('C:\Program Files\ChromeWebdrive\chromedriver.exe', options=options)
    driver.get(url)
    time.sleep(2)
    btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/ul/li/div/div[4]/div')))
    btn.click()
    print("关闭疫情提醒")
    time.sleep(1)
    scroll_length = driver.find_element_by_class_name('cpt-bg-bar')
    scroll_length.get_attribute('style')
    length = re.findall(re.compile(r'\d+'), scroll_length.get_attribute('style'))[0]
    print(length)
    # 破解滑动验证码
    scrollElement = driver.find_elements_by_class_name('cpt-drop-btn')[0]
    ActionChains(driver).click_and_hold(on_element=scrollElement).perform()
    # 第一次滑动
    ActionChains(driver).move_to_element_with_offset(to_element=scrollElement, xoffset=100, yoffset=10).perform()
    # 第二次滑动
    ActionChains(driver).move_to_element_with_offset(to_element=scrollElement, xoffset=200, yoffset=20).perform()
    # 第三次滑动
    ActionChains(driver).move_to_element_with_offset(to_element=scrollElement, xoffset=int(length) - 200,
                                                     yoffset=50).perform()
    print('滑块破解成功')
    time.sleep(1)
    # time.sleep(30)



