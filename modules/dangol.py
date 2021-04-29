import requests
from requests.auth import HTTPBasicAuth
import json

class member:
    def __init__(self,name,age,number):
        self.name=name
        self.age=age
        self.number=number
        self.order=[]
        self.point=0
        self.prefer=dict()
        
    def recent(self): # 최근 주문 목록 (3개)
        return len(self.order[-3:]), list(reversed(self.order[-3:]))
    
    def preference(self,): # 가장 많이 주문한 메뉴(사이드 조건 포함)
        res=sorted(self.prefer,key=lambda x: self.prefer[x],reverse=True)
        return res[-1]

    def add_order(self,basket, price):
        self.order+=basket
        for num, menu, side_list, side, drink in basket:
            if (menu, tuple(side_list), side, drink) in self.prefer:
                self.prefer[(menu, tuple(side_list), side, drink)]+=num
            else:
                self.prefer[(menu, tuple(side_list), side, drink)]=num
        self.point+=price//100 # 예를 들어 1%의 포인트 적립

def getMenusByAge(name, key, age):
    agedict = dict()
    agedict[0] = "young"
    agedict[1] = "middle"
    agedict[2] = "old"
    res = requests.get('http://127.0.0.1:80/api/menu/favorite/age/' + str(agedict[age]), auth=HTTPBasicAuth(name, key))
    return res.text

def addOrderForAge(basket, age, name, key):
    agedict = dict()
    agedict[0] = "young"
    agedict[1] = "middle"
    agedict[2] = "old"
    order = [ menu+1 for num, menu, side_list, side, drink in basket ]
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    data = {'order': order, 'age': agedict[age]}
    res = requests.post('http://127.0.0.1:80/order/insert', data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(name, key))

member_dict=dict()

def write(now_member, age_result, price, number, basket):
    f = open("../data/data.txt", 'a')
    f.write(now_member + "," + str(age_result) + ',' +str(price) +',' +str(number)+"\n")
    for num, menu, side_list, side, drink in basket:
        f.write(str(num) + "," + str(menu) + "," + ",".join([str(i) for i in side_list]) + "," + str(side) + "," + str(drink) + "\n")
    f.write("\n")
    f.close()

def load():
    f = open("../data/data.txt", 'r')
    while f.readable():
        line = f.readline()
        if line=="" or line=="\n":
            break
        s= list(line.split(","))
        if s[0]!="." and not s[0] in member_dict:
            member_dict[s[0]] = member(s[0],int(s[1]),s[3])

        bas=[]
        line = f.readline()
        while line!="\n" and line!="":
            ss = [int(i) for i in line.split(",")]
            bas.append([ss[0],ss[1],[ss[2],ss[3],ss[4],ss[5],ss[6],ss[7]],ss[8],ss[9]])
            if not f.readable():
                break
            line = f.readline()
        if s[0]!=".":
            member_dict[s[0]].add_order(bas,int(s[2]))
    f.close()