import pymysql
import pandas as pd
from flask import Flask, render_template, request, redirect, jsonify
import operator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global who
    if request.method == 'GET':
        return render_template('start.html')

    if request.method == 'POST':
        err_msg = ""

        try:
            human_no = 0
            real_human_no = 0
            total_sum = 0

            print('===========forLoop==========')
            i = 0
            for key, value in request.form.items():
                print('i = ',i)
                print("key: {0}, value: {1}".format(key, value))    # key= h10_q1

                if i == 0:
                    # human_no slicing
                    index1 = str(key).find('h')
                    index2 = str(key).find('_')
                    human_no = int(str(key)[index1+1:index2])
                    print('human_no = ', human_no)
                    real_human_no = human_no - 1
                    print('real_human_no = ', real_human_no)

                if i != 7:
                    total_sum += int(value)*mul_list[i]
                    score[real_human_no][i] = int(value)*mul_list[i]
                    chk_num[real_human_no][i] = int(value)
                if i == 7:
                    opinion[real_human_no] = value

                i += 1
            print('===========forLoop==========')

            if i == 8:
                print(i, 'good')
                err_msg = ""
                if human_no == 1:
                    dic['생기/소재연구센터'] = total_sum
                elif human_no == 2:
                    dic['청주사업장1공장'] = total_sum
                elif human_no == 3:
                    dic['DP연구소'] = total_sum
                elif human_no == 4:
                    dic['DT추진단'] = total_sum
                elif human_no == 5:
                    dic['천안사업장'] = total_sum
            else:
                print(i, 'bad')
                err_msg = "오류 메시지: 점수를 모두 입력해주세요! (여기 로직 못옴 이제)"
        except:
            print('pass')
            err_msg = "오류 메시지: 알 수 없는 오류"
            pass


        sdict= dict(sorted(dic.items(), key=operator.itemgetter(1), reverse=True)) # for 실시간 차트 - temp 지역변수
        print('sdict = \n', sdict)

        presenter = presenter_list[real_human_no]
        print('presenter = ', presenter) # 지역변수

        cat1 = score[real_human_no][0] + score[real_human_no][1]
        cat2 = score[real_human_no][2] + score[real_human_no][3] + score[real_human_no][4]
        cat3 = score[real_human_no][5] + score[real_human_no][6]
        print('cat1, cat2, cat3 = ', cat1, cat2, cat3) # 지역변수

        q1 = score[real_human_no][0]
        q2 = score[real_human_no][1]
        q3 = score[real_human_no][2]
        q4 = score[real_human_no][3]
        q5 = score[real_human_no][4]
        q6 = score[real_human_no][5]
        q7 = score[real_human_no][6]
        comment = opinion[real_human_no]
        print('q1, q2, q3, q4, q5, q6, q7 = ', q1, q2, q3, q4, q5, q6, q7) # 지역변수
        print('comment = ', comment)
        print('err_msg = ', err_msg)
        print('who2 = ', who)

        sql = '''UPDATE assess_table_2 SET q1=%s, q2=%s, q3=%s, q4=%s, q5=%s, q6=%s, q7=%s, total=%s, cat1=%s, cat2=%s, cat3=%s, comment=%s WHERE assessor=%s and presenter=%s'''
        cursor.execute(sql, (q1, q2, q3, q4, q5, q6, q7, total_sum, cat1, cat2, cat3, comment, who, presenter))
        db.commit()

        url_logo = 'https://ls-electric-assessment-app.s3.ap-northeast-2.amazonaws.com/static/img/logo2.jpg'

        # chk_num 배열을 chk_num_text로 변환(for javascript)
        chk_num_text = ''
        for a in chk_num:
            for b in a:
                chk_num_text += str(b)

        comment_list[real_human_no] = comment

        return render_template('index.html', sdict=sdict, err_msg=err_msg, who=who, url_logo=url_logo, chk_num_text=chk_num_text, comment_list=comment_list)

@app.route('/start', methods=['GET', 'POST'])
def start():
    global who
    if request.method == 'GET':
        return render_template('start.html')
    if request.method == 'POST':
        who = str(request.form['who']) # 각자의 고유한 값
        print('who1 = ', who)

        url_logo = 'https://ls-electric-assessment-app.s3.ap-northeast-2.amazonaws.com/static/img/logo2.jpg'

        temp_dic = {'생기/소재연구센터': 0, '청주사업장1공장': 0, 'DP연구소': 0, 'DT추진단': 0, '천안사업장': 0}
        temp_sdict= dict(sorted(temp_dic.items(), key=operator.itemgetter(1), reverse=True))
        
        return render_template('index.html', who=who, url_logo=url_logo, sdict=temp_sdict)

@app.route('/end', methods=['GET'])
def end():
    if request.method == 'GET':
        try:
            db.close()
            print('db 닫았음!')
        except:
            print('db 닫기 실패!!')
            pass
        return render_template('end.html')

@app.route('/standard', methods=['GET'])
def standard():
    if request.method == 'GET':
        url_standard = 'https://ls-electric-assessment-app.s3.ap-northeast-2.amazonaws.com/static/img/standard.png' 
        print('standard uploaded')
        return render_template('standard.html', url_standard=url_standard)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        sql = '''INSERT INTO UserInfo (username, password) VALUES (%s, %s);'''

        cursor.execute(sql, (username, password))
        db.commit()
        db.close()

        #return redirect(request.url)
        return render_template('login.html')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sql = '''SELECT * FROM UserInfo WHERE username=%s'''
        rows_count = cursor.execute(sql, username)

        if rows_count > 0:
            user_info = cursor.fetchone()
            print('user info: ', user_info)

            if password == user_info[2]:
                print('로그인 완료!')
                user_id = user_info[0]
                payload = {
                    'user_id': user_id,
                }
                return render_template('start.html')
            token = jwt.encode(payload, 'aaa', 'HS256')

            print('access_token : ', token.decode('UTF-8'))

            return render_template('login.html')

        else:
            print('User does not exist')
            return render_template('login.html')

    return render_template('login.html')

if __name__ == "__main__":
    db = pymysql.connect(
    host='3.35.27.106', # 새로운 db주소 쓰기
    port=3306,
    user='user1',
    passwd='1234',
    db='assess_db_2', # assess_db_2
    charset='utf8'
    )
    cursor = db.cursor()

    # 모두 공통
    mul_list = [4,2,2,2,2,4,4]
    presenter_list = ['조욱동 이사', '김정옥 이사', '서장철 담당(DP)', '서장철 담당(DT)', '박경록 담당']

    chk_num = [[0,0,0,0,0,0,0] for i in range(5)]
    comment_list = ['' for i in range(5)]

    score = [[0,0,0,0,0,0,0] for i in range(5)]
    opinion = ['' for i in range(5)]

    dic = {'생기/소재연구센터': 0, '청주사업장1공장': 0, 'DP연구소': 0, 'DT추진단': 0, '천안사업장': 0}
    who = ""

    app.run(host='0.0.0.0', debug=True)
    #app.run(debug=True, port=5000)
