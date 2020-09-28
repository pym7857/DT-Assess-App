import pymysql
import pandas as pd
from flask import Flask, render_template, request
import operator

app = Flask(__name__)


db = pymysql.connect(
    host='127.0.0.1', 
    port=3306, 
    user='root', 
    passwd='1562', 
    db='assess_db', 
    charset='utf8'
)
#cursor = db.cursor(pymysql.cursors.DictCursor)
cursor = db.cursor()
#sql = '''SELECT * FROM test1_table;'''
#cursor.execute(sql)
#result = cursor.fetchall()
#db.close()
#print(str(result))


h1_total = 0
h2_total = 0
err_msg = ""
score = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
opinion = ['','','','','','','','','','','','',''] # 13개
dic = {'권봉현 전무': 0, '김동현 전무': 0, '서장철 담당(DP)': 0, '김영근 상무': 0, '이건욱 상무': 0, '조욱동 이사': 0, '김정옥 이사': 0, '김준길 이사': 0, '김유종 이사': 0, '채대석 이사': 0, '박경록 담당': 0, '서장철 담당(DT)': 0, '신용학 담당': 0}
who = ""
presenter_list = ['권봉현 전무', '김동현 전무' '서장철 담당(DP)', '김영근 상무', '이건욱 상무', '조욱동 이사', '김정옥 이사', '김준길 이사', '김유종 이사', '채대석 이사', '박경록 담당', '서장철 담당(DT)', '신용학 담당']

@app.route('/', methods=['GET', 'POST'])
def index():
    global h1_total, h2_total, score, err_msg, dic, who, opinion

    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':

        human_no = 0
        total_sum = 0
        mul_list = [4,2,2,2,2,4,4]

        try:
            i = 0
            for key, value in request.form.items():
                print('i = ',i)
                print("key: {0}, value: {1}".format(key, value))

                human_no = int(str(key[1:2]))
                print('human_no = ', human_no)

                if i != 7:
                    total_sum += int(value)*mul_list[i]
                    score[human_no-1][i] = int(value)*mul_list[i]
                if i == 7:
                    opinion[human_no-1] = value

                i += 1

            print('==========================')
            print('total_sum = ', total_sum)
            if i == 8:
                print(i, 'good')
                err_msg = ""
                if human_no == 1:
                    dic['권봉현 전무'] = total_sum
                elif human_no == 2:
                    dic['김동현 전무'] = total_sum
                elif human_no == 3:
                    dic['서장철 담당(DP)'] = total_sum
                elif human_no == 4:
                    dic['김영근 상무'] = total_sum
                elif human_no == 5:
                    dic['이건욱 상무'] = total_sum
                elif human_no == 6:
                    dic['조욱동 이사'] = total_sum
                elif human_no == 7:
                    dic['김정옥 이사'] = total_sum
                elif human_no == 8:
                    dic['김준길 이사'] = total_sum
                elif human_no == 9:
                    dic['김유종 이사'] = total_sum
                elif human_no == 10:
                    dic['채대석 이사'] = total_sum
                elif human_no == 11:
                    dic['빅경록 담당'] = total_sum
                elif human_no == 12:
                    dic['서장철 담당(DT)'] = total_sum
                elif human_no == 13:
                    dic['신용학 담당'] = total_sum
            else:
                print(i, 'bad')
                err_msg = "오류 메시지: 점수를 모두 입력해주세요!"
        except:
            print('pass')
            err_msg = "오류 메시지: 점수를 모두 입력해주세요!"
            pass


        sdict= dict(sorted(dic.items(), key=operator.itemgetter(1), reverse=True)) # for 실시간 차트
        print('sdict = \n', sdict)

        print('who = ', who) # 평가자
        print('opinion = ', opinion)
        print('score = ', score)

        presenter = presenter_list[human_no-1]
        print('presenter = ', presenter)

        cat1 = score[human_no-1][0] + score[human_no-1][1]
        cat2 = score[human_no-1][2] + score[human_no-1][3] + score[human_no-1][4]
        cat3 = score[human_no-1][5] + score[human_no-1][6]
        print('cat1, cat2, cat3 = ', cat1, cat2, cat3)

        q1 = score[human_no-1][0]
        q2 = score[human_no-1][1]
        q3 = score[human_no-1][2]
        q4 = score[human_no-1][3]
        q5 = score[human_no-1][4]
        q6 = score[human_no-1][5]
        q7 = score[human_no-1][6]
        comment = opinion[human_no-1]
        print('q1, q2, q3, q4, q5, q6, q7 = ', q1, q2, q3, q4, q5, q6, q7)
        print('comment = ', comment)
        print('err_msg = ', err_msg)

        sql = '''UPDATE assess_table SET q1=%s, q2=%s, q3=%s, q4=%s, q5=%s, q6=%s, q7=%s, total=%s, cat1=%s, cat2=%s, cat3=%s, comment=%s WHERE assessor=%s and presenter=%s'''
        cursor.execute(sql, (q1, q2, q3, q4, q5, q6, q7, total_sum, cat1, cat2, cat3, comment, who, presenter))
        db.commit()
        #result = cursor.fetchall()
        #print(str(result))

        return render_template('index.html', sdict=sdict, err_msg=err_msg, who=who)

@app.route('/start', methods=['GET', 'POST'])
def start():
    global who
    if request.method == 'GET':
        return render_template('start.html')
    if request.method == 'POST':
        who = str(request.form['who'])
        print('who2 = ', who)
        
        return render_template('index.html', who=who)

@app.route('/end', methods=['GET'])
def end():
    if request.method == 'GET':
        try:
            db.close()
        except:
            pass
        return render_template('end.html')

@app.route('/standard', methods=['GET'])
def standard():
    if request.method == 'GET':
        return render_template('standard.html')

if __name__ == "__main__":
    app.run(debug=True)