import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import threading

app = QApplication(sys.argv)

import dangol_order
import dangol_check
import dangol_register
import dangol
import pay
from menu import *
from dangol import *
import copy
import SSD_face_detector


kiosk_UI = '../_uiFiles/main_window.ui'
basic_UI = '../_uiFiles/basic.ui'
menu_list_UI = '../_uiFiles/menu_list.ui'
now_UI = '../_uiFiles/now.ui'
add_UI = '../_uiFiles/add.ui'

pay_UI = '../_uiFiles/pay.ui'
pay_list_UI = '../_uiFiles/pay_list.ui'
young_UI = '../_uiFiles/young.ui'

old_UI = '../_uiFiles/old.ui'
old_basic_UI = '../_uiFiles/old_basic.ui'
old_insert_UI = '../_uiFiles/old_insert.ui'


# 상수들 #
menu_idx = 0

basket = []
total_cost = 0
sample = [1, 99, [0, 0, 0, 0, 0, 0], 0, 0]
temp_order = []
age_result = 99

"""
갯수, 메뉴, [올엑스트라, X , 치즈(장수), 베이컨(장수),화이트치즈(장수)
할라피뇨(갯수)],음료,사이드
"""

status_ext = [0] * 10
status_drk = [0] * 6
status_side = [0] * 6

# 모듈 return 값 저장


def age_check():
    global age_result
    age_result=SSD_face_detector.facecheck()

# 계산 관련 함수들 #
def Cal_now(temp):
    add_temp = 0
    result = 0
    for i in range(0, 6):
        add_temp += temp[2][i] * add_price[i]
    result += event_price[temp[1]] + add_temp + \
        drk_price[temp[3]] + side_price[temp[4]]
    return result * temp[0]


def Cal_total_price():
    global total_cost
    total_result = 0
    for order in basket:
        if order[0] != 0:
            total_result += Cal_now(order)
    total_cost = total_result
    return total_result


def Cal_total_counts():
    total_counts = 0
    for order in basket:
        if order[0] != 0:
            total_counts += order[0]
    return total_counts


# 내부 동작 #
def next_idx():
    global menu_idx
    menu_idx += 1


def set_idx(num):
    global menu_idx
    menu_idx = num


def create_order(menu_num):
    global temp_order
    temp_order = copy.deepcopy(sample)
    temp_order[1] = menu_num


# add로 인한 order 변경

def change_igr(igr_num):
    """
    [올엑스트라, X , 치즈(장수), 베이컨(장수),화이트치즈(장수), 할라피뇨(갯수)],
    """
    global temp_order

    if igr_num == 0 or igr_num == 1:
        temp_order[2][igr_num] += 1
    elif igr_num == 2:
        temp_order[2][2] += 1
    elif igr_num == 3:
        temp_order[2][2] += 2
    elif igr_num == 4:
        temp_order[2][3] += 1
    elif igr_num == 5:
        temp_order[2][3] += 2
    elif igr_num == 6:
        temp_order[2][4] += 1
    elif igr_num == 7:
        temp_order[2][4] += 2
    elif igr_num == 8:
        temp_order[2][5] = + 2
    elif igr_num == 9:
        temp_order[2][5] += 4


def change_side(side_num):
    global temp_order
    temp_order[3] = side_num


def change_drk(drk_num):
    global temp_order
    temp_order[4] = drk_num


# 어린이 추천메뉴

class young(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(young_UI, self)
        #self.bgplz.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        self.old_rec_menu1.setStyleSheet(
            "background-image:url(../image/young/yg_recmenu1.PNG)")
        self.old_rec_menu2.setStyleSheet(
            "background-image:url(../image/young/yg_recmenu2.PNG)")
        self.old_rec_menu3.setStyleSheet(
            "background-image:url(../image/young/yg_recmenu3.PNG)")
        self.old_rec_menu4.setStyleSheet(
            "background-image:url(../image/young/yg_recmenu4.PNG)")
        self.old_rec_ok.setStyleSheet(
            "background-image:url(../image/old/old_rec_ok.PNG)")

        self.old_rec_menu1.clicked.connect(lambda: self.click_event(0))
        self.old_rec_menu2.clicked.connect(lambda: self.click_event(1))
        self.old_rec_menu3.clicked.connect(lambda: self.click_event(2))
        self.old_rec_menu4.clicked.connect(lambda: self.click_event(3))
        # self.old_rec_ok.clicked.connect(lambda: main_window.old_nope())

    def click_event(self, num):
        create_order(num)
        main_window.B_to_N()


