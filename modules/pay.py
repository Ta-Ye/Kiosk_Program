import sys
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from dangol import *
from menu import *

pay_UI = '../_uiFiles/final_payment.ui'

STOREKEY = ""
STORENAEM = ""

class payment(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(pay_UI, self)
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        self.member_line.setFont(QFont('나눔스퀘어 bold', 20))
        self.basket_line.setFont(QFont('나눔스퀘어 bold', 20))
        self.payment_line.setFont(QFont('나눔스퀘어 bold', 20))
        
        self.member=""
        self.basket=[]
        self.cost=0
        self.age_result=0

        self.back_btn.clicked.connect(self.hide)
        self.card_btn.clicked.connect(self.end)

        self.back_btn.setStyleSheet("background-image:url(../image/final_payment/back.PNG)")
        self.card_btn.setStyleSheet("background-image:url(../image/final_payment/pay_card.PNG)")


    def refresh(self,now_member,age_result, basket, total_cost):
        self.member=now_member
        self.basket=basket
        self.cost=total_cost
        self.age_result=age_result

        # 번호표시
        if now_member=="":
            self.member_line.hide()
        else:
            self.member_line.show()
            ss=member_dict[now_member].number+"님의 주문 내역"
            self.member_line.setText(ss)
        # 주문내역 표시
        self.basket_line.setPlainText("")
        for order in basket:
            num,menu,side_list,side,drink=order
            if num==0:
                continue
            if age_result==0: # 노인
                self.basket_line.insertPlainText(menu_name[menu]+" | "+" | ".join([old_igr_name[idx] for idx,i in enumerate(side_list) if i==1])
                                  +old_drk_name[drink] + " | " +old_side_name[side]+"\n\n")
            else:
                self.basket_line.insertPlainText(menu_name[menu]+" | "+" | ".join([igr_name[idx] for idx,i in enumerate(side_list) if i==1])
                                  +drk_name[drink] + " | " + side_name[side]+"\n\n")
        
        # 가격 표시
        self.payment_line.setText(str(total_cost)+" 원")

        self.show()

    def end(self):
        if self.member!="":
            member_dict[self.member].add_order(self.basket,self.cost)
            write(self.member, self.age_result, self.cost, member_dict[self.member].number, self.basket)
        age_list[self.age_result].add_order(self.basket)
        addOrderForAge(self.basket, self.age_result, STOREKEY)
        self.hide()
    

