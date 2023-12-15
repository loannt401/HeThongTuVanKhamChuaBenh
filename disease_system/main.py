import os
import sys

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from class_all import *
from class_all import ConvertData



# biến khởi tạo
validate = Validate()
list_symptom_of_person = []  # list các triệu chứng người dùng khi trả lời là yes

db = ConvertData()
'''
dữ liệu trong db:
    self.resultbenh = [{'idbenh': 'S01', 'tenbenh' : 'dau bung', 'nguyennhan' : '...', 'loikhuyen' : '...'}]
    self.resulttrieutrung = [{'idtrieuchung' : '...', 'noidung' : '...'}]
    self.resultfc = [{'trieuchung' : '...', 'benh' : [...]}]
    self.resultbc = [{'rule' : '...', 'benh' : '...', 'trieuchung' : [...]}]
    self.resulttt = {'D1' : ['S01', 'S02], 'D2' : [...], 'D3' : [...], 'D4' : [...], 'D5' : [...], 'D6' : [...]}

'''
db.convertbenh()  # bang benh
db.converttrieuchung()  # bang trieu chung
db.getfc()
db.getbc()

# print(db.gettrieuchung())
#nho
luat_lui = db.groupbc()
luat_tien = db.groupfc()




#################################################
# 1. câu hỏi chào hỏi
def welcome_question():
    print("-->Xin chào, đây là hệ thống hỗ trợ chẩn đoán và chữa trị bệnh tiêu hóa. Nếu bạn có vấn đề về tiêu hóa, tôi sẽ giúp bạn!")
    print("-->Để nhận lời khuyên và chuẩn đoán chi tiết, vui lòng trả lời một số câu hỏi sau.")
    return 



