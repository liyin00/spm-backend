import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'account' #waiting for confirmation of table name
 
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(50), nullable=False)
    CourseDescription = db.Column(db.String(50), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
 
    # def __init__(self, id, name, age, phone):
    def __init__(self, CourseID, CourseName, CourseDescription, StartDate, EndDate):
        # self.id = id
        self.CourseID = CourseID
        self.CourseName = CourseName
        self.CourseDescription = CourseDescription
        self.StartDate = StartDate
        self.EndDate = EndDate
 
    def json(self):
        return {"CourseID": self.CourseID, 
                "CourseName": self.CourseName, 
                "CourseDescription": self.CourseDescription, 
                "StartDate": self.StartDate, 
                "EndDate": self.EndDate}

#find all courses
@app.route("/courses")
def get_all():
    courses = Course.query.all()
    if len(courses):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in courses]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no course information."
        }
    ), 404

#search course by courseid
@app.route("/course/<int:CourseID>")
def find_by_CourseID(CourseID):
    course = Course.query.filter_by(CourseID=CourseID).first()
    if course:
        return jsonify(

            {
                "code": 200,
                "data": course.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Course Info not found."
        }
    ), 404

#add course
@app.route("/course/add", methods=['POST'])
def create_course():
    data = request.get_json()
    course_info = Course(**data)
   
    try:
        db.session.add(course_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                # "data": {
                #     "phone": patient_info.phone
                # },
                "message": "An error occurred when creating the course."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": course_info.json()
        }
    ), 201

#delete course
@app.route("/course/delete", methods=['POST'])
def delete_course():
    data = request.get_json()
    CourseID = data['CourseID']
    course = Course.query.filter_by(CourseID=CourseID).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "CourseID": CourseID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "CourseID": CourseID
            },
            "message": "Course info not found."
        }
    ), 404

#update courses
@app.route("/course/update", methods=['POST'])
def update_by_CourseID():
    data = request.get_json()
    CourseID = data['CourseID']
    course_info = Course.query.filter_by(CourseID=CourseID).first()
    course_info.CourseName = data.CourseName
    course_info.CourseDescription = data.CourseDescription
    course_info.StartDate = data.StartDate
    course_info.EndDate = data.EndDate
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                # "data": {
                #     "phone": patient_info.phone
                # },
                "message": "An error occurred when updating the course."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": course_info.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)