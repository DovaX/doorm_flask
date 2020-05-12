from flask import Flask, jsonify, request 
from flask_mysqldb import MySQL 
from flask_cors import CORS
import dorm as dm

app = Flask(__name__)

app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
CORS(app)

TABLE_NAME=""

item_name="item"
column1_name="column1"
column2_name="column2"


@app.route('/api/'+item_name+'s', methods=['GET'])
def get_all_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM "+TABLE_NAME)
    rv = cur.fetchall()
    return jsonify(rv)

@app.route('/api/'+item_name, methods=['POST'])
def add_task():
    cur = mysql.connection.cursor()
    column1 = request.get_json()[column1_name]
    column2 = request.get_json()[column2_name]

    cur.execute("INSERT INTO "+TABLE_NAME+" ("+column1_name+","+column2_name+") VALUES ('" + str(column1) + "','"+str(column2)+"')")
                
    mysql.connection.commit()
    result = {column1_name:column1,column2_name:column2}

    return jsonify({"result": result})

@app.route("/api/"+item_name+"/<id>", methods=['PUT'])
def update_task(id):
    cur = mysql.connection.cursor()
    column1 = request.get_json()[column1_name]
    
    cur.execute("UPDATE "+TABLE_NAME+" SET "+column1_name+" = '" + str(column1) + "' where id = " + id)
    mysql.connection.commit()
    result = {column1_name:column1}

    return jsonify({"reuslt": result})

@app.route("/api/"+item_name+"/<id>", methods=['DELETE'])
def delete_task(id):
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM "+TABLE_NAME+" where id = " + id)
    mysql.connection.commit()

    if response > 0:
        result = {'message' : 'record deleted'}
    else:
        result = {'message' : 'no record found'}
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)