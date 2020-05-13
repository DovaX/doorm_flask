from flask import Flask, jsonify, request, json
from flask_mysqldb import MySQL 
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import dorm as dm

app = Flask(__name__)
db1=dm.Mysqldb()


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



def initialize_api():
def rename_function(new_name):
    def decorator(f):
        f.__name__ = new_name
        return f
    return decorator
    
    @app.route('/', methods=['GET'])
    def test():
        print("test")
        return(jsonify({}))
        
    @app.route('/api/'+item_name+'s', methods=['GET'])
    def get_all_items():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM "+TABLE_NAME)
        rv = cur.fetchall()
        return jsonify(rv)
    
    @app.route('/api/'+item_name, methods=['POST'])
    def add_item():
        cur = mysql.connection.cursor()
        column1 = request.get_json()[column1_name]
        column2 = request.get_json()[column2_name]
    
        cur.execute("INSERT INTO "+TABLE_NAME+" ("+column1_name+","+column2_name+") VALUES ('" + str(column1) + "','"+str(column2)+"')")
                    
        mysql.connection.commit()
        result = {column1_name:column1,column2_name:column2}
    
        return jsonify({"result": result})
    
    @app.route("/api/"+item_name+"/<id>", methods=['PUT'])
    def update_item(id):
        cur = mysql.connection.cursor()
        column1 = request.get_json()[column1_name]
        
        cur.execute("UPDATE "+TABLE_NAME+" SET "+column1_name+" = '" + str(column1) + "' where id = " + id)
        mysql.connection.commit()
        result = {column1_name:column1}
    
        return jsonify({"reuslt": result})
    
    @app.route("/api/"+item_name+"/<id>", methods=['DELETE'])
    def delete_item(id):
        cur = mysql.connection.cursor()
        response = cur.execute("DELETE FROM "+TABLE_NAME+" where id = " + id)
        mysql.connection.commit()
    
        if response > 0:
            result = {'message' : 'record deleted'}
        else:
            result = {'message' : 'no record found'}
        return jsonify({"result": result})
    
    
    
    @app.route('/api/'+item_name+'/register', methods=['POST'])
    def register():
        cur = mysql.connection.cursor()
        email = request.get_json()['email']
        password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
        creation_utc_time = datetime.utcnow()
    	
        cur.execute("INSERT INTO "+TABLE_NAME+" (email, password, creation_utc_time) VALUES ('" + 
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
    	
    
    @app.route('/api/'+item_name+'/login', methods=['POST'])
    def login():
        cur = mysql.connection.cursor()
        email = request.get_json()['email']
        password = request.get_json()['password']
        result = ""
    	
        cur.execute("SELECT * FROM "+TABLE_NAME+" where email = '" + str(email) + "'")
        rv = cur.fetchone()
    	
        if bcrypt.check_password_hash(rv['password'], password):
            access_token = create_access_token(identity = {'email': rv['email']})
            result = access_token
        else:
            result = jsonify({"error":"Invalid username and password"})
        
        return result

if __name__ == '__main__':
    initialize_api()
    app.run(debug=True)