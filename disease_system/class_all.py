import re

import mysql.connector
import json
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="chtdtttbtl"
)


class ConvertData:
    """
    Truy vấn và xử lý dữ liệu
    """
    def __init__(self):
        self.resultbenh = []
        self.resulttrieutrung = []
        self.resultfc = []
        self.resultbc = []
        self.resulttt = []

    def convertbenh(self):
        """
        Lấy dữ liệu bảng bệnh
        dữ liệu dạng: self.resultbenh = [{'idbenh': 'S01', 'tenbenh' : 'dau bung', 'nguyennhan' : '...', 'loikhuyen' : '...'}]
        """
        dbbenh = mydb.cursor()
        dbbenh.execute("SELECT * FROM chtdtttbtl.benh;")
        benh = dbbenh.fetchall()
        dirbenh = {}
        for i in benh:
            dirbenh['idbenh'] = i[0]
            dirbenh['tenBenh'] = i[1]
            dirbenh["nguyennhan"] = i[2]
            dirbenh['loikhuyen'] = i[3]
            self.resultbenh.append(dirbenh)
            dirbenh = {}

    def converttrieuchung(self):
        """
        Lấy dữ liệu từ bảng trieuchung
        dữ liệu dạng: self.resulttrieutrung = [{'idtrieuchung' : '...', 'noidung' : '...'}]
        """
        dbtrieuchung = mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chtdtttbtl.trieuchung;")
        trieuchung = dbtrieuchung.fetchall()
        dirtrieuchung = {}
        # resulttrieuchung=[]
        for i in trieuchung:
            dirtrieuchung['idtrieuchung'] = i[0]
            dirtrieuchung['noidung'] = i[1]
            self.resulttrieutrung.append(dirtrieuchung)
            dirtrieuchung = {}

    def getfc(self):
        """
        Nhóm các bệnh cùng 1 triệu chứng
        trạng thái 1 là luật suy diễn tiến
        dữ liệu dạng: self.resultfc = [{'trieuchung' : '...', 'benh' : [...]}]
        """
        dbfc = mydb.cursor()
        dbfc.execute(
            "select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1'")
        fc = dbfc.fetchall()
        s = []  # list triệu chứng 
        d = []  # list bệnh 
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        # print(s)
        # print(d)

        tt = s[0]   # chọn triệu chứng đầu tiên để nhóm các bệnh cùng một triệu chứng
        # print(tt)
        benh = []
        dicfc = {}
        for i in range(len(s)):
            if s[i] == tt:
                benh.append(d[i])
            else:
                dicfc['trieuchung'] = tt
                dicfc['benh'] = benh
                tt = s[i]
                self.resultfc.append(dicfc)
                benh = []
                benh.append(d[i])
                dicfc = {}
        # print(benh)
        # print()

    def getbc(self):
        """
        Nhóm các triệu chứng cùng 1 bệnh
        trạng thái 0 là luật suy diễn lùi 
        dữ liệu dạng: self.resultbc = [{'rule' : '...', 'benh' : '...', 'trieuchung' : [...]}]
        """
        dbbc = mydb.cursor()
        dbbc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='0' order by idbenh")
        fc = dbbc.fetchall()
        rule = []
        s = []
        d = []
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        # print(rule)
        vtrule = rule[0]
        tt = []
        benh = None
        # result=[]
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tt.append(s[i])
                benh = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['benh'] = benh
                dicbc['trieuchung'] = tt
                vtrule = rule[i]
                self.resultbc.append(dicbc)
                benh = d[i]
                tt = []
                tt.append(s[i])
                dicbc = {}
        # print(dicbc)

    def groupbc(self):
        """
        dữ liệu dạng: self.resultbc = [{'rule' : '...', 'benh' : '...', 'trieuchung' : [...]}]
        """
        p = []
        vt = self.resultbc[0]['benh']
        temp = []
        for i in self.resultbc:
            t = []
            t.append(i['benh'])
            for j in i['trieuchung']:
                t.append(j)
            temp.append(t)
        return temp

    def groupfc(self):
        res = []
        for i in self.resultfc:
            for j in range(len(i['benh'])):
                res.append([i['benh'][j], i['trieuchung']])
        return res

    def gettrieuchung(self):
        """
        Nhóm tất cả triệu chứng trong 1 bệnh
        dữ liệu đầu ra dạng: {'D1' : ['S01', 'S02], 'D2' : [...], 'D3' : [...], 'D4' : [...], 'D5' : [...], 'D6' : [...]}
        """
        dbtrieuchung=mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chtdtttbtl.suydien order by idbenh")
        dttt=dbtrieuchung.fetchall()
        benh=[] # list chứa bệnh được sắp xếp từ D1 đến D6
        tt=[]   # list chứa triệu chứng
        rule=[] # luật 
        for i in dttt:
            benh.append(i[3])
            tt.append(i[2])
            rule.append(i[1])

        vtbenh=benh[0]
        lstt=[]     # chứa triệu chứng của bệnh đang xét 
        dirtt={}    # dữ liệu dạng: dirtt = {'D1' : ['S01', 'S02], 'D2' : [...], 'D3' : [...], 'D4' : [...], 'D5' : [...], 'D6' : [...]}
        
        for i in range(len(benh)):
            if benh[i]==vtbenh:
                lstt.append(tt[i])
            else:
                dirtt[vtbenh]=sorted(set(lstt))
                lstt=[]
                vtbenh=benh[i]
                lstt.append(tt[i])
        dirtt[vtbenh]=sorted(set(lstt))
        self.resulttt=dirtt

        return self.resulttt
    
    def get_benh_by_id(self, id_benh):
        """
        Tìm bệnh dựa trên id
        """
        for i in self.resultbenh:
            if i["idbenh"] == id_benh:
                return i
        return 0

    def get_trieuchung_by_id(self, id_trieuchung):
        '''
        Tìm triệu chứng dựa trên id 
        '''
        for i in self.resulttrieutrung:
            if i["idtrieuchung"] == id_trieuchung:
                return i
        return 0

    

