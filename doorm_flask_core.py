from flask import Flask, jsonify, request, json
from flask_mysqldb import MySQL 
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import dorm as dm


"""
Template
app = Flask(__name__)
db1=dm.Mysqldb()
db1.close_connection()

app.config['MYSQL_USER'] = db1.DB_USERNAME
app.config['MYSQL_PASSWORD'] = db1.DB_PASSWORD
app.config['MYSQL_DB'] = db1.DB_DATABASE
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)
CORS(app)

TABLE_NAME="users"

item_name="item"
column1_name="column1"
column2_name="column2"

doorm_flask_dict={'users':'read','items':'read'}
"""



#CRUD API - CREATE, READ, UPDATE, DELETE

def rename_function(new_name):
    def decorator(f):
        f.__name__ = new_name
        return f
    return decorator

def initialize_api(app,doorm_flask_dict,column1_name,mysql):   
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    for k,v in doorm_flask_dict.items():
        if 'read' in v:
            @app.route('/api/'+k, methods=['GET'])
            @rename_function('read_all_'+k)
            def read_all_x(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM "+k)
                rv = cur.fetchall()
                return jsonify(rv)
    
        if 'create' in v:
            item=k[:-1]
            @app.route('/api/'+item, methods=['POST'])
            @rename_function('create_'+item)
            def add_item(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                column1 = request.get_json()[column1_name]
                #column2 = request.get_json()[column2_name]
            
                cur.execute("INSERT INTO "+k+" ("+column1_name+") VALUES ('" + str(column1) + "')")
                            #,"+column2_name+"
                            #'"+str(column2)+"'
         
                mysql.connection.commit()                
                result = {column1_name:column1}#,column2_name:column2}            
                return jsonify({"result": result})
    
        if 'update' in v:
            item=k[:-1]
            @app.route("/api/"+item+"/<id>", methods=['PUT'])
            @rename_function('update_'+item)
            def update_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                column1 = request.get_json()[column1_name]
                
                cur.execute("UPDATE "+k+" SET "+column1_name+" = '" + str(column1) + "' where id = " + id)
                mysql.connection.commit()
                result = {column1_name:column1}
            
                return jsonify({"reuslt": result})
    
        if 'delete' in v:
            item=k[:-1]
            @app.route("/api/"+item+"/<id>", methods=['DELETE'])
            @rename_function('delete_'+item)
            def delete_item(id,k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                response = cur.execute("DELETE FROM "+k+" where id = " + id)
                mysql.connection.commit()
            
                if response > 0:
                    result = {'message' : 'record deleted'}
                else:
                    result = {'message' : 'no record found'}
                return jsonify({"result": result})
            
        if 'register' in v:
            item=k[:-1]    
            @app.route('/api/'+item+'/register', methods=['POST'])
            @rename_function('register_'+item)
            def register(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                email = request.get_json()['email']
                #req_pass=request.get_json()['password']
                password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
                creation_utc_time = datetime.utcnow()
            	
                cur.execute("INSERT INTO "+k+" (email, password, creation_utc_time) VALUES ('" + 
            		str(email) + "', '" + 
            		str(password) + "', '" + 
            		str(creation_utc_time) + "')")
                mysql.connection.commit()
            	
                result = {
            		'email' : email,
            		'password' : password,
            		'created' : creation_utc_time
            	}
            
                return jsonify({'result' : result})
      
        if 'login' in v:
            item=k[:-1]    
            @app.route('/api/'+item+'/login', methods=['POST'])
            @rename_function('login_'+item)
            def login(k=k): #k=k because of late binding - otherwise, it would assign all endpoints with the same k
                cur = mysql.connection.cursor()
                email = request.get_json()['email']
                password = request.get_json()['password']
                result = ""
            	
                cur.execute("SELECT * FROM "+k+" where email = '" + str(email) + "'")
                rv = cur.fetchone()
                print("RV",rv)
                if bcrypt.check_password_hash(rv['password'], password):
                    access_token = create_access_token(identity = {'email': rv['email'],'id':rv['id']})
                    result = access_token
                else:
                    result = jsonify({"error":"Invalid username and password"})
                
                return result

"""
if __name__ == '__main__':
    initialize_api()
    
    #globals['read_all_users']()
    app.run(debug=True)
    
"""