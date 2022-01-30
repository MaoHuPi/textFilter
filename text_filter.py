import os
import numpy as np
import tkinter
import tkinter.font
from tkinter import messagebox
import pyglet
import pygame
import cv2
from PIL import ImageGrab
import time
import sys
# basic
VERSION = '2.0.0'
def tsj(t, s, j):
    t = str(t)
    s = str(s)
    j = str(j)
    return(j.join(t.split(s)))
def timeStr():
    T = time.localtime()
    def TJ(n:int, s:int):
                return(str(n).rjust(s, '0'))
    return('{yy}_{MM}_{dd} {hh}_{mm}_{ss}'.format(yy = TJ(T.tm_year, 4), MM = TJ(T.tm_mon, 2), dd = TJ(T.tm_mday, 2), hh = TJ(T.tm_hour, 2), mm = TJ(T.tm_min, 2), ss = TJ(T.tm_sec, 2)))
def exitTool():
    global run, font
    run = False
    cv2.destroyAllWindows()
    pygame.quit()
    pygame.font.quit()
    sys.exit()
# cv2
cam = 0
cap = False
proportion = 1
flip = False
video = False
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
camMax = 0
def capSet(capId):
    global cam, cap
    cam = capId
    cap = cv2.VideoCapture(capId)
def capDetect():
    global cam, camMax
    capSet(0)
    while int(cap.get(cv2.CAP_PROP_FPS)) != 0:
        capSet(cam+1)
    if cam == 0:
        cam,  camMax = -1, -1
        if messagebox.askokcancel('提醒','裝置未連接攝影鏡頭，是否重新偵測？\n(取消：只使用螢幕擷取)'):
            capDetect()
    else:
        camMax = cam-1
        capSet(-1)
# tkinter
run = False
win2 = tkinter.Tk()
win2.title('[Text Filter | 文字濾鏡] - 設定')
win2.iconbitmap('./image/icon.ico')
vnw = win2.winfo_screenwidth()/100
vnh = win2.winfo_screenheight()/100
vw = int(vnw*50)
vh = int(vnw*50*0.3997395833333333)
win2.geometry('%dx%d+%d+%d' % (vw, vh, int((vnw*100-vw)/2), int((vnh*100-vh)/2)))
win2.minsize(width = vw, height = vh)
vw = vw/100
vh = vh/100
# wD = 0.05339
wD = 0.03
formWidth = int(60*vnw*wD)
formFont = ('zpix', int(2*vw))
win2.resizable(0, 1)
win2.config(bg = '#000000')
texts = '文字濾鏡'
ohrs = []
def textSet():
    global texts, win2, run
    texts = itext.get()
    capDetect()
    run = True
    win2.destroy()
def _iteach():
    homeElements = [itext, isubmit, iteach, iabout]
    for E in homeElements:
        E.pack_forget()
    for ohr in ohrs:
        ohr.pack_forget()
    otitle.config(text = '[Text Filter | 文字濾鏡] - 使用教學')
    br(win2)
    br(win2)
    ocontent.config(text = '1. 在設定視窗的輸入欄位中輸入要做為濾鏡顯示的文字。\n\n2. 點擊設定視窗中的「送出文字」按鈕來完成設定。\n\n3. 待輸出視窗出現並開始攫取攝影鏡頭後，\n即可使用其它錄製、串流工具來擷取視窗輸出。\n\n4. 在輸出視窗中，可以透過「左」、「右」鍵來切換影像來源，\n亦可透過視窗邊框的拖曳來調整視窗大小(輸出解析度)，按下空白鍵則可水平翻轉輸入畫面。')
    ocontent.pack()
    br(win2)
    ihome.pack()
def _iabout():
    homeElements = [itext, isubmit, iteach, iabout]
    for E in homeElements:
        E.pack_forget()
    for ohr in ohrs:
        ohr.pack_forget()
    otitle.config(text = '[Text Filter | 文字濾鏡] - 關於軟體')
    br(win2)
    br(win2)
    ocontent.config(text = '名稱：Text Filter | 文字濾鏡\n\n版本：{version}\n\n程式：貓虎皮\n\n字體：Zpix'.format(version = VERSION))
    ocontent.pack()
    br(win2)
    ihome.pack()
def _ihome():
    homeElements = [ocontent, ihome]
    for E in homeElements:
        E.pack_forget()
    for ohr in ohrs:
        ohr.pack_forget()
    otitle.config(text = '[Text Filter | 文字濾鏡] - 設定')
    br(win2)
    br(win2)
    itext.pack()
    br(win2)
    isubmit.pack()
    br(win2)
    iteach.pack()
    br(win2)
    iabout.pack()
def br(window):
    ohr = tkinter.Label(window, text = '')
    ohr.config(bg = '#000000', fg = '#000000', width = int(50*vw*wD - (formWidth)/2), font = ('zpix', int(1*vw)))
    ohr.pack()
    ohrs.append(ohr)
pyglet.font.add_file('./font/Zpix.ttf')
otitle = tkinter.Label(win2, text = '[Text Filter | 文字濾鏡] - 設定')
otitle.config(bg = '#6464ff', fg = '#ffffff', width = int(100*vnw), font = ('zpix', int(3*vw)))
otitle.pack()
itext = tkinter.Entry(win2)
itext.config(bg = '#000000', fg = '#ffffff', width = formWidth, font = formFont)
isubmit = tkinter.Button(win2, text = '送出文字', command = textSet)
isubmit.config(bg = '#000000', fg = '#ffffff', width = formWidth, font = formFont)
iteach = tkinter.Button(win2, text = '使用教學', command = _iteach)
iteach.config(bg = '#000000', fg = '#ffffff', width = formWidth, font = formFont)
iabout = tkinter.Button(win2, text = '關於軟體', command = _iabout)
iabout.config(bg = '#000000', fg = '#ffffff', width = formWidth, font = formFont)
ocontent = tkinter.Label(win2, text = '')
ocontent.config(bg = '#000000', fg = '#ffffff', font = ('zpix', int(1.5*vw)), justify = 'left')
ihome = tkinter.Button(win2, text = '回到設定', command = _ihome)
ihome.config(bg = '#000000', fg = '#ffffff', width = formWidth, font = formFont)
_ihome()
win2.mainloop()
if run == False:
    exitTool()
