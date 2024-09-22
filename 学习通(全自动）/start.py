from selenium import webdriver
from selenium.webdriver.common.by import By
import time,pyautogui
from process import main

def find_img(name,threshold=0.8):
    while True:
        time.sleep(2)
        try:
            img = pyautogui.locateOnScreen(r'.\img\img_'+f'{name}'+'.png', confidence=threshold)
            pyautogui.click(img, duration=1)
            break
        except:
            continue
def find_img1(name,threshold=0.8):
    while True:
        time.sleep(1)
        pyautogui.scroll(-100)
        try:
            time.sleep(1)
            img = pyautogui.locateOnScreen(r'.\img\img_'+f'{name}'+'.png', confidence=threshold)
            pyautogui.click(img, duration=1)
            break
        except:
            continue
def login_to_course(t,num):
    driver = webdriver.Edge()
    driver.get('https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com')

    element = driver.find_element(By.ID, 'phone')
    element1 = driver.find_element(By.ID, 'pwd')
    element.send_keys('your phone number')#有替换成你的手机号码
    element1.send_keys('your password')#替换成你的密码

    # 点击登录
    login_button = driver.find_element(By.ID, 'loginBtn')
    login_button.click()

    print('开始调整窗口大小')
    pyautogui.click(500, 40, duration=1)
    fw = pyautogui.getActiveWindow()
    time.sleep(1)
    fw.topleft = (-10, 0)
    fw.width = 1470
    fw.height=1080
    time.sleep(5)
    pyautogui.click(622,330)
    find_img('my_study')
    time.sleep(1)
    find_img1('course')#替换成你需要看的课程的截图，可以看我提供的例子，在img文件中对应名称查找img_course.png
    # time.sleep(5)
    # pyautogui.click(100,550,duration=0.5)
    find_img('chapter1')
    pyautogui.moveRel(200,0,duration=0.5)
    find_img1('chapter',threshold=0.9)
    # time.sleep(5)
    # pyautogui.click(1400,240,duration=0.5)
    find_img('fold')
    time.sleep(3)
    main(num)
    time.sleep(t)
    driver.quit()

if __name__ == '__main__':
    login_to_course(3600,20)#第一个参数是窗口维持的时间，第二个是要看的章节数