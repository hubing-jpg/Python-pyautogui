from check import find_image_on_screen,check
import pyautogui,time,sys,os



def speed():
    while True:
        time.sleep(1)
        if check('black'):
            continue
        else :
            print('尝试拖动进度条')
            # pyautogui.moveRel(800, 400, duration=0.6)
            try:
                if find_image_on_screen('line1'):
                    pyautogui.click(find_image_on_screen('line1')[0], find_image_on_screen('line1')[2],
                                    duration=1)
                elif find_image_on_screen('line2',threshold=0.6):
                    pyautogui.click(find_image_on_screen('line2',threshold=0.6)[0], find_image_on_screen('line2',threshold=0.6)[2],
                                    duration=1)
            except:
                print("未匹配到进度条")
            break

def watch_ppt():
    print('开始检测ppt')
    time.sleep(2)#等待加载ppt
    while True:
        if find_image_on_screen('yellow1',reg=(0,0,1920,410)):#检测是否已经看完ppt
            pyautogui.moveTo(500,500,duration=1)# 将鼠标移至ppt中
            old_screen=pyautogui.screenshot()
            pyautogui.scroll(-800)#滚动ppt
            new_screen = pyautogui.screenshot()
            if old_screen==new_screen:
                print('未检测到ppt.')
                return True
            elif old_screen!=new_screen:
                print('正在阅读')
                time.sleep(1)
                continue# 直到黄色任务点消失才执行下一步
        elif find_image_on_screen('green1',reg=(0,0,1920,410)):#检测是否出现任务点已完成的绿色字样
            print('已看完ppt')
            pyautogui.moveTo(30  ,500,duration=1)# 将鼠标移至ppt外
            pyautogui.scroll(-400)#向下滚动
            return True
        else:
            print('未检测到ppt')
            return False

def watch_vido():
    j=0
    while check('green1')==False or check('blue1')==False:
        print('开始检测视频')
        pyautogui.moveTo(30, 500, duration=1)
        time.sleep(1)#等待加载视频
        if find_image_on_screen('green1',reg=(0,0,1920,410)):#一开就检测是否已经播放完视频
            pyautogui.scroll(-200)
            print('已看完视频')
            break
        elif check('green1')==False and check('yellow1')==False and check('blue1'):
            break
        else:
            try:#；两种检测视频播放按钮是否存在的方法，如果第一种方法没检测到则用第二种方法，检测到存在后定位坐标并点击，显示开始播放视频
                if find_image_on_screen('play',threshold=0.6):
                    pyautogui.click(find_image_on_screen('play',threshold=0.6)[0], find_image_on_screen('play',threshold=0.6)[1],duration=1)
                else:
                    play_pos = pyautogui.locateOnScreen(r'.\img\img_play.png', confidence=0.5)
                    pyautogui.click(play_pos, duration=1)
                print('开始播放视频')
                # speed()
                defend()

            except: #如果多没找到就显示未找到视频，并向下滚动页面，退出循环
                    print('未找到视频')
                    pyautogui.scroll(-100)
                    j+=1
                    continue

def get_next():#跳转下一节
    next_button = pyautogui.locateOnScreen(r'.\img\img_blue1.png', confidence=0.9)
    pyautogui.click(next_button, duration=1)
    print('播放下一节')

def pass_page():#如果出现文章、测试、或这一节的视频和ppt都已经看完
    while not check('blue1'):#如果没检测到下一节按钮就一直向下滑页面
        pyautogui.scroll(-800)
    if check('blue1'):
        get_next()#检测到后就点击下一节
        time.sleep(1)
        if find_image_on_screen('again1'):
            get_next()#再次点击
    else:
        print('未检测到下一节按钮')

def wait():
    # 总进度
    total = 100
    for i in range(total + 1):
        # 模拟延时
        time.sleep(0.05)  # 每1%进度延时0.1秒

        # 计算进度条显示
        filled_length = int(50 * i // 100)  # 按比例计算填充长度
        bar = '█' * filled_length + '-' * (50 - filled_length)  # 构造进度条显示字符串

        # 输出进度条
        sys.stdout.write('\r进度 |%s| %d%%' % (bar, i))  # 使用'\r'回车到行首，输出进度条和百分比
        sys.stdout.flush()  # 立即刷新输出缓冲区
    print('\n')

def record(num):
    f=open('record.txt','a',encoding='utf-8')
    f.write(f'已看完{num}节，完成时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}\n')

def defend():
    print('开始防锁屏')
    old_mouse_pos=pyautogui.position()
    # 记录开始时间
    start_time = time.time()
    while True:
        # 计算已过去的时间
        elapsed_time = time.time() - start_time
        # 检查是否已过四分钟
        if  elapsed_time >= 2 * 60:
            new_mouse_pos=pyautogui.position()
            if old_mouse_pos==new_mouse_pos:
                pyautogui.move(-50, -50)  # 将鼠标稍微移动
                pyautogui.move(50, 50)  # 将鼠标稍微移动
                start_time = time.time()#重置时间
                old_mouse_pos=new_mouse_pos
                print('2分钟鼠标未动，我浅动一下')
            else:
                start_time = time.time()  # 重置时间
                old_mouse_pos = new_mouse_pos
        elif find_image_on_screen('green1',reg=(0,0,1920,410)):
            pyautogui.scroll(-300)
            print('已看完视频')
            break


def main(num=20):
    print('开始刷课')
    k=1
    while k<=num:
        time.sleep(2.5)
        if check('write'):
            wait()
        #检测是否存在视频
        if check('play',threshold=0.6) or find_image_on_screen('play',threshold=0.6):
            watch_vido()
            pass_page()
        else:
            if watch_ppt():
                watch_vido()
            pass_page()
        record(k)
        k+=1


def off_computer():
    time.sleep(3600)
    os.system('shutdown /s /t 0')