#################################################################
# 2. 1 số câu hỏi đầu tiên
def first_question(list_symptom_of_person):
    AllSymLst = [db.resulttrieutrung[0], db.resulttrieutrung[12],
                 db.resulttrieutrung[29], db.resulttrieutrung[34]]

    while (1):
        if (len(list_symptom_of_person) == 4):
            break
        if (len(list_symptom_of_person) == 0):
            print(f'-->Hệ thống: Bạn có triệu trứng nào ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
        else:
            print(f'-->Hệ thống: Bạn có triệu trứng nào nữa ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều 1, 2, ... )')

        # Loại bỏ mỗi triệu chứng được chọn sau mỗi câu hỏi
        count = 1
        for i in AllSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]} \n')
            count += 1

        print("0. Tôi không có triệu chứng nào ở trên\n---------------------Câu trả lời của bạn---------------------")

        # print(f'-->Bạn: Câu trả lời của tôi là: ')

        answer = validate.validate_input_number_form(len(AllSymLst))
        if 0 in answer: 
            print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
            print([i['idtrieuchung'] for i in list_symptom_of_person])
            break
        for i in answer:
            list_symptom_of_person.append(AllSymLst[i-1])

        # loại bỏ triệu chứng đã chọn trong AllSymLst 
        stt_trieuchung = []
        for i in range(len(AllSymLst)):
            if i+1 not in answer:
                stt_trieuchung.append(i)
        NewAllSymLst = []
        for i in stt_trieuchung:
            NewAllSymLst.append(AllSymLst[i])
        AllSymLst = NewAllSymLst
        
        # if (answer == '0'):
        #     break
        # else:
        #     list_symptom_of_person.append(AllSymLst[int(answer)-1])

        print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
        print([i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person



#############################################################
# 3. Câu hỏi thứ 2 ( về vị trí)
def second_question(list_symptom_of_person):
    
    Location_StomachAcheSymLst = [db.resulttrieutrung[5], db.resulttrieutrung[6]]
    # print('Location_StomachAcheSymLst: ', Location_StomachAcheSymLst)
    check = {'idtrieuchung': 'S01', 'noidung': 'Đau bụng'}
    if (check in list_symptom_of_person):
        print(f'-->Hệ thống: Bạn đang có triệu chứng ĐAU BỤNG.\n Để có chuẩn đoán chính xác, hãy cho tôi biết chi tiết thêm về vị trí đau')

        count = 1
        for i in Location_StomachAcheSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]}')
            count += 1
        print('0. Bỏ qua')
        print('---------------------Câu trả lời của bạn---------------------')
        answer = validate.validate_input_number_form_2(input(), len(Location_StomachAcheSymLst))
        print(f'-->Bạn: Câu trả lời của tôi là {answer}')

        if (answer != '0'):
            list_symptom_of_person.append(
                Location_StomachAcheSymLst[int(answer)-1])
            print(
                f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', [i['idtrieuchung'] for i in list_symptom_of_person])

    # print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:',
    #       [i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person




########################################################
# 4. Câu hỏi thứ 3 về tần suất đau
def third_question(list_symptom_of_person):
    Frequency_StomachAcheSymLst = [
        db.resulttrieutrung[7],
        db.resulttrieutrung[8],
        db.resulttrieutrung[9],
        db.resulttrieutrung[10],
        db.resulttrieutrung[11],
    ]
    old = len(list_symptom_of_person)
    while (1):
        check = {'idtrieuchung': 'S01', 'noidung': 'Đau bụng'}
        if (check in list_symptom_of_person):
            if old == len(list_symptom_of_person):
                print(
                f'-->Hệ thống: Tiếp theo tôi muốn biết bạn thường đau bụng lúc nào và kéo dài bao lâu. (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            else:
                print(f'-->Hệ thống: Bạn còn triệu chứng nào dưới đây không? (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            
            count = 1
            for i in Frequency_StomachAcheSymLst:
                if (i not in list_symptom_of_person):
                    print(f'{count}. {i["noidung"]}')
                count += 1
            print('0. Bỏ qua')
            print('---------------------Câu trả lời của bạn---------------------')
            answer = validate.validate_input_number_form(len(Frequency_StomachAcheSymLst))
            if 0 in answer: 
                print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
                print([i['idtrieuchung'] for i in list_symptom_of_person])
                break
            for i in answer:
                list_symptom_of_person.append(Frequency_StomachAcheSymLst[i-1])

            # loại bỏ triệu chứng đã chọn trong AllSymLst 
            stt_trieuchung = []
            for i in range(len(Frequency_StomachAcheSymLst)):
                if i+1 not in answer:
                    stt_trieuchung.append(i)
            NewFrequency_StomachAcheSymLst = []
            for i in stt_trieuchung:
                NewFrequency_StomachAcheSymLst.append(Frequency_StomachAcheSymLst[i])
            Frequency_StomachAcheSymLst = NewFrequency_StomachAcheSymLst
            

            print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
            print([i['idtrieuchung'] for i in list_symptom_of_person])

        else:
            break
    return list_symptom_of_person

########################################################
# 5. Câu hỏi thêm về kiểu đau bụng
def extra_question(list_symptom_of_person):
    Type_StomachAcheSymLst = [
        db.resulttrieutrung[1],
        db.resulttrieutrung[2],
        db.resulttrieutrung[3],
        db.resulttrieutrung[4],
        
    ]
    old = len(list_symptom_of_person)
    while (1):
        check = {'idtrieuchung': 'S01', 'noidung': 'Đau bụng'}
        if (check in list_symptom_of_person):
            if old == len(list_symptom_of_person):
                print(f'-->Hệ thống: Bạn thường đau bụng như thế nào? (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            else:
                print(f'-->Hệ thống: Bạn còn triệu chứng nào dưới đây không? (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            count = 1
            for i in Type_StomachAcheSymLst:
                if (i not in list_symptom_of_person):
                    print(f'{count}. {i["noidung"]}')
                count += 1
            print('0. Bỏ qua')
            print('---------------------Câu trả lời của bạn---------------------')

            answer = validate.validate_input_number_form(len(Type_StomachAcheSymLst))
            if 0 in answer: 
                print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
                print([i['idtrieuchung'] for i in list_symptom_of_person])
                break
            for i in answer:
                list_symptom_of_person.append(Type_StomachAcheSymLst[i-1])

            # loại bỏ triệu chứng đã chọn trong AllSymLst 
            stt_trieuchung = []
            for i in range(len(Type_StomachAcheSymLst)):
                if i+1 not in answer:
                    stt_trieuchung.append(i)
            NewAllSymLst = []
            for i in stt_trieuchung:
                NewAllSymLst.append(Type_StomachAcheSymLst[i])
            Type_StomachAcheSymLst = NewAllSymLst

            print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
            print([i['idtrieuchung'] for i in list_symptom_of_person])
        else:
            break
    return list_symptom_of_person


########################################################
# 6. Câu hỏi thêm về buồn nôn
def nausea_question(list_symptom_of_person):
    nauseaSymLst = [
        db.resulttrieutrung[13],
        db.resulttrieutrung[14],
        db.resulttrieutrung[15],
        db.resulttrieutrung[16],
        db.resulttrieutrung[17],
    ]
    old = len(list_symptom_of_person)
    while (1):
        check = {'idtrieuchung': 'S13', 'noidung': 'Buồn nôn, nôn mửa'}
        if (check in list_symptom_of_person):
            if old == len(list_symptom_of_person):
                print(f'-->Hệ thống: Chúng tôi thấy rằng bạn có triệu chứng buồn nôn. Hãy cho biết chi tiết thêm. (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            else:
                print(f'-->Hệ thống: Bạn còn triệu chứng nào dưới đây không? (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều: 1, 2, ... )')
            
            count = 1
            for i in nauseaSymLst:
                if (i not in list_symptom_of_person):
                    print(f'{count}. {i["noidung"]}')
                count += 1
            print('0. Bỏ qua')
            print('---------------------Câu trả lời của bạn---------------------')

            answer = validate.validate_input_number_form(len(nauseaSymLst))
            if 0 in answer: 
                print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
                print([i['idtrieuchung'] for i in list_symptom_of_person])
                break
            for i in answer:
                list_symptom_of_person.append(nauseaSymLst[i-1])

            # loại bỏ triệu chứng đã chọn trong AllSymLst 
            stt_trieuchung = []
            for i in range(len(nauseaSymLst)):
                if i+1 not in answer:
                    stt_trieuchung.append(i)
            NewAllSymLst = []
            for i in stt_trieuchung:
                NewAllSymLst.append(nauseaSymLst[i])
            nauseaSymLst = NewAllSymLst

            print(f'-->Hệ thống: Danh sách mã các triệu chứng bạn đang mắc:', end=" ")
            print([i['idtrieuchung'] for i in list_symptom_of_person])
        else:
            break
    return list_symptom_of_person

#################################################################
# 5. kịch bản câu hỏi phụ trợ để suy diễn tiến
def forth_question_before_forward_inference(list_symptom_of_person):
    initTree= TreeForFC('S19',TreeForFC('S29',TreeForFC('S22',TreeForFC('S23'),TreeForFC('S24')),
                TreeForFC('S27',TreeForFC('S28'),TreeForFC('S33'))),TreeForFC('S37',TreeForFC('S21',
                TreeForFC('S20'),TreeForFC('S36')),TreeForFC('S25',TreeForFC('S26'),TreeForFC('S34'))))
    
    savedTree = initTree

    for i in range(0, 4):
        currentSym = db.get_trieuchung_by_id(savedTree.value)
        print(
            f'-->Hệ thống: Bạn có triệu chứng {currentSym["noidung"]} không ( trả lời 1 hoặc 0) :')
        answer = validate.validate_binary_answer(input())
        print(f'-->Bạn: Câu trả lời của tôi là {answer}')
        if (answer == True):
            savedTree = savedTree.left
            list_symptom_of_person.append(currentSym)
        else:
            savedTree = savedTree.right
        print(f'-->Hệ thống: Danh sách mã các triệu chứng mà bạn đang mắc', [
              i['idtrieuchung'] for i in list_symptom_of_person])

    return list_symptom_of_person




################################################################
# 6 phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_disease = [i for i in fc.facts if i[0] == "D"]
    print("---------------------------------------------------------")
    print(
        f'-->Hệ thống: Chúng tôi dự đoán bạn có thể bị bệnh :', end="")
    
    for i in list_predicted_disease:
        temp = db.get_benh_by_id(i)
        print(temp['tenBenh'], end=', ')
    
    print("sau đây chúng tôi sẽ hỏi bạn một số câu hỏi để đưa ra kết quả chính xác.")
    print()
    
    return list_predicted_disease




########################################################################
# 7 phần suy diễn lùi
def backward_chaining(luat_lui,list_symptom_of_person_id,list_predicted_disease,file_name ):
    predictD=list_predicted_disease
    rule=luat_lui
    all_rule=db.gettrieuchung()
    fact_real=list_symptom_of_person_id
    benh=0
    for g in predictD:
        goal=g
        D=db.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
        print()
        print(f"--> Hệ thống : Chúng tôi đã có các triệu chứng ban đầu và có thể bạn mắc bệnh {D['tenBenh']}({goal})", end="")
        print(", sau đây chúng tôi muốn hỏi bạn một vài câu hỏi để tìm hiểu về bệnh bạn đang mắc phải.")
        all_s_in_D=all_rule[goal]
        all_s_in_D=sorted(set(all_s_in_D)-set(fact_real))
        d=searchindexrule(rule,goal)
        
        b=BackwardChaining(rule,fact_real,goal,file_name) # kết luận trong trường hợp các luât jtruwowsc đã suy ra đk luôn
        
        if b.result1==True:# đoạn đầu
            print("--> Hệ thống : Bạn mắc bệnh {}- {}, sau đây là lời khuyên chi tiết cho bạn.".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng hệ hệ thống của chúng tôi")
            return goal,fact_real
        
        while(len(all_s_in_D)>0):
            s=db.get_trieuchung_by_id(all_s_in_D[0])
            question=f"--> Hệ thống : Bạn có bị triệu chứng {s['noidung']}({all_s_in_D[0]}) không?"
            print(question)
            answer = validate.validate_binary_answer(input())
            
            print(f"answer: {answer}")
            if answer== True :
                fact_real.append(all_s_in_D[0])
                b=BackwardChaining(rule,fact_real,goal,file_name)
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,1)
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
                if b.result1==True:
                    benh=1
                    break
            if answer==False :
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,0) #S01 S02 S03 S04 S05
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
            if len(d)==0: 
                print(f"--> Hệ thống : Có vẻ như bạn không mắc bệnh {goal}-{D['tenBenh']}")
                break
        if benh==1:
            print("--> Hệ thống : Bạn mắc bệnh {}- {} , và sau đây là lời khuyên chi tiết".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng hệ thống của chúng tôi")
            
            return goal,fact_real
            break
    if benh==0:
        print(f"Bạn không bị bệnh nào cả")
        return None, fact_real



    

person = welcome_question()
list_symptom_of_person = []  # list các đối tượng triệu chứng


list_symptom_of_person = first_question(list_symptom_of_person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

list_symptom_of_person = second_question(list_symptom_of_person)
list_symptom_of_person = third_question(list_symptom_of_person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])

list_symptom_of_person = extra_question(list_symptom_of_person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])

list_symptom_of_person=nausea_question(list_symptom_of_person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])

list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])

list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
list_symptom_of_person_id = list(set(list_symptom_of_person_id))
list_symptom_of_person_id.sort()

list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex')
# print(list_predicted_disease)


if len(list_predicted_disease)==0 :
    print("Bạn không có dấu hiệu của bệnh nào cả.Cám ơn bạn đã sử dụng hệ thống.")
    sys.exit()

'''list_predicted_disease=['D01','D02','D03']
list_symptom_of_person_id=['S01','S02','S04','S09']'''
disease,list_symptom_of_person_id= backward_chaining(luat_lui,list_symptom_of_person_id,list_predicted_disease,"ex")

