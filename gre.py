from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from lxml import etree
import os
from PIL import Image
from io import BytesIO

os.environ['MOZ_HEADLESS'] = '1'

username = "xxxx"
passwd = 'xxxx'


def open_url():
    print('打开网页...')
    driver = webdriver.Firefox()
    driver.get("https://gre.etest.net.cn")
    driver.implicitly_wait(10)

    return driver


def login(driver):
    driver.find_element_by_id("neeaId").send_keys(username)
    driver.find_element_by_id("password").send_keys(passwd)
    driver.find_element_by_id("checkImageCode").click()
    driver.implicitly_wait(10)
    image = driver.find_element_by_id('chkImg').screenshot_as_png
    im = Image.open(BytesIO(image))
    im.save('tmp.png')
    command = 'xdg-open {}'.format('tmp.png')
    os.system(command)
    print('验证码：')
    codeContent = input()
    driver.find_element_by_id("checkImageCode").send_keys(codeContent)
    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div[5]/input')
    ActionChains(driver).click(login).perform()
    driver.implicitly_wait(10)

    return driver


def get_seats(driver):
    print('开始查询考位...')

    driver.find_elements_by_xpath('//*[@id="westContainer"]/ul/li[13]/a')[0].click()
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="huabei"]')[0].click()
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="BEIJING"]')[0].click()
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="BEIJING_BEIJING"]')[0].click()
    time.sleep(1)
    driver.find_elements_by_xpath('//*[@id="cities_Next"]')[0].click()
    time.sleep(1)
    s1 = Select(driver.find_element_by_tag_name("select"))

    for i in range(len(s1.options)):
        Select(driver.find_element_by_tag_name("select")).select_by_index(i)
        time.sleep(1)
        date = s1.first_selected_option.text
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='testDate_Next']").click()
        time.sleep(1)

        match = 0

        content = driver.page_source

        selector = etree.HTML(content)
        pList = selector.xpath('//*[@id="sitesTable0"]/tbody/tr')
        for item in pList:
            if item.xpath('td[4]/text()') and item.xpath('td[4]/text()')[0] != '暂满':
                school_code = item.xpath('td[1]/a/text()')[0]
                school_name = item.xpath('td[2]/text()')[0]
                print(date, school_code, school_name, item.xpath('td[4]/text()')[0])
                match = 1

        if match == 0:
            print('Soooo sad!!!--{}--没有考位'.format(date))

        driver.find_element_by_xpath('//*[@id="sites_BackDate"]').click()
        time.sleep(1)


if __name__ == '__main__':
    driver = open_url()
    driver = login(driver)

    driver = get_seats(driver)
    driver.quit()

    print('查询结束.')
