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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/lms' #environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'course'
 
    courseId = db.Column(db.Integer(), primary_key=True)
    courseName = db.Column(db.String(250), nullable=False)
    courseDesc = db.Column(db.String(999), nullable=False)
    prerequisites = db.Column(db.String(999), nullable=False)
    isActive = db.Column(db.Integer(), nullable=False)

    def json(self):
        return {"courseId": self.courseId, 
                "courseName": self.courseName, 
                "courseDesc": self.courseDesc, 
                "prerequisites": self.prerequisites, 
                "isActive": self.isActive}

class CourseClass(db.Model):
    __tablename__ = 'courseclass'
 
    courseClassId = db.Column(db.Integer(), primary_key=True)
    courseId = db.Column(db.Integer(), nullable=False)
    startDateTime = db.Column(db.DateTime(), nullable=True)
    endDateTime = db.Column(db.DateTime(), nullable=True)
    learnersId = db.Column(db.PickleType(), nullable=True)
    trainerId = db.Column(db.Integer(), nullable=True)
    classSize = db.Column(db.Integer(), nullable=True)

    def json(self):
        return {"courseClassId": self.courseClassId,
                "courseId": self.courseId, 
                "startDateTime": self.startDateTime, 
                "endDateTime": self.endDateTime, 
                "learnersId": self.learnersId, 
                "trainerId": self.trainerId,
                "classSize": self.classSize}

db.create_all()

#start of CRUD Courses-----------------------------------------------------------
#find all courses
@app.route("/courses")
def get_all():
    courses = Course.query.all()
    if len(courses):
        return jsonify(
            {
                "data": {
                    "courses": [course.json() for course in courses]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "There is no available course information."
        }
    ), 404

#search course by course name
@app.route("/course/<string:courseName>", methods=['GET'])
def find_by_CourseID(courseName):
    course = Course.query.filter_by(courseName=courseName).first()
    if course:
        return jsonify(

            {
                "data": course.json()
            }
        ), 200
    return jsonify(
        {
            "message": "Course Info not found."
        }
    ), 404

#add new course
@app.route("/course/add", methods=['POST'])
def create_course():
    data = request.get_json()

    if bool(Course.query.filter_by(courseName=data['courseName']).first()):
        return jsonify(
            {
                "message": "There is an existing course with the same name."
            }
        ), 500
    
    course_info = Course(courseName=data['courseName'], courseDesc=data['courseDesc'],
                        prerequisites=data['prerequisites'], isActive=data['isActive'])
    try:
        db.session.add(course_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when creating the course."
            }
        ), 500

    return jsonify(
        {
            "data": course_info.json()
        }
    ), 201

#delete course by course name
@app.route("/course/delete/<int:courseId>", methods=['POST'])
def delete_course(courseId):
    course = Course.query.filter_by(courseId=courseId).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify(
            {
                "message": "Course was successfully deleted."
            }
        ),200
    return jsonify(
        {
            "message": "Course was not found."
        }
    ), 404

#update course by course name
#currently cannot edit the course name itself as i need the name to search the database, will find a work around later on
@app.route("/course/update", methods=['POST'])
def update_by_courseName():
    data = request.get_json()
    courseName = data['courseName']
    
    if bool(Course.query.filter_by(courseName=courseName).first()) == False:
        return jsonify(
            {
                "message": "This course does not exist."
            }
        ), 404

    course_info = Course.query.filter_by(courseName=courseName).first()
    course_info.courseDesc = data['courseDesc']
    course_info.prerequisites = data['prerequisites']
    course_info.isActive = data['isActive']
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when updating the course."
            }
        ), 500

    return jsonify(
        {
            "data": course_info.json()
        }
    ), 201
#end of CRUD courses--------------------------------------------------------------------------

#start of CRUD Classes------------------------------------------------------------------------
#find class based on courseId


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)