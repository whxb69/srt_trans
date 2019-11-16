from selenium import webdriver
from pykeyboard import PyKeyboard
import os


k = PyKeyboard()

flacs = [os.path.abspath(file) for file in os.listdir() if os.path.splitext(file)[1] == '.flac']

driver = webdriver.Chrome()
url = 'https://fanyi.caiyunapp.com/#/video'

for flac in flacs:
    driver.get(url)

    upload = driver.find_element_by_xpath('//*[@id="audio_file"]')
    print(upload)
    upload.send_keys(flac)

    l_choose = driver.find_element_by_xpath('//*[@id="xiaoyi-web"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]')
    l_choose.click()

    ok = driver.find_element_by_xpath('/html/body/div[4]/div/div[3]/button')
    ok.click()

    progress = driver.find_element_by_xpath('//*[@id="xiaoyi-web"]/div/div[2]/div[2]/div')

    temp = progress.text
    while temp:
        try:
            temp = progress.text
        except:
            break

    res1 = driver.find_element_by_xpath('//*[@id="xiaoyi-web"]/div/div[2]/div[3]/div[1]/div[1]/a')
    res1.click()
    res2 = driver.find_element_by_xpath('//*[@id="xiaoyi-web"]/div/div[2]/div[3]/div[1]/div[2]/a')
    res1.click()
    res3 = driver.find_element_by_xpath('//*[@id="xiaoyi-web"]/div/div[2]/div[3]/div[1]/div[3]/a')
    res1.click()
