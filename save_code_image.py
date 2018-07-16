from selenium import webdriver
import time
import os
import urllib.request

def open_url():
    driver = webdriver.Firefox()
    driver.get("https://toefl.etest.net.cn/cn/")
    
    return driver

def login(driver):

    image_dir = '/home/wengzh/Documents/tofel_images'

    if not os.path.exists(image_dir):
        os.mkdir(image_dir)

    for i in range(3000):
        driver.find_element_by_id("a_changeone").click()
        # get code content image
        image = driver.find_element_by_xpath("//img[@id='imgVerifycode']").get_attribute("src")

        file_name = os.path.basename(image)

        file_name = os.path.join(image_dir, file_name)

        urllib.request.urlretrieve(image, file_name)

        time.sleep(2)


def close(driver):
    """关闭浏览器"""
    driver.quit()


def save_image(image_dir):
    n = 0
    while n<6000:
        file_name = os.path.join(image_dir, str(n)+'.jpg')
        urllib.request.urlretrieve('https://toefl.etest.net.cn/cn/15288554340750.08946816043956507VerifyCode3.jpg', file_name)
        n += 1
        if n%50 == 0:
            print('已完成{}张下载'.format(n))

if __name__ == '__main__':
    # driver = open_url()
    # driver = login(driver)
    # close(driver)
    save_image('/home/wengzh/Documents/tofel_images')