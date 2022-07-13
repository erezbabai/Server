from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session

from assignment4.assignment4 import assignment4


app = Flask(__name__)

app.register_blueprint(assignment4)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)




movie_dict = {
    'Fight club': [139, 'Drama'],
    'Inception': [148, 'Action'],
    'Shutter Island': [138, 'Drama'],
    'The Truemans show': [107, 'Drama'],
    'The dark night': [152, 'Drama']
}

@app.route('/')
def index_func():
    return render_template('HomePage.html')





if __name__ == '__main__':
    app.run(debug=True)


@app.route('/log_out')
def logout_func():
    session['registration'] = False
    session.clear()
    return render_template('assignment3_2.html')


@app.route('/assignment3_1')
def movie_funct():
    user = {'first_name': 'eREZ', 'last_name': 'BabaI', 'email': 'eRezbab@gmail.com', 'ID': '313328874'}
    hobbies = ['Reading', 'dIving', 'WatcHing FootBall', 'HIKING', 'movIes']
    preferences_in_music_dict = {'70s Rock': ['LYNard SKynard', 'Guns N ROSes', 'Bob Dylan', 'The BeaTLES'],
                                 'Mizrahit': ['OmeR Adam', 'EyAl Golan'],
                                 'Country': ['Jhonny CASH', 'Tim MaCgraw'],
                                 'Israeli': ['Ishay RiBo', 'Noa Kirel', 'Ishay RiBo', 'Noa Kirel', 'AmIR DAdon'],
                                 '': ['Sean Paul', 'Eminem', 'Elvis PreslI']}
    favorit_singer = 'Ishay Ribo'
    session['favorit_singer'] = favorit_singer

    if 'movie_name' in request.args:
        movie_name = request.args['movie_name']
        if movie_name in movie_dict:
            return render_template('assignment3_1.html',
                                   movie_name=movie_name,
                                   movie_length=movie_dict[movie_name][0],
                                   movie_genre=movie_dict[movie_name][1],
                                   user=user,
                                   hobbies=hobbies,
                                   preferences_in_music_dict=preferences_in_music_dict,
                                   favorit_singer=favorit_singer
                                   )
        else:
            return render_template('assignment3_1.html',
                                   movie_dict=movie_dict,
                                   user=user,
                                   hobbies=hobbies,
                                   preferences_in_music_dict=preferences_in_music_dict,
                                   favorit_singer=favorit_singer,
                                   message='Movie not found.')
    return render_template('assignment3_1.html',
                           movie_dict=movie_dict,
                           user=user,
                           hobbies=hobbies,
                           preferences_in_music_dict=preferences_in_music_dict,
                           favorit_singer=favorit_singer
                           )







@app.route('/assignment3_2')
@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2_page():
    if request.method == 'GET':
        if 'user_email' in request.args or 'user_ID' in request.args:
                if  request.args['user_email'] =='' and request.args['user_ID'] =='':
                    return render_template('assignment3_2.html',
                                users_list=users_dict)
                else:
                    for u_id, u_info in users_dict.items():
                            for key in u_info:
                                if  key == 'user_email' or key == 'user_ID':
                                 if (u_info[key] == request.args[key]):
                                    user_name = u_info['user_name']
                                    user_nickname = u_info['user_nickname']
                                    user_email = u_info['user_email']
                                    user_Gender = u_info['user_Gender']
                                    user_age = u_info['user_age']
                                    user_ID = u_info['user_ID']
                                    return render_template('assignment3_2.html',
                                                           user_name=user_name,
                                                           user_nickname=user_nickname,
                                                           user_email=user_email,
                                                           user_Gender=user_Gender,
                                                           user_age=user_age,
                                                           user_ID=user_ID)
                    else:
                        return render_template('assignment3_2.html',
                                               message='user not found.')

    elif request.method == 'POST':
            session['registration'] = False
            user_name = request.form['user_name']
            user_nickname = request.form['user_nickname']
            user_ID = request.form['user_ID']
            password = request.form['user_password']
            user_Gender = request.form['user_Gender']
            user_email = request.form['user_email']
            user_age = request.form['user_age']

            for u_id, u_info in users_dict.items():
                for key in u_info:
                    if key == 'user_ID':
                        if u_info[key] == user_ID:
                            return render_template('assignment3_2.html',
                                                   regSitua='ID already exists in the system, please contact us')
                    if key == 'user_email':
                        if u_info[key] == user_email:
                            return render_template('assignment3_2.html',
                                                   regSitua='email already in use')
                    if key == 'user_nickname':
                        if u_info[key] == user_nickname:
                            return render_template('assignment3_2.html',
                                                   regSitua='Nickname already exists in the system,'
                                                            ' try something else ')

            session['username'] = user_name
            session['nickname'] = user_nickname
            session['registration'] = True
            newInfo = {'user_name': user_name, 'user_nickname': user_nickname, 'user_email': user_email, 'user_Gender': user_Gender, 'user_age': user_age, 'user_ID': user_ID, 'user_password': password}
            users_dict['user' + str((len(users_dict.keys())+1))] = newInfo
            return render_template('assignment3_2.html',
                                            regSitua='Success',
                                            username=user_name)


    return render_template('assignment3_2.html')



users_dict = {
        'user1': {'user_name': 'Erez Babai', 'user_nickname': 'erezbab' ,'user_email': 'erezbab@gmail.com', 'user_Gender': 'Male', 'user_age': '27','user_ID': '313328874', 'user_password': 'oA319145959!'},
        'user2': {'user_name': 'Yoni Marziano', 'user_nickname': 'YOma', 'user_email': 'Yoni@gmail.com', 'user_Gender': 'Other', 'user_age': '32','user_ID': '300000030', 'user_password': 'ggg999Oh123'},
        'user3': {'user_name': 'May Blomnder', 'user_nickname': 'Mayblon', 'user_email': 'mayNeg@post.bgu.ac.il', 'user_Gender': 'male', 'user_age': '22','user_ID': '300000031', 'user_password': 'mayaMaya123'},
        'user4': {'user_name': 'Eran Yaacov', 'user_nickname': 'Eranja', 'user_email': 'eran@walla.com', 'user_Gender': 'female', 'user_age': '31','user_ID': '300000032', 'user_password': 'Ron987654S'},
        'user5': {'user_name': 'Shir Regev', 'user_nickname': 'Lasl', 'user_email': 'shir@gmail.com', 'user_Gender': 'male', 'user_age': '77','user_ID': '300000033', 'user_password': 'ShShSh666'},
        'user6': {'user_name': 'Noa Matias', 'user_nickname': 'NoaleeE', 'user_email': 'noaZlo30@gmail.com', 'user_Gender': 'female', 'user_age': '26','user_ID': '300000034', 'user_password': 'Noa5060Zak'}
    }



@app.route('/lynardskynard')
def bestBand():
    return redirect("https://www.youtube.com/channel/UCipLjr-h2iaEBWMJVfK2e2A")

