import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import dangol_check
from dangol import *
from menu import *


dangol_order_UI = '../_uiFiles/dangol_order.ui'

class dangol_order(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(dangol_order_UI, self)

        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.lower()
        self.plz_bg.lower()
        self.plz_bg.lower()
        self.plz_bg.lower()
        self.last=[self.dg_last_1, self.dg_last_2, self.dg_last_3]
        
        self.btn_dg_most.setStyleSheet("background-image:url(../image/dangol_order/dg_order.PNG)")
        self.btn_dg_last_1.setStyleSheet("background-image:url(../image/dangol_order/dg_order.PNG)")
        self.btn_dg_last_2.setStyleSheet("background-image:url(../image/dangol_order/dg_order.PNG)")
        self.btn_dg_last_3.setStyleSheet("background-image:url(../image/dangol_order/dg_order.PNG)")
        self.btn_dg_basic.setStyleSheet("background-image:url(../image/dangol_order/keep.PNG)")

        self.dg_number.setFont(QFont('나눔스퀘어 bold', 28))
        self.dg_most.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_1.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_2.setFont(QFont('나눔스퀘어 bold', 15))
        self.dg_last_3.setFont(QFont('나눔스퀘어 bold', 15))

        #메뉴
        self.preference=[]
        self.recent=[]
        self.num=0

    def refresh(self,now_member):
        # 회원번호 출력
        self.dg_number.setText(str(member_dict[now_member].number))

        # 가장 많이 주문한 메뉴 출력
        menu,side_list,side,drink=member_dict[now_member].preference()
        self.preference=[1,menu,side_list,drink,side]
        if member_dict[now_member].age==1: # 노인
            self.dg_most.setText(menu_name[menu]+" | "
                              +old_drk_name[drink] + " | " +old_side_name[side])
        else:
            self.dg_most.setText(menu_name[menu]+" | "
                              +drk_name[drink] + " | " + side_name[side])
        
        # 최근 주문한 메뉴 출력
        self.num, self.recent=member_dict[now_member].recent()

        for i in range(self.num):
            x,menu,side_list,side,drink=self.recent[i]
            if member_dict[now_member].age==1: # 노인
                self.last[i].setText(menu_name[menu]+" | "
                                  +old_drk_name[drink] + " | " +old_side_name[side])
            else:
                self.last[i].setText(menu_name[menu]+" | "
                                  +drk_name[drink] + " | " + side_name[side])
        
        
    def most(self):
        return self.preference
    def last1_f(self):
        return [1]+self.recent[0][1:]
    def last2_f(self):
        if self.num>1:
            return [1]+self.recent[1][1:]
    def last3_f(self):
        if self.num>2:
            return [1]+self.recent[2][1:]