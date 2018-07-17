from selenium import webdriver
import csv
import time
import re
import os
from PIL import Image
from io import BytesIO

os.environ['MOZ_HEADLESS'] = '1'

username = "xxx"
passwd = 'xxx'


def open_url():
    print('打开网页...')
    driver = webdriver.Firefox()
    driver.get("https://toefl.etest.net.cn/cn/")
    driver.implicitly_wait(10)

    return driver


def login(driver):
    driver.find_element_by_id("id_username").send_keys(username)
    driver.find_element_by_id("id_pwd").send_keys(passwd)
    driver.find_element_by_id("a_changeone").click()

    image = driver.find_element_by_id('imgVerifycode').screenshot_as_png
    im = Image.open(BytesIO(image))
    im.save('tmp.png')
    command = 'xdg-open {}'.format('tmp.png')
    os.system(command)
    print('验证码：')
    codeContent = input()
    driver.find_element_by_id("input_vcode").send_keys(codeContent)

    driver.find_element_by_id("id_login").click()
    driver.implicitly_wait(10)

    if driver.page_source.find("考位查询"):
        print('输入正确!')
    else:
        print('输入错误, 尝试重新登录...')
        login(driver)

    return driver


def search_zuowei(driver):
    driver.find_element_by_link_text("考位查询").click()

    return driver


def get_zuowei(driver, month, are):
    print('开始查询考位...')

    # 获取月份
    driver.find_elements_by_xpath('//input[@value="%s"]' % month)[0].click()
    time.sleep(1)
    # 获取城市
    driver.find_elements_by_xpath('//input[@value="%s"]' % are)[0].click()
    time.sleep(1)

    image = driver.find_elements_by_xpath('//img')
    if len(image) > 2:
        image2 = image[2].screenshot_as_png
    else:
        image2 = image[1].screenshot_as_png
    im = Image.open(BytesIO(image2))
    im.save('tmp.png')
    command = 'xdg-open {}'.format('tmp.png')
    os.system(command)
    print('验证码：')
    codeContent2 = input()

    driver.find_element_by_name("afCalcResult").send_keys(codeContent2)
    driver.find_element_by_name("submit").click()
    driver.implicitly_wait(10)
    # 检查是否输入正确
    if driver.page_source.find('请输入验证码') != -1:
        print('输入错误, 请重新输入...')
        get_zuowei(driver, month, are)
    else:
        print('输入正确!')
        content = driver.page_source
        driver.implicitly_wait(10)
        time1 = re.findall(r'<tr bgcolor="#FFCC99">(.*?)</tr>', content, re.S)[0]  # 匹配时间地区
        time_clear = re.findall(r'<b>(.*?)</b>', time1, re.S)
        time_str = time_clear[0] + time_clear[1]
        aim_list = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>', content, re.S)
        res_list = []
        for aim in aim_list:
            aim_clear = re.findall(r'<td.*?>(.*?)</td>', aim, re.S)
            if "有名额" in aim_clear:
                aim_clear[0] = time_str
                res_list.append(aim_clear)
        if len(res_list) != 0:
            print(res_list)
            with open("test.csv", "w", newline='') as csvfile:  # 保存到csv
                writer = csv.writer(csvfile)
                # 先写入columns_name
                writer.writerow(["time--这--", "id--是--", "dizhi--分--", "money--割--", "zhuangtai--线--"])
                # 写入多行用writerows
                writer.writerows(res_list)
        else:
            print('Soooo sad!!!{}--{}--没有考位...'.format(month, are))

    return driver


if __name__ == '__main__':
    driver = open_url()
    driver = login(driver)
    driver = search_zuowei(driver)

    for i in range(8, 12):
        if i < 10:
            test_month = '20180' + str(i)
        else:
            test_month = '2018' + str(i)
        try:
            driver = get_zuowei(driver, test_month, 'Beijing')
            driver.back()
            driver.refresh()
            time.sleep(15)
        except Exception as e:
            print(e)
            with open('error.txt', 'a') as f:
                f.write("{}{}-Beijing\n".format(e, test_month))

    driver.quit()

    print('查询结束.')