if texts == '':
    texts = '文字濾鏡'
# pygame
pygame.init()
icon = pygame.image.load('./image/icon.png')
vw = int(vnw*50)
vh = int(vnw*50*0.3997395833333333)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (int((vnw*100-vw)/2), int((vnh*100-vh)/2))
win = pygame.display.set_mode((vw, vh))
pygame.display.set_icon(icon)
pygame.display.set_caption('[Text Filter | 文字濾鏡] - 輸出')
vw = vw/100
vh = vh/100
font = False
lastFontSize = 0
def fontSet(size, path = './font/Zpix.ttf'):
    global font, lastFontSize
    lastFontSize = size
    font = pygame.font.Font(path, size)
def fillText(self, text, x, y, fillStyle, againstX = 'left', againstY = 'top'):
    global font
    if(font == False):
        fontSet(1)
    size = {'w':0, 'h':0}
    size['w'], size['h'] = font.size(text)
    addX = size['w'] if againstX == 'right' else size['w']/2 if againstX == 'center' else 0
    addY = size['h'] if againstY == 'bottom' else size['h']/2 if againstY == 'center' else 0
    self.blit(font.render(text, True, fillStyle), (int(x-addX), int(y-addY)))
def fillRect(self, x, y, w, h, fillStyle):
        pygame.draw.rect(self, fillStyle, [int(x), int(y), int(w), int(h)], 0)
actionSideLength = 10
actionGap = 0.5
actionBgColor = (100, 100, 255)
actionFgColor = (255, 255, 255)
fillRect(win, (50-actionSideLength-actionGap)*vw, 50*vh-(actionSideLength+actionGap)*vw, actionSideLength*vw, actionSideLength*vw, actionBgColor)
fillRect(win, (50+actionGap)*vw, 50*vh+actionGap*vw, actionSideLength*vw, actionSideLength*vw, actionBgColor)
fontSet(int(actionSideLength*vw))
fillText(win, '文', (50-(actionSideLength/2+actionGap))*vw, 50*vh-(actionSideLength/2+actionGap)*vw, actionFgColor, againstX = 'center', againstY = 'center')
fillText(win, '字', (50+(actionSideLength/2+actionGap))*vw, 50*vh-(actionSideLength/2+actionGap)*vw, actionFgColor, againstX = 'center', againstY = 'center')
fillText(win, '濾', (50-(actionSideLength/2+actionGap))*vw, 50*vh+(actionSideLength/2+actionGap)*vw, actionFgColor, againstX = 'center', againstY = 'center')
fillText(win, '鏡', (50+(actionSideLength/2+actionGap))*vw, 50*vh+(actionSideLength/2+actionGap)*vw, actionFgColor, againstX = 'center', againstY = 'center')
pygame.display.update()
while run:
    if(cam < 0):
        ret = True
        frame = ImageGrab.grab(bbox = None)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    else:
        ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (int(vw*100), int(vw*100*len(frame)/len(frame[0]))))
        if flip:
            frame = cv2.flip(frame, 1, dst = None)
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        PixelSideLength = int(len(frame[0])/30)
        if(lastFontSize != int(PixelSideLength*0.8)):
            fontSet(int(PixelSideLength*0.8))
        # pygame.display.set_mode((len(frame[0]), len(frame)), pygame.RESIZABLE)
        fillRect(win, 0, 0, len(frame[0]), len(frame), (0, 0, 0))
        frameZpix = np.zeros((len(frame), len(frame[0]), 3), np.uint8)
        iMax = int(len(frame)/PixelSideLength)+1
        jMax = int(len(frame[0])/PixelSideLength)+1
        for i in range(0, iMax):
            for j in range(0, jMax):
                if(i*PixelSideLength < len(frame) and j*PixelSideLength < len(frame[0])):
                    color = frame[i*PixelSideLength, j*PixelSideLength]
                    textNum = int(frame2[i*PixelSideLength, j*PixelSideLength, 0]/(255/6))
                    if len(texts) > 6:
                        textNum += 6*int(frame2[i*PixelSideLength, j*PixelSideLength, 2]/(255/2))
                    color = (int(color[2]), int(color[1]), int(color[0]))
                    fillText(win, texts[textNum % len(texts)], j*PixelSideLength, i*PixelSideLength, color)
        pygame.display.update()
    else:
        print('[ERROR] 圖片捕捉失敗')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitTool()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cam2 = cam-1 if cam > -1 else -1
                if cam != cam2:
                    capSet(cam2)
            elif event.key == pygame.K_RIGHT:
                cam2 = cam+1 if cam < camMax else camMax
                if cam != cam2:
                    capSet(cam2)
            elif event.key == pygame.K_SPACE:
                flip = not flip
    pygame.time.Clock().tick(1000)
    if ret:
        i = tsj(tsj(str(pygame.display.get_surface()), '(', 'x'), ')', 'x').split('x')
        if vw*100 != int(i[1]) or vh*100 != int(i[1])/2:
            vw = int(i[1])/100
            vh = int(i[1])*len(frame)/len(frame[0])/100
            pygame.display.set_mode((int(vw*100), int(vh*100)), pygame.RESIZABLE)
    else:
        print('[ERROR] 視窗縮放失敗')