class Validate:
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self, count):
        while (1):
            value = input(f"--> Bạn : Câu trả lời của tôi là: ")
            value2 = []
            if "," in value:
                value2 = value.split(",")
            elif "-" in value:
                value2 = value.split("-")
            elif " " in value:
                value2 = value.split(" ")
                while "" in value2:
                    value2.remove("")
            else: 
                value2.append(value)

            value_list = [s.strip() for s in value2]

            contains_non_digit = any(any(not char.isdigit() for char in s) for s in value_list)

            if contains_non_digit:
                print("--> Hệ thống : Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời.")
            else:
                answer_list = [int(x) for x in value_list]
                unique_list = [x for x in answer_list if answer_list.count(x) == 1]
                if count < max(answer_list) or min(answer_list) < 0:
                    print("--> Hệ thống : Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời.")
                elif 0 in answer_list and len(answer_list) > 1:
                    print("--> Hệ thống : Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời.")
                elif len(unique_list) != len(answer_list):
                    print("--> Hệ thống : Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời.")
                else:
                    return answer_list

    def validate_input_number_form_2(self, value, limit):
        check = value.isnumeric()
        if (check and int(value)>=0 and int(value)<=limit):
            return value
        else:
            print("-->Hệ thống: Vui lòng nhập 1 số từ 0 tới ", end="")
            print(limit)
            value = input()

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->hệ thống: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()



class TreeForFC(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Symptom:
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 10 * level + '-> ' + str(node.value))
        printTree(node.right, level + 1)
        

def searchindexrule(rule,goal):
    """
    Tìm vị trí các rule có bệnh là goal
    """
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
def get_s_in_d(answer,goal,rule,d,flag):
    """
    Lấy các triệu chứng theo sự suy diễn để giảm thiểu câu hỏi
    và  đánh dấu các luật đã được duyệt qua để bỏ qua những luật có cùng cùng câu hỏi vào
    """
    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)        

    return sorted(set(result)),index



