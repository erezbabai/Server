from flask import Flask, redirect, render_template, jsonify, Blueprint
from flask import render_template
from flask import request, session
import requests
import mysql.connector
import mysql

assignment4 = Blueprint('assignment4', __name__,
                         static_folder='static',
                         static_url_path='/',
                         template_folder='templates')



# Home page function
@assignment4.route('/')
def assignment4_func():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)




def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='eb313328874',
                                         database='hw4')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# SELECT
@assignment4.route('/select_users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)



# insert
@assignment4.route('/insert_user',methods=['POST'])
def insert_user():
    user_name = request.form['user_name']
    user_nickname = request.form['user_nickname']
    user_ID = int(request.form['user_ID'])
    password = request.form['user_password']
    user_Gender = request.form['user_Gender']
    user_email = request.form['user_email']
    query = f'select * from users'
    usersList = interact_db(query, query_type='fetch')

    for u in usersList:
        if user_nickname == u.user_nickname or u.user_ID == user_ID or user_email == u.user_email:
            return render_template('assignment4.html',users= usersList, regMessage='Another account with the same ID, Email or nickname'
                                                ' already exits please try another combination')


    query = "INSERT INTO users(user_name, user_nickname ,user_email, user_age, user_Gender, user_ID, user_password) VALUES ('%s','%s','%s','%d','%s','%d','%s' ) " % (user_name, user_nickname, user_email, 45 , user_Gender, user_ID, password)
    interact_db(query, query_type='commit')
    query = f'select * from users'
    usersList = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=usersList, regMessage='Inserted')


@assignment4.route('/assignment_4')
def assignment_4_page():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)

# DELETE
@assignment4.route('/delete_user', methods=['POST'])
def delete_user_func():

    user_id = int(request.form['user_id'])
    queryGetUsers = f'select * from users'
    usersList = interact_db(queryGetUsers, query_type='fetch')
    if findUser(user_id):
            query = "DELETE FROM users WHERE user_id= '%d';" % user_id
            interact_db(query, query_type='commit')
            queryGetUsers = f'select * from users'
            usersList = interact_db(queryGetUsers, query_type='fetch')
            return render_template('assignment4.html', users=usersList, deleteMessage='User Deleted')

    return render_template('assignment4.html', users=usersList, deleteMessage= 'User Not Exist')

# UPDATE
@assignment4.route('/update_user', methods=['POST'])
def update_user_func():
    id = int(request.form['user_id'])
    password = request.form['user_pass']
    gender = request.form['user_Gender']
    queryGetUsers = f'select * from users'
    usersList = interact_db(queryGetUsers, query_type='fetch')

    if findUser(id):
            query = "UPDATE users set user_Gender= '%s'  ,user_password= '%s'   WHERE user_id= '%d';" % \
                    (gender, password, id)
            interact_db(query, query_type='commit')
            queryGetUsers = f'select * from users'
            usersList = interact_db(queryGetUsers, query_type='fetch')
            return render_template('assignment4.html', users= usersList, updateMessage= 'User details updated')

    return render_template('assignment4.html', users=usersList, updateMessage= 'User ID is incorrect')


# get all user JSON
@assignment4.route('/assignment4/users')
def getallusers():
        query = f'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'ID': user.user_ID,
                'name': user.user_name,
                'nickname': user.user_nickname,
                'Gender': user.user_Gender,
                'email': user.user_email,
                'Age': user.user_age
                }
            return_list.append(user_dict)
        return jsonify(return_list)


@assignment4.route('/assignment4/outer_source')
def assignment4_outer_source_page():
    return render_template('assignment4_outerSource.html')


@assignment4.route('/fetch_back_end')
def fetch_back_end_func():
    ID = request.args['id_backend']
    result= requests.get(f'https://reqres.in/api/users/{ID}')
    if result is not None:
        info=result.json()
        for userData_Key, userData_Values in info.items():
            for key in userData_Values:
                if key == 'avatar':
                    picture = userData_Values['avatar']
                if key == 'first_name':
                    first_name=userData_Values['first_name']
                if key == 'last_name':
                    last_name = userData_Values['last_name']
                if key == 'email':
                 user_email = userData_Values['email']

            return render_template('assignment4_outerSource.html', userFirstName=first_name
                               , userLastName=last_name, picture=picture, userEmail=user_email)
    return  render_template('assignment4_outerSource.html', backendMessage= 'User with that ID doesnt exist')



# PART C
@assignment4.route('/assignment4/restapi_users/', defaults={'user_ID': 300000032})
@assignment4.route('/assignment4/restapi_users/<int:user_ID>')
def restapi_users__func(user_ID):
    if user_ID == 300000032:
        query = "select * FROM users WHERE user_ID='300000032';"
        users_list = interact_db(query, query_type='fetch')
        firstObject = users_list[0]
        return jsonify(firstObject)

    user_query = "select * FROM users WHERE user_ID='%s';" % user_ID
    users_list = interact_db(user_query, query_type='fetch')

    if len(users_list) != 0:
        user = users_list[0]
    else:
        user={
        'ERROR':'We couldnt find the user'
        }
    return jsonify(user)



def findUser(ID):
    query = 'select * from users'
    usersList = interact_db(query, query_type='fetch')
    for i in usersList:
        if i.user_ID == ID:
            return True
    return False

