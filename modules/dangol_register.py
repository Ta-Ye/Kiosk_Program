import sys
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import cv2,os, threading
import SSD_face_detector
from dangol import *
import menu

register_UI = '../_uiFiles/dangol_register.ui'
start_UI = '../_uiFiles/start.ui'

new_member=0
    
class register(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(register_UI, self)

        #setStyleSheet
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.dg_intro_label.setStyleSheet("background-image:url(../image/dangol_register/dg_intro.PNG)")
        self.btn_0.setStyleSheet("background-image:url(../image/dangol_register/0.PNG)")
        self.btn_1.setStyleSheet("background-image:url(../image/dangol_register/1.PNG)")
        self.btn_2.setStyleSheet("background-image:url(../image/dangol_register/2.PNG)")
        self.btn_3.setStyleSheet("background-image:url(../image/dangol_register/3.PNG)")
        self.btn_4.setStyleSheet("background-image:url(../image/dangol_register/4.PNG)")
        self.btn_5.setStyleSheet("background-image:url(../image/dangol_register/5.PNG)")
        self.btn_6.setStyleSheet("background-image:url(../image/dangol_register/6.PNG)")
        self.btn_7.setStyleSheet("background-image:url(../image/dangol_register/7.PNG)")
        self.btn_8.setStyleSheet("background-image:url(../image/dangol_register/8.PNG)")
        self.btn_9.setStyleSheet("background-image:url(../image/dangol_register/9.PNG)")
        self.btn_cancel.setStyleSheet("background-image:url(../image/dangol_register/back.PNG)")
        self.btn_clr.setStyleSheet("background-image:url(../image/dangol_register/clr.PNG)")
        self.dg_register.setStyleSheet("background-image:url(../image/dangol_register/dg_rec_ok.PNG)")
        self.dg_back.setStyleSheet("background-image:url(../image/dangol_register/dg_back.PNG)")

        self.dg_back.clicked.connect(self.regi_stop)
        self.btn_cancel.clicked.connect(self.one_delete)
        self.running=False
        
        self.btn_0.clicked.connect(lambda: self.write_edit(button=0))
        self.btn_1.clicked.connect(lambda: self.write_edit(button=1))        
        self.btn_2.clicked.connect(lambda: self.write_edit(button=2))
        self.btn_3.clicked.connect(lambda: self.write_edit(button=3))
        self.btn_4.clicked.connect(lambda: self.write_edit(button=4))
        self.btn_5.clicked.connect(lambda: self.write_edit(button=5))
        self.btn_6.clicked.connect(lambda: self.write_edit(button=6))
        self.btn_7.clicked.connect(lambda: self.write_edit(button=7))
        self.btn_8.clicked.connect(lambda: self.write_edit(button=8))
        self.btn_9.clicked.connect(lambda: self.write_edit(button=9))

    def write_edit(self, button):
        self.dg_cur_num.setText(self.dg_cur_num.text() + str(button))

    def one_delete(self):
        arr = self.dg_cur_num.text()
        self.dg_cur_num.setText(arr[0:-1])
        
    def run(self):
        while self.running:
            ret, frame= menu.cap.read()
            if ret:
                img= cv2.resize(frame,dsize=(400,400),interpolation=cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h,w,c = img.shape
                qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                self.dg_video.setPixmap(pixmap)
                self.dg_video.show()
        self.dg_video.hide()

    def regi_stop(self):
        self.hide()
        self.running=False

    def member_register(self):
        global new_member
        dangol_number = self.dg_cur_num.text()
        print(dangol_number)

        count = 0
        print(len(dangol_number))
        for i in dangol_number:
            count += len(i)

        if count == 4:
            self.running=False
            age=SSD_face_detector.save(new_member)
            self.hide()
            name=str(new_member//2+new_member%2).zfill(5)
            print(name)
            member_dict[name]=member(name,age,dangol_number)
            new_member+=2
            return name