from flask import Flask, Response, request
from flask import jsonify
from flask_cors import CORS
import json
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

@app.route('/fields')
def get_field():
    try:
        conn = pymysql.connect(
            host='field-database.cdsowpyuckv0.us-east-1.rds.amazonaws.com',
            port=3306,
            user='chiajou',
            password='chiajoukuo',
            db='fieldInfo'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fields")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        print(resp)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
		
@app.route('/fields/<int:id>')
def get_field_by_id(id):
    try:
        conn = pymysql.connect(
            host='field-database.cdsowpyuckv0.us-east-1.rds.amazonaws.com',
            port=3306,
            user='chiajou',
            password='chiajoukuo',
            db='fieldInfo'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fields WHERE id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/fields/create', methods=['POST'])
def create_field():
    try:
        _id = request.form.get('id', False)
        _name = request.form.get('name', False)
        _location = request.form.get('location', False)
        _team = request.form.get('team', False)
        _capacity = request.form.get('capacity', False)

        conn = pymysql.connect(
            host='field-database.cdsowpyuckv0.us-east-1.rds.amazonaws.com',
            port=3306,
            user='chiajou',
            password='chiajoukuo',
            db='fieldInfo'
        )

        cursor = conn.cursor()
        query = "INSERT INTO fields(id, name, team, location, capacity) VALUES(%s, %s, %s, %s, %s);"
        info = (_id, _name, _location, _team, _capacity)
        print(info)
        cursor.execute(query, info)
        resp = jsonify('Post successfully.')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