# OLD
class old(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(old_UI, self)
        #self.bgplz.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        self.old_rec_ok.clicked.connect(lambda: main_window.Set_OldB())

    def refresh(self):
        prefer = getMenusByAge(pay.STORENAME, pay.STOREKEY,age_result)
        if len(prefer)==4:
            self.old_rec_menu1.setStyleSheet("background-image:url(../image/old/" + str(int(prefer[0].get("menuNum"))-1) + ".PNG)")
            self.old_rec_menu2.setStyleSheet("background-image:url(../image/old/" + str(int(prefer[1].get("menuNum"))-1) + ".PNG)")
            self.old_rec_menu3.setStyleSheet("background-image:url(../image/old/" + str(int(prefer[2].get("menuNum"))-1) + ".PNG)")
            self.old_rec_menu4.setStyleSheet("background-image:url(../image/old/" + str(int(prefer[3].get("menuNum"))-1) + ".PNG)")
            self.old_rec_ok.setStyleSheet("background-image:url(../image/old/old_rec_ok.PNG)")

            self.old_rec_menu1.clicked.connect(
                lambda: self.click_event(int(prefer[0]["menuNum"])))
            self.old_rec_menu2.clicked.connect(
                lambda: self.click_event(int(prefer[1]["menuNum"])))
            self.old_rec_menu3.clicked.connect(
                lambda: self.click_event(int(prefer[2]["menuNum"])))
            self.old_rec_menu4.clicked.connect(
                lambda: self.click_event(int(prefer[3]["menuNum"])))


    def click_event(self, num):
        create_order(num)
        main_window.B_to_N()


class old_basic(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(old_basic_UI, self)
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        QScroller.grabGesture(self.scrollArea.viewport(),
                               QScroller.LeftMouseButtonGesture)
        # QScroller.grabGesture(self.scroll_burger_2.viewport(),
        #                       QScroller.LeftMouseButtonGesture)
        # QScroller.grabGesture(self.scroll_side_2.viewport(),
        #                       QScroller.LeftMouseButtonGesture)
        # QScroller.grabGesture(self.scroll_drink.viewport(),
        #                       QScroller.LeftMouseButtonGesture)
        # QScroller.grabGesture(self.scroll_basket.viewport(),
        #                       QScroller.LeftMouseButtonGesture)

        self.Button_set.clicked.connect(lambda: self.menu(num=0))
        self.Button_burger.clicked.connect(lambda: self.menu(num=1))
        self.Button_side.clicked.connect(lambda: self.menu(num=2))
        self.Button_drink.clicked.connect(lambda: self.menu(num=3))

        self.all_cancel.clicked.connect(lambda: old_mn.all_clear())
        self.btn_pay.clicked.connect(self.ppp)

        self.all_price.setFont(QFont('나눔스퀘어 bold', 28))


        self.set_1.clicked.connect(lambda: self.click_event(0))
        self.set_2.clicked.connect(lambda: self.click_event(1))
        self.set_3.clicked.connect(lambda: self.click_event(2))
        self.set_4.clicked.connect(lambda: self.click_event(3))
        self.set_5.clicked.connect(lambda: self.click_event(4))
        self.set_6.clicked.connect(lambda: self.click_event(5))


        self.set_1.setStyleSheet("background-image:url(../image/old/0.PNG)")
        self.set_2.setStyleSheet("background-image:url(../image/old/1.PNG)")
        self.set_3.setStyleSheet("background-image:url(../image/old/2.PNG)")
        self.set_4.setStyleSheet("background-image:url(../image/old/3.PNG)")
        self.set_5.setStyleSheet("background-image:url(../image/old/4.PNG)")
        self.set_6.setStyleSheet("background-image:url(../image/old/5.PNG)")



    def ppp(self):
        p.refresh(now_member, age_result, basket, total_cost)

    def menu(self, num):
        self.basic_Widget.setCurrentIndex(num)

    def click_event(self, num):
        create_order(num)
        main_window.B_to_N()

    def insert_basket(self):
        match = False
        global temp_order
        global menu_idx
        igr_match = 0
        match_index = 100

        if len(basket) == 0:
            basket.append(temp_order)
            self.Layout_basket.addWidget(old_mn.return_list(menu_idx))
            next_idx()
        else:
            for i in range(len(basket)):
                if basket[i][1] == temp_order[1] and basket[i][3] == temp_order[3] and basket[i][4] == temp_order[4]:
                    for k in range(6):
                        if basket[i][2][k] == temp_order[2][k]:
                            igr_match += 1
                    if igr_match == 6:
                        match = True
                        basket[i][0] += 1
                        match_index = i
                        break

            if match:
                old_mn.return_list(match_index)
            else:
                basket.append(temp_order)
                self.Layout_basket.addWidget(old_mn.return_list(menu_idx))
                next_idx()
        self.total_print()

    def total_print(self):
        self.all_price.setPlainText(
            '총 주문금액  :  ' + str(Cal_total_price()) + '원')


class old_menu_list(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(old_insert_UI, self)

        self.cancel_1.clicked.connect(lambda: self.delete_list(0))
        self.cancel_2.clicked.connect(lambda: self.delete_list(1))
        self.cancel_3.clicked.connect(lambda: self.delete_list(2))
        self.cancel_4.clicked.connect(lambda: self.delete_list(3))
        self.cancel_5.clicked.connect(lambda: self.delete_list(4))
        self.cancel_6.clicked.connect(lambda: self.delete_list(5))
        self.cancel_7.clicked.connect(lambda: self.delete_list(6))
        self.cancel_8.clicked.connect(lambda: self.delete_list(7))
        self.cancel_9.clicked.connect(lambda: self.delete_list(8))
        self.cancel_10.clicked.connect(lambda: self.delete_list(9))
        self.cancel_11.clicked.connect(lambda: self.delete_list(10))
        self.cancel_12.clicked.connect(lambda: self.delete_list(11))

        self.W = [self.w_1, self.w_2, self.w_3, self.w_4, self.w_5, self.w_6,
                  self.w_7, self.w_8, self.w_9, self.w_10, self.w_11, self.w_12]
        self.name = [self.name_1, self.name_2, self.name_3, self.name_4, self.name_5, self.name_6,
                     self.name_7, self.name_8, self.name_9, self.name_10, self.name_11, self.name_12]
        self.counts = [self.counts_1, self.counts_2, self.counts_3, self.counts_4, self.counts_5, self.counts_6,
                       self.counts_7, self.counts_8, self.counts_9, self.counts_10, self.counts_11, self.counts_12]
        self.price = [self.price_1, self.price_2, self.price_3, self.price_4, self.price_5,
                      self.price_6, self.price_7, self.price_8, self.price_9, self.price_10, self.price_11, self.price_12]

    def return_list(self, cur_idx):

        global basket
        global temp_order

        name_idx = int(basket[cur_idx][1])
        cnt = int(basket[cur_idx][0])
        side_idx = int(basket[cur_idx][3])
        drk_idx = int(basket[cur_idx][4])
        igr_list = basket[cur_idx][2]

        d = " +"
        temp_igr = ""
        self.W[cur_idx].show()

        self.price[cur_idx].setText(str(Cal_now(basket[cur_idx])) + "원")
        self.counts[cur_idx].setText(str(cnt))

        for i in range(len(igr_list)):
            if igr_list[i] == 1:
                if temp_igr == "":
                    temp_igr = old_igr_name[i]
                else:
                    temp_igr = temp_igr + d + old_igr_name[i]
        if temp_igr != "":
            temp_igr = temp_igr + " , "
        self.name[cur_idx].setText(menu_name[name_idx] + " , " + temp_igr +
                                   old_drk_name[drk_idx] + " , " + old_side_name[side_idx])

        if cur_idx == menu_idx:
            return self.W[cur_idx]
        else:
            return self.W[menu_idx]

    def delete_list(self, btn_num):
        cnt = int(basket[btn_num][0])

        if cnt == 1:
            self.W[btn_num].hide()
            basket[btn_num][0] == 0
        else:
            basket[btn_num][0] -= 1
            self.return_list(btn_num)

    def all_clear(self):
        global basket
        global menu_idx
        k = len(basket)
        for i in range(k):
            print(k)
            self.W[i].hide()
        basket = []
        menu_idx = 0
        old_bb.total_print()

# NOW - 현재 메뉴 출력


class now(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(now_UI, self)
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        self.cur_price.setFont(QFont('나눔스퀘어 bold', 40))

        self.now_go.clicked.connect(lambda: self.click_event(0))
        self.now_add.clicked.connect(lambda: self.click_event(1))

        global temp_order

        url = "../image/now/"
        set_url = [url + "set_0.PNG", url + "set_1.PNG", url + "set_2.PNG", url + "set_3.PNG", url + "set_4.PNG"
                    , url + "set_5.PNG", url + "set_6.PNG", url + "set_7.PNG", url + "set_8.PNG"]
        bg_url = [url + "bg0.PNG",url + "bg1.PNG", url + "bg2.PNG", url + "bg3.PNG", url + "bg4.PNG", url + "bg5.PNG", url + "bg6.PNG", url + "bg7.PNG", url + "bg8.PNG"]
        yg_side_url = [url + "fries_R.PNG", url + "fries_L.PNG", url + "chicken.PNG", url + "chz_fries.PNG",
                    url + "chz_stick.PNG", url + "szn_fries.PNG"]
        old_side_url = [url + "old_fries_R.PNG", url + "old_fries_L.PNG", url + "chicken.PNG", url + "chz_fries.PNG",
                        url + "chz_stick.PNG", url + "szn_fries.PNG"]
        yg_drk_url = [url + "cola_R.PNG", url + "cola_L.PNG", url + "soda_R.PNG", url + "soda_L.PNG",
                    url + "grp_juice.PNG", url + "org_juice.PNG"]
        old_drk_url = [url + "old_cola_R.PNG", url + "old_cola_L.PNG", url + "old_soda_R.PNG", url + "old_soda_L.PNG",
                    url + "grp_juice.PNG", url + "org_juice.PNG"]

        self.now_go.setStyleSheet("background-image:url(../image/now/keep.PNG); border :0px")
        self.now_add.setStyleSheet("background-image:url(../image/now/change.PNG); border :0px")

        cur_set = set_url[int(temp_order[1])]
        cur_bg = bg_url[int(temp_order[1])]
        if age_result == 0:  # old#
            cur_side = old_side_url[int(temp_order[3])]
            cur_drk = old_drk_url[int(temp_order[4])]
            self.cur_mn.setStyleSheet(
                "background-image:url(" + cur_set + "); border :0px")
            self.cur_bg.setStyleSheet(
                "background-image:url(" + cur_bg + "); border :0px")
            self.cur_side.setStyleSheet(
                "background-image:url(" + cur_side + "); border :0px")
            self.cur_drk.setStyleSheet(
                "background-image:url(" + cur_drk + "); border :0px")
        else:
            cur_side = yg_side_url[int(temp_order[3])]
            cur_drk = yg_drk_url[int(temp_order[4])]
            self.cur_mn.setStyleSheet(
                "background-image:url(" + cur_set + "); border :0px")
            self.cur_bg.setStyleSheet(
                "background-image:url(" + cur_bg + "); border :0px")
            self.cur_side.setStyleSheet(
                "background-image:url(" + cur_side + "); border :0px")
            self.cur_drk.setStyleSheet(
                "background-image:url(" + cur_drk + "); border :0px")

        self.cur_price.setText(str(Cal_now(temp_order))+" 원")

    def click_event(self, key):
        global age_result

        if key == 0:  # go basic
            if age_result == 0:
                main_window.Go_to_OldB()
            else:
                main_window.Go_to_B()
        else:  # go add
            main_window.N_to_A()

# BASIC - 기본구현


class menu_list(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(menu_list_UI, self)

        self.cancel_1.clicked.connect(lambda: self.delete_list(0))
        self.cancel_2.clicked.connect(lambda: self.delete_list(1))
        self.cancel_3.clicked.connect(lambda: self.delete_list(2))
        self.cancel_4.clicked.connect(lambda: self.delete_list(3))
        self.cancel_5.clicked.connect(lambda: self.delete_list(4))
        self.cancel_6.clicked.connect(lambda: self.delete_list(5))
        self.cancel_7.clicked.connect(lambda: self.delete_list(6))
        self.cancel_8.clicked.connect(lambda: self.delete_list(7))
        self.cancel_9.clicked.connect(lambda: self.delete_list(8))
        self.cancel_10.clicked.connect(lambda: self.delete_list(9))
        self.cancel_11.clicked.connect(lambda: self.delete_list(10))
        self.cancel_12.clicked.connect(lambda: self.delete_list(11))

        self.W = [self.w_1, self.w_2, self.w_3, self.w_4, self.w_5, self.w_6,
                  self.w_7, self.w_8, self.w_9, self.w_10, self.w_11, self.w_12]
        self.name = [self.name_1, self.name_2, self.name_3, self.name_4, self.name_5, self.name_6,
                     self.name_7, self.name_8, self.name_9, self.name_10, self.name_11, self.name_12]
        self.counts = [self.counts_1, self.counts_2, self.counts_3, self.counts_4, self.counts_5, self.counts_6,
                       self.counts_7, self.counts_8, self.counts_9, self.counts_10, self.counts_11, self.counts_12]
        self.price = [self.price_1, self.price_2, self.price_3, self.price_4, self.price_5,
                      self.price_6, self.price_7, self.price_8, self.price_9, self.price_10, self.price_11, self.price_12]

    def return_list(self, cur_idx):

        global basket
        global temp_order

        name_idx = int(basket[cur_idx][1])
        cnt = int(basket[cur_idx][0])
        side_idx = int(basket[cur_idx][3])
        drk_idx = int(basket[cur_idx][4])
        igr_list = basket[cur_idx][2]

        d = " +"
        temp_igr = ""
        self.W[cur_idx].show()
        str_igr = " , "

        self.price[cur_idx].setText(str(Cal_now(basket[cur_idx])) + "원")
        self.counts[cur_idx].setText(str(cnt))

        for i in range(6):
            if igr_list[i] >= 1:
                cnt = str(igr_list[i]) + " "
                if temp_igr == "":
                    temp_igr = "+" + cnt + igr_name[i]
                else:
                    temp_igr = temp_igr + " & " + cnt + igr_name[i]

        if temp_igr != "":
            str_igr = " , " + temp_igr + " , "

        self.name[cur_idx].setText(menu_name[name_idx] + str_igr +
                                   drk_name[drk_idx] + " , " + side_name[side_idx])
        print(temp_igr)
        return self.W[cur_idx]

    def delete_list(self, btn_num):
        cnt = int(basket[btn_num][0])

        if cnt == 1:
            self.W[btn_num].hide()
            basket[btn_num][0] = 0
        else:
            basket[btn_num][0] -= 1
            self.return_list(btn_num)

        print(basket)
        bb.total_print()

    def all_clear(self):
        global basket
        global menu_idx
        k = len(basket)
        for i in range(k):
            print(k)
            self.W[i].hide()
        basket = []
        menu_idx = 0
        bb.total_print()


class add(QWidget):
    # age_result == 1 의 click image 만들기.. 까먹지말자
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(add_UI, self)
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")

        # set stylesheet#
        if age_result == 0:
            #self.bgplz.setStyleSheet(
            #    "background-image:url(../image/main_bg.PNG)")
            self.add_X.setStyleSheet(
                "background-image:url(../image/add/old_no.PNG)")
            self.add_all.setStyleSheet(
                "background-image:url(../image/add/old_all_extra.PNG)")
            self.bacon_2.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.bacon_4.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.chz_1.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.chz_2.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.W_chz_1.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.W_chz_2.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.jala_2.setStyleSheet(
                "background-image:url(../image/add/2_jala.jpg)")
            self.jala_4.setStyleSheet(
                "background-image:url(../image/add/4_jala.jpg)")

            self.coke_R.setStyleSheet(
                "background-image:url(../image/add/old_cokeR.PNG)")
            self.coke_L.setStyleSheet(
                "background-image:url(../image/add/old_cokeL.PNG)")
            self.soda_R.setStyleSheet(
                "background-image:url(../image/add/old_sodaR.PNG)")
            self.soda_L.setStyleSheet(
                "background-image:url(../image/add/old_sodaL.PNG)")
            self.grape.setStyleSheet(
                "background-image:url(../image/add/grp_juice.PNG)")
            self.orange.setStyleSheet(
                "background-image:url(../image/add/org_juice.PNG)")

            self.fries_R.setStyleSheet(
                "background-image:url(../image/add/old_friesR.PNG)")
            self.fries_L.setStyleSheet(
                "background-image:url(../image/add/old_friesL.PNG)")
            self.chicken.setStyleSheet(
                "background-image:url(../image/add/chicken.PNG)")
            self.chz_fries.setStyleSheet(
                "background-image:url(../image/add/chz_fries.PNG)")
            self.chzstick.setStyleSheet(
                "background-image:url(../image/add/chz_stick.PNG)")
            self.szn_fries.setStyleSheet(
                "background-image:url(../image/add/szn_fries.PNG)")
            self.add_next.setStyleSheet(
                "background-image:url(../image/add/add_ok.PNG)")
        else:
            #self.bgplz.setStyleSheet(
            #    "background-image:url(../image/main_bg.PNG)")
            self.add_X.setStyleSheet(
                "background-image:url(../image/add/no.PNG)")
            self.add_all.setStyleSheet(
                "background-image:url(../image/add/all_extra.PNG)")
            self.bacon_2.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.bacon_4.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.chz_1.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.chz_2.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.W_chz_1.setStyleSheet(
                "background-image:url(../image/add/1sheet.jpg)")
            self.W_chz_2.setStyleSheet(
                "background-image:url(../image/add/2sheet.jpg)")
            self.jala_2.setStyleSheet(
                "background-image:url(../image/add/2_jala.jpg)")
            self.jala_4.setStyleSheet(
                "background-image:url(../image/add/4_jala.jpg)")

            self.coke_R.setStyleSheet(
                "background-image:url(../image/add/cokeR.PNG)")
            self.coke_L.setStyleSheet(
                "background-image:url(../image/add/cokeL.PNG)")
            self.soda_R.setStyleSheet(
                "background-image:url(../image/add/sodaR.PNG)")
            self.soda_L.setStyleSheet(
                "background-image:url(../image/add/sodaL.PNG)")
            self.grape.setStyleSheet(
                "background-image:url(../image/add/grp_juice.PNG)")
            self.orange.setStyleSheet(
                "background-image:url(../image/add/org_juice.PNG)")

            self.fries_R.setStyleSheet(
                "background-image:url(../image/add/friesR.PNG)")
            self.fries_L.setStyleSheet(
                "background-image:url(../image/add/friesL.PNG)")
            self.chicken.setStyleSheet(
                "background-image:url(../image/add/chicken.PNG)")
            self.chz_fries.setStyleSheet(
                "background-image:url(../image/add/chz_fries.PNG)")
            self.chzstick.setStyleSheet(
                "background-image:url(../image/add/chz_stick.PNG)")
            self.szn_fries.setStyleSheet(
                "background-image:url(../image/add/szn_fries.PNG)")

            # self.add_next.setStyleSheet(
            #     "background-image:url(../image/add/add_ok.PNG)")

        self.add_back.setStyleSheet("background-image:url(../image/add/back.PNG)")
        self.add_next.setStyleSheet("background-image:url(../image/add/order.PNG)")

        # Click event

        self.add_all.clicked.connect(lambda: self.click_event(0, 0))
        self.add_X.clicked.connect(lambda: self.click_event(0, 1))
        self.chz_1.clicked.connect(lambda: self.click_event(0, 2))  # 2
        self.chz_2.clicked.connect(lambda: self.click_event(0, 3))
        self.bacon_2.clicked.connect(lambda: self.click_event(0, 4))  # 3
        self.bacon_4.clicked.connect(lambda: self.click_event(0, 5))
        self.W_chz_1.clicked.connect(lambda: self.click_event(0, 6))  # 4
        self.W_chz_2.clicked.connect(lambda: self.click_event(0, 7))
        self.jala_2.clicked.connect(lambda: self.click_event(0, 8))
        self.jala_4.clicked.connect(lambda: self.click_event(0, 9))

        self.coke_R.clicked.connect(lambda: self.click_event(1, 0))
        self.coke_L.clicked.connect(lambda: self.click_event(1, 1))
        self.soda_R.clicked.connect(lambda: self.click_event(1, 2))
        self.soda_L.clicked.connect(lambda: self.click_event(1, 3))
        self.grape.clicked.connect(lambda: self.click_event(1, 4))
        self.orange.clicked.connect(lambda: self.click_event(1, 5))

        self.fries_R.clicked.connect(lambda: self.click_event(2, 0))
        self.fries_L.clicked.connect(lambda: self.click_event(2, 1))
        self.chicken.clicked.connect(lambda: self.click_event(2, 2))
        self.chz_fries.clicked.connect(lambda: self.click_event(2, 3))
        self.chzstick.clicked.connect(lambda: self.click_event(2, 4))
        self.szn_fries.clicked.connect(lambda: self.click_event(2, 5))

        self.add_next.clicked.connect(lambda: self.click_event(3, 0))

    def click_event(self, key, num):
        global status_ext
        global status_drk
        global status_side

        clk_url = "../image/add/clk/"
        no_clk_url = "../image/add/"

        age_url = ""
        if age_result == 0:  # old
            age_url = "old_"

        if key == 0:  # change extra

            check_x = False
            if status_ext[1] == 1:
                check_x = True

            check_db = False  # 다른메뉴 누르고 X 누르면 다 취소되도록.
            for i in range(10):
                if status_ext[i] == 1 and i != 1:
                    check_db = True
                    break

            if num == 1:
                if not check_x and not check_db:
                    status_ext[1] = 1
                    url = clk_url
                    self.add_X.setStyleSheet("background-image:url(" + url + age_url + "no.PNG)")
                if check_x:
                    status_ext[1] = 0
                    url = no_clk_url
                    self.add_X.setStyleSheet("background-image:url(" + url + age_url + "no.PNG)")
                if not check_x and check_db:
                    status_ext = [0] * 10
                    status_ext[1] = 1
                    url = clk_url
                    self.add_X.setStyleSheet("background-image:url(" + url + age_url + "no.PNG)")

            if num != 1 and not check_x:
                if status_ext[num] == 0:
                    status_ext[num] = 1
                else:
                    status_ext[num] = 0

                if num == 0:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.add_all.setStyleSheet("background-image:url(" + url + age_url + "all_extra.PNG)")
                    else:
                        url = clk_url
                        self.add_all.setStyleSheet("background-image:url(" + url + age_url + "all_extra.PNG)")
                elif num == 2:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.chz_1.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")
                    else:
                        url = clk_url
                        self.chz_1.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")
                elif num == 3:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.chz_2.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")
                    else:
                        url = clk_url
                        self.chz_2.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")
                elif num == 4:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.bacon_2.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")
                    else:
                        url = clk_url
                        self.bacon_2.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")

                elif num == 5:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.bacon_4.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")
                    else:
                        url = clk_url
                        self.bacon_4.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")

                elif num == 6:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.W_chz_1.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")
                    else:
                        url = clk_url
                        self.W_chz_1.setStyleSheet("background-image:url(" + url + "1sheet.jpg)")
                elif num == 7:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.W_chz_2.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")
                    else:
                        url = clk_url
                        self.W_chz_2.setStyleSheet("background-image:url(" + url + "2sheet.jpg)")
                elif num == 8:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.jala_2.setStyleSheet("background-image:url(" + url + "2_jala.jpg)")
                    else:
                        url = clk_url
                        self.jala_2.setStyleSheet("background-image:url(" + url + "2_jala.jpg)")
                elif num == 9:
                    if status_ext[num] == 0:
                        url = no_clk_url
                        self.jala_4.setStyleSheet("background-image:url(" + url + "4_jala.jpg)")
                    else:
                        url = clk_url
                        self.jala_4.setStyleSheet("background-image:url(" + url + "4_jala.jpg)")

        elif key == 1:  # change drk

            checked_index = 99
            double_checked = False

            for i in range(6):
                if status_drk[i] == 1:
                    checked_index = i
                    double_checked = True

            if num == checked_index or not double_checked:
                if status_drk[num] == 0:
                    status_drk[num] = 1
                else:
                    status_drk[num] = 0

                if num == 0:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.coke_R.setStyleSheet("background-image:url(" + url + age_url + "cokeR.PNG)")
                    else:
                        url = clk_url
                        self.coke_R.setStyleSheet("background-image:url(" + url + age_url + "cokeR.PNG)")
                elif num == 1:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.coke_L.setStyleSheet("background-image:url(" + url + age_url + "cokeL.PNG)")
                    else:
                        url = clk_url
                        self.coke_L.setStyleSheet("background-image:url(" + url + age_url + "cokeL.PNG)")
                elif num == 2:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.soda_R.setStyleSheet("background-image:url(" + url + age_url + "sodaR.PNG)")
                    else:
                        url = clk_url
                        self.soda_R.setStyleSheet("background-image:url(" + url + age_url + "sodaR.PNG)")
                elif num == 3:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.soda_L.setStyleSheet("background-image:url(" + url + age_url + "sodaL.PNG)")
                    else:
                        url = clk_url
                        self.soda_L.setStyleSheet("background-image:url(" + url + age_url + "sodaL.PNG)")
                elif num == 4:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.grape.setStyleSheet("background-image:url(" + url + "grp_juice.PNG)")
                    else:
                        url = clk_url
                        self.grape.setStyleSheet("background-image:url(" + url + "grp_juice.PNG)")
                elif num == 5:
                    if status_drk[num] == 0:
                        url = no_clk_url
                        self.orange.setStyleSheet("background-image:url(" + url + "org_juice.PNG)")
                    else:
                        url = clk_url
                        self.orange.setStyleSheet("background-image:url(" + url + "org_juice.PNG)")

        elif key == 2:  # change side

            checked_index = 99
            double_checked = False

            for i in range(6):
                if status_side[i] == 1:
                    checked_index = i
                    double_checked = True

            if num == checked_index or not double_checked:

                if status_side[num] == 0:
                    status_side[num] = 1
                else:
                    status_side[num] = 0

                if num == 0:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.fries_R.setStyleSheet("background-image:url(" + url + age_url + "friesR.PNG)")
                    else:
                        url = clk_url
                        self.fries_R.setStyleSheet("background-image:url(" + url + age_url + "friesR.PNG)")
                elif num == 1:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.fries_L.setStyleSheet("background-image:url(" + url + age_url + "friesL.PNG)")
                    else:
                        url = clk_url
                        self.fries_L.setStyleSheet("background-image:url(" + url + age_url + "friesL.PNG)")
                elif num == 2:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.chicken.setStyleSheet("background-image:url(" + url + "chicken.PNG)")
                    else:
                        url = clk_url
                        self.chicken.setStyleSheet("background-image:url(" + url + "chicken.PNG)")
                elif num == 3:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.chz_fries.setStyleSheet("background-image:url(" + url + "chz_fries.PNG)")
                    else:
                        url = clk_url
                        self.chz_fries.setStyleSheet("background-image:url(" + url + "chz_fries.PNG)")
                elif num == 4:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.chzstick.setStyleSheet("background-image:url(" + url + "chz_stick.PNG)")
                    else:
                        url = clk_url
                        self.chzstick.setStyleSheet("background-image:url(" + url + "chz_stick.PNG)")
                elif num == 5:
                    if status_side[num] == 0:
                        url = no_clk_url
                        self.szn_fries.setStyleSheet("background-image:url(" + url + "szn_fries.PNG)")
                    else:
                        url = clk_url
                        self.szn_fries.setStyleSheet("background-image:url(" + url + "szn_fries.PNG)")

        else:  # go next

            for i in range(10):
                if status_ext[i] == 1:
                    change_igr(i)
            for j in range(6):
                if status_drk[j] == 1:
                    change_drk(j)
                if status_side[j] == 1:
                    change_side(j)

            status_ext = [0] * 10
            status_drk = [0] * 6
            status_side = [0] * 6

            if age_result == 0:
                main_window.Go_to_OldB()
            else:
                main_window.Go_to_B()


class basic(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(basic_UI, self)
        # 스크롤
        QScroller.grabGesture(self.scroll_event.viewport(),
                              QScroller.LeftMouseButtonGesture)
        QScroller.grabGesture(self.scroll_burger.viewport(),
                              QScroller.LeftMouseButtonGesture)
        QScroller.grabGesture(self.scroll_side.viewport(),
                              QScroller.LeftMouseButtonGesture)
        QScroller.grabGesture(self.scroll_drink.viewport(),
                              QScroller.LeftMouseButtonGesture)
        QScroller.grabGesture(self.scroll_basket.viewport(),
                              QScroller.LeftMouseButtonGesture)


        #결제창으로 보내기
        self.nextbtn.clicked.connect(lambda: p.refresh(
            now_member, age_result, basket, total_cost))

        # 메뉴
        self.gui_setting()
        # 버튼
        # self.all_cancel.clicked.connect()

    def gui_setting(self):
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.menu_00.setStyleSheet("background-image:url(../image/basic/0.png); border :0px")
        self.menu_01.setStyleSheet("background-image:url(../image/basic/1.png); border :0px")
        self.menu_02.setStyleSheet("background-image:url(../image/basic/2.png); border :0px")
        self.menu_03.setStyleSheet("background-image:url(../image/basic/3.png); border :0px")
        self.menu_04.setStyleSheet("background-image:url(../image/basic/4.png); border :0px")
        self.menu_05.setStyleSheet("background-image:url(../image/basic/5.png); border :0px")
        self.menu_06.setStyleSheet("background-image:url(../image/basic/6.png); border :0px")
        self.menu_07.setStyleSheet("background-image:url(../image/basic/7.png); border :0px")
        self.menu_08.setStyleSheet("background-image:url(../image/basic/8.png); border :0px")

        self.menu_00.clicked.connect(lambda: self.click_event(0))
        self.menu_01.clicked.connect(lambda: self.click_event(1))
        self.menu_02.clicked.connect(lambda: self.click_event(2))
        self.menu_03.clicked.connect(lambda: self.click_event(3))
        self.menu_04.clicked.connect(lambda: self.click_event(4))
        self.menu_05.clicked.connect(lambda: self.click_event(5))
        self.menu_06.clicked.connect(lambda: self.click_event(6))
        self.menu_07.clicked.connect(lambda: self.click_event(7))
        self.menu_08.clicked.connect(lambda: self.click_event(8))

        self.Button_set.clicked.connect(lambda: self.menu(num=1))
        self.Button_burger.clicked.connect(lambda: self.menu(num=2))
        self.Button_side.clicked.connect(lambda: self.menu(num=3))
        self.Button_drink.clicked.connect(lambda: self.menu(num=4))

        self.all_cancel.clicked.connect(lambda: mn.all_clear())
        self.nextbtn.clicked.connect(self.ppp)

    def ppp(self):
        p.refresh(now_member, age_result, basket, total_cost)

    def menu(self, num):
        self.basic_Widget.setCurrentIndex(num)

    def click_event(self, num):
        create_order(num)
        main_window.B_to_N()

    def insert_basket(self):
        match = False
        global temp_order
        global menu_idx
        igr_match = 0
        match_index = 100

        if len(basket) == 0:
            basket.append(temp_order)
            self.Layout_basket.addWidget(mn.return_list(menu_idx))
            next_idx()
        else:
            for i in range(len(basket)):
                if basket[i][1] == temp_order[1] and basket[i][3] == temp_order[3] and basket[i][4] == temp_order[4]:
                    for k in range(6):
                        if basket[i][2][k] == temp_order[2][k]:
                            igr_match += 1
                    if igr_match == 6:
                        match = True
                        basket[i][0] += 1
                        match_index = i
                        break

            if match:
                mn.return_list(match_index)
            else:
                basket.append(temp_order)
                self.Layout_basket.addWidget(mn.return_list(menu_idx))
                next_idx()

        self.total_print()

    def total_print(self):
        self.all_price.setText(
            '총 주문금액  :  ' + str(Cal_total_price()) + '원')
        self.all_count.setText(
            '총 주문수량  :  ' + str(Cal_total_counts()) + '개')


# main 이랑 다른화면으로 넘어가는 함수 있음
class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(kiosk_UI, self)
        self.plz_bg.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg.lower()
        self.plz_bg_2.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.plz_bg_2.lower()
        #self.background.setStyleSheet("background-image:url(../image/main_bg.PNG)")
        self.Button_main_order.setStyleSheet("background-image:url(../image/main_window/basic_order.PNG)")
        self.Button_dg_register.setStyleSheet("background-image:url(../image/main_window/dg_register.PNG)")
        self.Button_dg_order.setStyleSheet("background-image:url(../image/main_window/dg_order.PNG)")
        # 첫화면
        self.btn_store.setStyleSheet("background-image:url(../image/main_window/forhere.PNG)")
        self.btn_takeout.setStyleSheet("background-image:url(../image/main_window/togo.PNG)")

        self.Button_main_order.clicked.connect(lambda: self.main_order())

        # 매장 or 포장

        self.stackedWidget.insertWidget(2, basic())
        bb.Button_back.clicked.connect(lambda: self.back())
        bb.Button_home.clicked.connect(lambda: self.home())
        old_bb.Button_back.clicked.connect(lambda: self.back())
        old_bb.Button_home.clicked.connect(lambda: self.home())

        self.btn_store.clicked.connect(lambda: self.match_age())
        self.btn_store.clicked.connect(oo.refresh)
        self.btn_takeout.clicked.connect(lambda: self.match_age())
        self.btn_takeout.clicked.connect(oo.refresh)

        # 단골 확인 및 주문
        self.Button_dg_order.clicked.connect(self.todangol)

        d_checker.btn_dg_yes.clicked.connect(self.ref)
        d_checker.btn_dg_basic.clicked.connect(self.match_age)
        dangol_check.rr.skip_btn2.clicked.connect(self.match_age)

        d_Order.btn_dg_most.clicked.connect(
            lambda: self.d_to_b(d_Order.most()))
        d_Order.btn_dg_basic.clicked.connect(self.match_age)
        d_Order.btn_dg_last_1.clicked.connect(
            lambda: self.d_to_b(d_Order.last1_f()))
        d_Order.btn_dg_last_2.clicked.connect(
            lambda: self.d_to_b(d_Order.last2_f()))
        d_Order.btn_dg_last_3.clicked.connect(
            lambda: self.d_to_b(d_Order.last3_f()))

        p.card_btn.clicked.connect(self.end)

        #단골 등록
        self.Button_dg_register.clicked.connect(self.dg_reg)
        d_register.dg_register.clicked.connect(self.dg_ok)
        d_register.dg_back.clicked.connect(self.match_age)

        self.storesubmit.clicked.connect(self.storeSubmit)
        self.warn.hide()

    #단골 등록
    def dg_reg(self):
        d_register.running = True
        th = threading.Thread(target=d_register.run)
        th.start()
        d_register.show()
        self.stackedWidget.insertWidget(3,d_register)
        self.stackedWidget.setCurrentIndex(3)

    def dg_ok(self):
        global now_member
        now_member = d_register.member_register()
        self.stackedWidget.removeWidget(d_register)
        global age_result
        age_result = member_dict[now_member].age
        if age_result == 0:
            self.stackedWidget.insertWidget(3, oo)
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.Set_B()       
    
    def end(self):
        global now_member
        now_member = ""
        mn.all_clear()
        old_mn.all_clear()
        self.stackedWidget.setCurrentIndex(0)

    def todangol(self):
        d_checker.faceCheck()
        d_checker.refresh()
        self.stackedWidget.insertWidget(3, d_checker)
        self.stackedWidget.setCurrentIndex(3)

    def ref(self):
        global now_member
        now_member = d_checker.yes()
        d_Order.refresh(now_member)
        self.stackedWidget.insertWidget(4, d_Order)
        self.stackedWidget.setCurrentIndex(4)

    def d_to_b(self, i):
        global age_result, temp_order
        temp_order = i
        age_result = member_dict[now_member].age
        self.stackedWidget.removeWidget(d_checker)
        self.stackedWidget.removeWidget(d_Order)
        if age_result == 0:
            old_bb.insert_basket()
            old_cur.insert_basket()
            self.Go_to_OldB()
            self.stackedWidget.insertWidget(3, oo)
            self.stackedWidget.setCurrentIndex(4)
        else:
            #bb.insert_basket()
            self.Go_to_B()
            self.Set_B()

    # 기본 레이아웃

    def main_order(self):
        global now_member
        now_member = ""
        self.stackedWidget.setCurrentIndex(1)

    def match_age(self):
        global age_result
        age_check()
        self.stackedWidget.removeWidget(d_checker)
        self.stackedWidget.removeWidget(d_Order)
        if age_result == 0:
            self.stackedWidget.insertWidget(3, oo)
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.Set_B()

    def B_to_N(self):
        self.stackedWidget.insertWidget(3, now())
        self.stackedWidget.setCurrentIndex(3)

    def N_to_A(self):
        self.stackedWidget.insertWidget(4, add())
        self.stackedWidget.setCurrentIndex(4)

    def Go_to_B(self):
        self.stackedWidget.insertWidget(2, bb)
        self.stackedWidget.setCurrentIndex(2)
        bb.insert_basket()

    def Go_to_OldB(self):
        self.stackedWidget.insertWidget(5, old_bb)
        self.stackedWidget.setCurrentIndex(5)
        old_bb.insert_basket()

    def back(self):
        self.stackedWidget.setCurrentIndex(1)

    def home(self):
        self.stackedWidget.setCurrentIndex(0)

    def Set_B(self):
        self.stackedWidget.setCurrentIndex(2)

    def Set_OldB(self):
        self.stackedWidget.insertWidget(2, old_bb)
        self.stackedWidget.setCurrentIndex(2)

    def storeSubmit(self):
        pay.STOREKEY = self.storekey.toPlainText()
        pay.STORENAME = self.storecode.toPlainText()
        if dangol.check(pay.STORENAME, pay.STOREKEY):
            self.Store.hide()
        else:
            self.warn.show()


load()
oo = old()

mn = menu_list()
old_mn = old_menu_list()
bb = basic()
old_bb = old_basic()

d_Order = dangol_order.dangol_order()
d_checker = dangol_check.checker()
p = pay.payment()

d_register = dangol_register.register()


main_window = Main()
main_window.showMaximized()
app.exec_()  # 이벤트루프로 진입시켜줌(무한루프)