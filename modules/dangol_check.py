import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from menu import *
from dangol import *
import face_recog

find_people_UI = '../_uiFiles/dangol_find_people.ui'
re_check_UI = '../_uiFiles/re_check.ui'

# 단골인식 후보 저장 배열
candidate=[]

class checker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(find_people_UI, self)
        

        #setStyleSheet
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.lower()
        self.btn_dg_basic.setStyleSheet("background-image:url(../image/dangol_find_people/basic_order.PNG)")
        self.btn_dg_yes.setStyleSheet("background-image:url(../image/dangol_find_people/yes.PNG)")
        self.btn_dg_no.setStyleSheet("background-image:url(../image/dangol_find_people/no.PNG)")
        
        self.dg_number.setFont(QFont('나눔스퀘어 bold', 28))
        self.dg_most.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_1.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_2.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_3.setFont(QFont('나눔스퀘어 bold', 15))

        self.btn_dg_no.clicked.connect(self.no)
        #self.skip_btn.clicked.connect(self.skip)

        self.last=[self.dg_last_1, self.dg_last_2, self.dg_last_3]

        rr.re_btn.clicked.connect(self.rere)


    def faceCheck(self):
        global candidate
        candidate = list(reversed(face_recog.your_face()))
        print(candidate)
    

    def yes(self):
        now_member=str(int(candidate[-1])//2).zfill(5)
        return now_member
    
    def no(self):
        if len(candidate)>1:
            candidate.pop()
            self.refresh()
        else:
            rr.show()

    def rere(self):
        self.faceCheck()
        self.refresh()

    def refresh(self):
        now_member=str(int(candidate[-1])//2).zfill(5)

        # 회원번호 출력
        self.dg_number.setText(str(member_dict[now_member].number))
        
        # 가장 많이 주문한 메뉴 출력
        menu,side_list,side,drink=member_dict[now_member].preference()
        self.preference=[menu,side_list,drink,side]
        if member_dict[now_member].age==0: # 노인
            self.dg_most.setPlainText(menu_name[menu]+" | " + " | ".join([old_igr_name[idx] for idx,i in enumerate(side_list) if i==1]) + "\n" 
                            + old_drk_name[drink] + " | " +old_side_name[side])
        else:
            self.dg_most.setPlainText(menu_name[menu]+" | "+ " | ".join([igr_name[idx] for idx,i in enumerate(side_list) if i==1]) + "\n"
                              +drk_name[drink] + " | " + side_name[side])
        
        # 최근 주문한 메뉴 출력
        self.num, self.recent=member_dict[now_member].recent()

        for i in range(self.num):
            x,menu,side_list,side,drink=self.recent[i]
            if member_dict[now_member].age==0: # 노인
                self.last[i].setPlainText(menu_name[menu]+" | " + " | ".join([old_igr_name[idx] for idx,i in enumerate(side_list) if i==1]) + "\n"
                                  +old_drk_name[drink] + " | " +old_side_name[side])
            else:
                self.last[i].setPlainText(menu_name[menu]+" | "+ " | ".join([igr_name[idx] for idx,i in enumerate(side_list) if i==1]) + "\n"
                                  +drk_name[drink] + " | " + side_name[side])


class re_check(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(re_check_UI, self)

        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        self.label_re_check.setStyleSheet("background-image:url(../image/re_check/fail.PNG)")
        self.re_btn.setStyleSheet("background-image:url(../image/re_check/re_check.PNG)")
        self.skip_btn2.setStyleSheet("background-image:url(../image/re_check/fail.PNG)")
    
        self.re_btn.clicked.connect(self.hide)
        self.skip_btn2.clicked.connect(self.hide)


rr = re_check()