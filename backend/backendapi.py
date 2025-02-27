import hashlib
import flask
from flask import request, make_response
from flask import jsonify

from sql import create_connection
from sql import execute_read_query
from sql import execute_update_query

import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Some API code is taken from class lecture and homeworks. Inspiration taken from w3schools, geeksforgeeks, and Stack Overflow.

# Create endpoint for login API with username: username and password: password
@app.route('/daycareauthentication', methods=['POST'])
def auth_test():
    request_data = request.get_json()
    if request_data['auth'] == "true":
        global authentication
        authentication = 'Success'
        return 'Authorized user access'
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# Create endpoint for API to view information from facility table
@app.route('/viewfacility', methods=['GET'])
def view_facility():
    if authentication == 'Success':
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select name from facility"
        facilities = execute_read_query(conn, sql)
        return jsonify(facilities)
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to add information to facility table
@app.route('/addfacility', methods=['POST'])
def add_facility():
    if authentication == 'Success':
        request_data = request.get_json()
        new_name = str(request_data['new_name'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"insert into facility(name) values ('{new_name}')"

        execute_update_query(conn, sql)
        return 'Add facility information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to update information in facility table
@app.route('/updatefacility', methods=['PUT'])
def update_facility():
    if authentication == 'Success':
        request_data = request.get_json()
        name_to_update = str(request_data['name_to_update'])
        new_name = str(request_data['new_name'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"update facility set name = '{new_name}' where name = '{name_to_update}'"

        execute_update_query(conn, sql)
        return 'Update facility information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to delete information from facility table
@app.route('/deletefacility', methods=['DELETE'])
def delete_facility():
    if authentication == 'Success':
        if "facnametodelete" in request.args:
            name_to_delete = str(request.args["facnametodelete"])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"delete from facility where name = '{name_to_delete}'"

        execute_update_query(conn, sql)
        return 'Delete facility information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to view information from classroom table
@app.route('/viewclassroom', methods=['GET'])
def view_classroom():
    if authentication == 'Success':
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select capacity, classroom.name as classroom_name, facility.name as facility_name from classroom join facility on classroom.facility = facility.id"
        classrooms = execute_read_query(conn, sql)
        return jsonify(classrooms)
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to add information to classroom table
@app.route('/addclassroom', methods=['POST'])
def add_classroom():
    if authentication == 'Success':
        request_data = request.get_json()
        new_capacity = int(request_data['new_capacity'])
        classroomname = str(request_data['classroomname'])
        facilityname = str(request_data['facilityname'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select name from facility"
        facilities = execute_read_query(conn, sql)
        test = "False"
        for i in facilities:
            if i["name"] == facilityname:
                test = "True"
                break
        if test == "True":
            sql = f"set @facility_id = (select id from facility where name = '{facilityname}');"
            execute_update_query(conn, sql)
            sql = f"insert into classroom(capacity, name, facility) values ({new_capacity}, '{classroomname}', @facility_id);"
            execute_update_query(conn, sql)
            return 'Add information to classroom table successful!'
        else:
            return 'Add information to classroom table failed. Facility name does not exist in database. Please choose an existing facility name.'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to update information in classroom table
@app.route('/updateclassroom', methods=['PUT'])
def update_classroom():
    if authentication == 'Success':
        request_data = request.get_json()
        capacity_to_update = int(request_data['capacity_to_update'])
        new_capacity = int(request_data['new_capacity'])
        classroomname_to_update = str(request_data['classroomname_to_update'])
        new_classroomname = str(request_data['new_classroomname'])
        facilityname_to_update = str(request_data['facilityname_to_update'])
        new_facility = str(request_data['new_facility'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select name from facility"
        facilities = execute_read_query(conn, sql)
        test = "False"
        for i in facilities:
            if i["name"] == new_facility:
                test = "True"
                break
        if test == "True":
            sql = f"set @facility_id_to_update = (select id from facility where name = '{facilityname_to_update}');"
            execute_update_query(conn, sql)
            sql = f"set @facility_id_new = (select id from facility where name = '{new_facility}');"
            execute_update_query(conn, sql)
            sql = f"update classroom set capacity = {new_capacity}, name = '{new_classroomname}', facility = @facility_id_new where capacity = {capacity_to_update} and name = '{classroomname_to_update}' and facility = @facility_id_to_update;"
            execute_update_query(conn, sql)
            return 'Update information in classroom table successful!'
        else:
            return 'Update information in classroom table failed. New facility name does not exist in database. Please choose a different new facility name.'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to delete information from classroom table
@app.route('/deleteclassroom', methods=['DELETE'])
def delete_classroom():
    if authentication == 'Success':
        if ("capacity_to_delete" and "classroomname_to_delete" and "facilityname_to_delete") in request.args:
            capacity_to_delete = int(request.args['capacity_to_delete'])
            classroomname_to_delete = str(request.args['classroomname_to_delete'])
            facilityname_to_delete = str(request.args['facilityname_to_delete'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"set @facility_id_to_delete = (select id from facility where name = '{facilityname_to_delete}');"
        execute_update_query(conn, sql)
        sql = f"delete from classroom where capacity = {capacity_to_delete} and name = '{classroomname_to_delete}' and facility = @facility_id_to_delete;"
        execute_update_query(conn, sql)
        return 'Delete classroom information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to view information from teacher table
@app.route('/viewteacher', methods=['GET'])
def view_teacher():
    if authentication == 'Success':
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select firstname, lastname, classroom.name as room from teacher join classroom on teacher.room = classroom.id"
        teachers = execute_read_query(conn, sql)
        return jsonify(teachers)
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to add information to teacher table
@app.route('/addteacher', methods=['POST'])
def add_teacher():
    if authentication == 'Success':
        request_data = request.get_json()
        new_firstname = str(request_data['new_firstname'])
        new_lastname = str(request_data['new_lastname'])
        capacity = int(request_data['capacity'])
        roomname = str(request_data['roomname'])
        facilityname = str(request_data["facilityname"])
        
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"select id from facility where name = '{facilityname}';"
        test = execute_read_query(conn, sql)
        test1 = []
        for i in test:
            test1.append(i['id'])
        sql = "select capacity, name, facility from classroom"
        classroom = execute_read_query(conn, sql)
        test2 = "False"
        for i in classroom:
            if i["capacity"] == capacity and i["name"] == roomname and i["facility"] == test1[0]:
                test2 = "True"
                break
        if test2 == "True":
            sql = f"select id from classroom where capacity = {capacity} and name = '{roomname}' and facility = {test1[0]};"
            test3 = execute_read_query(conn, sql)
            test4 = []
            for i in test3:
                test4.append(i['id'])
            sql = f"select count(*) from teacher join classroom on teacher.room = classroom.id where teacher.room = {test4[0]};"
            test5 = execute_read_query(conn, sql)
            test6 = []
            for i in test5:
                test6.append(i['count(*)'])
            if (len(test1) == 0) or (len(test4) == 0) or (len(test6) == 0):
                return 'Add information to teacher table failed. Classroom does not exist in database. Please choose an existing classroom'
            if ((test6[0])*10) < capacity:
                sql = f"insert into teacher(firstname, lastname, room) values ('{new_firstname}', '{new_lastname}', {test4[0]});"
                execute_update_query(conn, sql)
                return 'Add information to teacher table successful!'
            else:
                return "Add information to teacher table failed. There are already enough teachers to fill this classroom's capacity. Please choose a different classroom"
        else: 
            return 'Add information to teacher table failed. Classroom does not exist in database. Please choose an existing classroom'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to update information in teacher table
@app.route('/updateteacher', methods=['PUT'])
def update_teacher():
    if authentication == 'Success':
        request_data = request.get_json()
        firstname_to_update = str(request_data['firstname_to_update'])
        new_firstname = str(request_data['new_firstname'])
        lastname_to_update = str(request_data['lastname_to_update'])
        new_lastname = str(request_data['new_lastname'])
        roomname_to_update = str(request_data['roomname_to_update'])
        new_roomname = str(request_data['new_roomname'])
        oldfacilityname = str(request_data["oldfacilityname"])
        newfacilityname = str(request_data['newfacilityname'])
        oldcapacity = int(request_data["oldcapacity"])
        newcapacity = int(request_data["newcapacity"])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"select id from facility where name = '{oldfacilityname}';"
        test = execute_read_query(conn, sql)
        test1 = []
        for i in test:
            test1.append(i['id'])
        sql = f"select id from facility where name = '{newfacilityname}';"
        test2 = execute_read_query(conn, sql)
        test3 = []
        for i in test2:
            test3.append(i['id'])
        sql = f"select id from classroom where capacity = {oldcapacity} and name = '{roomname_to_update}' and facility = {test1[0]};"
        test4 = execute_read_query(conn, sql)
        test5 = []
        for i in test4:
            test5.append(i['id'])
        sql = f"select id from classroom where capacity = {newcapacity} and name = '{new_roomname}' and facility = {test3[0]};"
        test6 = execute_read_query(conn, sql)
        test7 = []
        for i in test6:
            test7.append(i["id"])
        sql = f"select id from classroom;"
        test8 = execute_read_query(conn,sql)
        test9 = []
        for i in test8:
            test9.append(i["id"])
        if (len(test1) == 0) or (len(test3) == 0) or (len(test5) == 0) or (len(test7) == 0) or (len(test9) == 0):
            return 'Update information in teacher table failed. Classroom does not exist in database. Please choose an existing classroom'
        if (test5[0] and test7[0]) in test9:
            sql = f"update teacher set firstname = '{new_firstname}', lastname = '{new_lastname}', room = {test7[0]} where firstname = '{firstname_to_update}' and lastname = '{lastname_to_update}' and room = {test5[0]};"
            execute_update_query(conn, sql)
            return 'Update information in teacher table successful!'
        else:
            return 'Update information in teacher table failed. Classroom does not exist in database. Please choose an existing classroom'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"

# Create endpoint for API to delete information from teacher table
@app.route('/deleteteacher', methods=['DELETE'])
def delete_teacher():
    if authentication == 'Success':
        if ("firstname_to_delete" and "lastname_to_delete" and "roomname_to_delete") in request.args:
            firstname_to_delete = str(request.args['firstname_to_delete'])
            lastname_to_delete = str(request.args['lastname_to_delete'])
            roomname_to_delete = str(request.args['roomname_to_delete'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"set @room_id_to_delete = (select id from classroom where name = '{roomname_to_delete}');"
        execute_update_query(conn, sql)
        sql = f"delete from teacher where firstname = '{firstname_to_delete}' and lastname = '{lastname_to_delete}' and room = @room_id_to_delete;"
        execute_update_query(conn, sql)
        return 'Delete teacher information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to view information from child table
@app.route('/viewchild', methods=['GET'])
def view_child():
    if authentication == 'Success':
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = "select firstname, lastname, age, classroom.name as room from child join classroom on child.room = classroom.id"
        children = execute_read_query(conn, sql)
        return jsonify(children)
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"

# Create endpoint for API to add information to child table
@app.route('/addchild', methods=['POST'])
def add_child():
    if authentication == 'Success':
        request_data = request.get_json()
        new_firstname = str(request_data['new_firstname'])
        new_lastname = str(request_data['new_lastname'])
        new_age= int(request_data['new_age'])
        roomname = str(request_data['roomname'])
        capacity = int(request_data['capacity'])
        facilityname = str(request_data['facilityname'])

        
        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"select id from facility where name = '{facilityname}';"
        test = execute_read_query(conn, sql)
        test1 = []
        for i in test:
            test1.append(i['id'])
        sql = "select capacity, name, facility from classroom"
        classroom = execute_read_query(conn, sql)
        test2 = "False"
        for i in classroom:
            if i["capacity"] == capacity and i["name"] == roomname and i["facility"] == test1[0]:
                test2 = "True"
                break
        if test2 == "True":
            sql = f"select id from classroom where capacity = {capacity} and name = '{roomname}' and facility = {test1[0]};"
            test3 = execute_read_query(conn, sql)
            test4 = []
            for i in test3:
                test4.append(i['id'])
            sql = f"select count(*) from child join classroom on child.room = classroom.id where child.room = {test4[0]};"
            test5 = execute_read_query(conn, sql)
            test6 = []
            for i in test5:
                test6.append(i['count(*)'])
            sql = f"select count(*) from teacher join classroom on teacher.room = classroom.id where teacher.room = {test4[0]};"
            test7 = execute_read_query(conn, sql)
            test8 = []
            for i in test7:
                test8.append(i['count(*)'])
            if (len(test1) == 0) or (len(test4) == 0) or (len(test6) == 0) or (len(test8) == 0):
                return 'Add information to child table failed. Classroom does not exist in database. Please choose an existing classroom.'
            if test6[0] < (test8[0]*10):
                sql = f"insert into child(firstname, lastname, age, room) values ('{new_firstname}', '{new_lastname}', {new_age}, {test4[0]});"
                execute_update_query(conn, sql)
                return 'Add information to child table successful!'
            else: 
                return 'Add information to child table failed. Not enough teachers in this classroom to watch a new child. Please choose another classroom.'
        else:
            return 'Add information to child table failed. Classroom does not exist in the database. Please choose an existing classroom.'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"
    
# Create endpoint for API to update information in child table
@app.route('/updatechild', methods=['PUT'])
def update_child():
    if authentication == 'Success':
        request_data = request.get_json()
        firstname_to_update = str(request_data['firstname_to_update'])
        new_firstname = str(request_data['new_firstname'])
        lastname_to_update = str(request_data['lastname_to_update'])
        new_lastname = str(request_data['new_lastname'])
        age_to_update = int(request_data['age_to_update'])
        new_age = int(request_data['new_age'])
        roomname_to_update = str(request_data['roomname_to_update'])
        new_roomname = str(request_data['new_roomname'])
        oldfacilityname = str(request_data["oldfacilityname"])
        newfacilityname = str(request_data['newfacilityname'])
        oldcapacity = int(request_data["oldcapacity"])
        newcapacity = int(request_data["newcapacity"])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"select id from facility where name = '{oldfacilityname}';"
        test = execute_read_query(conn, sql)
        test1 = []
        for i in test:
            test1.append(i['id'])
        sql = f"select id from facility where name = '{newfacilityname}';"
        test2 = execute_read_query(conn, sql)
        test3 = []
        for i in test2:
            test3.append(i['id'])
        sql = f"select id from classroom where capacity = {oldcapacity} and name = '{roomname_to_update}' and facility = {test1[0]};"
        test4 = execute_read_query(conn, sql)
        test5 = []
        for i in test4:
            test5.append(i['id'])
        sql = f"select id from classroom where capacity = {newcapacity} and name = '{new_roomname}' and facility = {test3[0]};"
        test6 = execute_read_query(conn, sql)
        test7 = []
        for i in test6:
            test7.append(i["id"])
        sql = f"select id from classroom;"
        test8 = execute_read_query(conn,sql)
        test9 = []
        for i in test8:
            test9.append(i["id"])
        if (len(test5) == 0) or (len(test7) == 0):
            return 'Update information in child table failed. Classroom does not exist in database. Please choose an existing classroom.'
        if (test5[0] and test7[0]) in test9:
            sql = f"select count(*) from child join classroom on child.room = classroom.id where child.room = {test7[0]};"
            test10 = execute_read_query(conn, sql)
            test11 = []
            for i in test10:
                test11.append(i['count(*)'])
            sql = f"select count(*) from teacher join classroom on teacher.room = classroom.id where teacher.room = {test7[0]};"
            test12 = execute_read_query(conn, sql)
            test13 = []
            for i in test12:
                test13.append(i['count(*)'])
            if test11[0] < (test13[0]*10):
                sql = f"update child set firstname = '{new_firstname}', lastname = '{new_lastname}', age = {new_age}, room = {test7[0]} where firstname = '{firstname_to_update}' and lastname = '{lastname_to_update}' and age = {age_to_update} and room = {test5[0]}"
                execute_update_query(conn, sql)
                return 'Update information in child table successful!'
            else:
                return 'Update information in child table failed. Not enough teachers in this classroom to watch a new child. Please choose another classroom.'
        else:
            return 'Update information in child table failed. Classroom does not exist in database. Please choose an existing classroom.'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"

# Create endpoint for API to delete information from child table
@app.route('/deletechild', methods=['DELETE'])
def delete_child():
    if authentication == 'Success':
        if ('firstname_to_delete' and 'lastname_to_delete' and 'age_to_delete' and 'roomname_to_delete') in request.args:
            firstname_to_delete = str(request.args['firstname_to_delete'])
            lastname_to_delete = str(request.args['lastname_to_delete'])
            age_to_delete = int(request.args['age_to_delete'])
            roomname_to_delete = str(request.args['roomname_to_delete'])

        myCreds = creds.creds()
        conn = create_connection(myCreds.myhostname, myCreds.uname, myCreds.passwd, myCreds.dbname)
        sql = f"set @room_id_to_delete = (select id from classroom where name = '{roomname_to_delete}');"
        execute_update_query(conn, sql)
        sql = f"delete from child where firstname = '{firstname_to_delete}' and lastname = '{lastname_to_delete}' and age = {age_to_delete} and room = @room_id_to_delete;"
        execute_update_query(conn, sql)
        return 'Delete child information successful!'
    else:
        return "Access denied, please go to '/daycareauthentication' endpoint to login"

app.run()