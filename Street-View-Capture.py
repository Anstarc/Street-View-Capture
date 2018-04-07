from selenium import webdriver
from selenium.webdriver.common.by import By
import ctypes
import time
import math

HEADING_ADD = 1
PITCH_ADD = 2

heading = 0
pitch = 10

heading_max = 180
pitch_max = -60

heading_step = 10

browser = webdriver.Firefox()

def init():
    
    url = "http://www.earthol.org/city-319.html"
    browser.set_window_size(1920, 1080)
    browser.get(url)
    
    print('Ready?')

    if input() != '1':
        print('Not ready')
        #exit()
        return 1
    '''
    global heading, pitch

    r = browser.execute_script('return pano.getPov()')
    print(r['heading'], r['pitch'])

    heading = r['heading']
    pitch = r['pitch']
    '''
    
def rotate(dir):
    global heading, pitch
    
    if dir == HEADING_ADD:
        heading += heading_step
        pitch = 10

    if dir == PITCH_ADD:
        pitch -= 10

    browser.execute_script('pano.setPov({heading:' + str(heading%360) + ', pitch:' + str(pitch) +'})')
    

def sort(a, b):
    if a > b:
        return b, a
    else:
        return a, b

def initOnce():
    global heading_max, heading

    r = browser.execute_script('return pano.getPov()')
    start = r['heading']
    print(start)

    input('结束？')
    
    r = browser.execute_script('return pano.getPov()')
    end = r['heading']
    print(end)

    if math.fabs(end-start) < 180:
        heading, heading_max = sort(start, end)
        
    else:
        heading_max, heading = sort(start, end)
        heading_max += 360

    print(heading, heading_max)
    browser.execute_script('pano.setPov({heading:' + str(heading) + ', pitch:10})')



def main():

    
    if init() == 1:
        return
    
    a = browser.find_element(by=By.ID, value="panomap")
    s = ''
    
    while True:
        if s != '2':
            ctypes.windll.user32.MessageBoxA(0,u"是否继续？".encode('gb2312'),u' 信息'.encode('gb2312'),0)
        s = input()
        if s == '0':
            break
        elif s == '2':
            r = browser.execute_script('return pano.getPov()')
            print(r['heading'], r['pitch'])
            continue
        elif s == 's':
            initOnce()
        else:
            continue

        pos = browser.execute_script('return pano.getPosition().toUrlValue()')

        while heading <= heading_max:

            while pitch >= pitch_max:
                time.sleep(1)
                print('I:\\Ubuntu\\data\\raw\\' + pos + '_' + str(heading) + '_' + str(pitch) + '.png\n')
                a.screenshot('I:\\Ubuntu\\data\\raw\\' + pos + '_' + str(heading) + '_' + str(pitch) + '.png')
                rotate(PITCH_ADD)

            rotate(HEADING_ADD)
    


    browser.close()  



if __name__ == '__main__':
    main()
