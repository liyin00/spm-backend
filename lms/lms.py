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
    learnerIds = db.Column(db.PickleType(), nullable=True)
    trainerId = db.Column(db.Integer(), nullable=True)
    classSize = db.Column(db.Integer(), nullable=True)

    def json(self):
        return {"courseClassId": self.courseClassId,
                "courseId": self.courseId, 
                "startDateTime": self.startDateTime, 
                "endDateTime": self.endDateTime, 
                "learnerIds": self.learnerIds, 
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

#delete course by courseId
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

#update course by courseId
@app.route("/course/update", methods=['POST'])
def update_by_courseId():
    data = request.get_json()
    courseId = data['courseId']
    
    if bool(Course.query.filter_by(courseId=courseId).first()) == False:
        return jsonify(
            {
                "message": "This course does not exist."
            }
        ), 404

    course_info = Course.query.filter_by(courseId=courseId).first()
    course_info.courseName = data['courseName']
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
@app.route("/class/<int:courseId>", methods=['GET'])
def find_class_by_CourseID(courseId):
    course_classes = CourseClass.query.filter_by(courseId=courseId).all()
    if course_classes:
        return jsonify(
            {
                "data": {
                    "classes": [course_class.json() for course_class in course_classes]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "Classes was not found."
        }
    ), 404

#add new class using courseId
@app.route("/class/add", methods=['POST'])
def create_class():
    data = request.get_json()

    if bool(Course.query.filter_by(courseId=data['courseId']).first()) == False:
        return jsonify(
            {
                "message": "This course does not exist."
            }
        ), 404
    startDate = data['startDateTime'].split('/') #DD/MM/YYYY format
    endDate = data['endDateTime'].split('/') #DD/MM/YYYY format
    class_info = CourseClass(courseId=data['courseId'], startDateTime=datetime(int(startDate[2]),int(startDate[1]),int(startDate[0])),
                        endDateTime=datetime(int(endDate[2]),int(endDate[1]),int(endDate[0])), learnerIds=data['learnerIds'], 
                        trainerId=data['trainerId'],classSize=data['classSize'])
    try:
        db.session.add(class_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when creating the class."
            }
        ), 500

    return jsonify(
        {
            "data": class_info.json()
        }
    ), 201

#delete class
@app.route("/class/delete/<int:courseClassId>", methods=['POST'])
def delete_class(courseClassId):
    class_info = CourseClass.query.filter_by(courseClassId=courseClassId).first()
    if class_info:
        db.session.delete(class_info)
        db.session.commit()
        return jsonify(
            {
                "message": "Class was successfully deleted."
            }
        ),200
    return jsonify(
        {
            "message": "Class was not found."
        }
    ), 404

#add new learner into class
@app.route("/class/add/learner", methods=['POST'])
def add_new_learner():
    data = request.get_json()
    id = data['learnerId']

    if bool(CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()) == False:
        return jsonify(
            {
                "message": "This class does not exist."
            }
        ), 404

    class_info = CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()
    new_dict = dict(class_info.learnerIds) #pickletype is not mutable unless you assign it onto another variable
    if id in new_dict:
        return jsonify(
            {
                "message": "Learner is already in this class."
            }
        ), 500

    new_dict[id] = 0
    class_info.learnerIds = new_dict

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when adding learner to the class."
            }
        ), 500

    return jsonify(
        {
            "data": class_info.json()
        }
    ), 201

#accept new learner into class
@app.route("/class/accept/learner", methods=['POST'])
def accept_new_learner():
    data = request.get_json()
    id = data['learnerId']

    if bool(CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()) == False:
        return jsonify(
            {
                "message": "This class does not exist."
            }
        ), 404

    class_info = CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()
    new_dict = dict(class_info.learnerIds) #pickletype is not mutable unless you assign it onto another variable
    new_dict[id] = 1
    class_info.learnerIds = new_dict

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when accepting learner to the class."
            }
        ), 500

    return jsonify(
        {
            "data": class_info.json()
        }
    ), 201

#add new trainer into class
@app.route("/class/add/trainer", methods=['POST'])
def add_new_trainer():
    data = request.get_json()
    id = data['trainerId']

    if bool(CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()) == False:
        return jsonify(
            {
                "message": "This class does not exist."
            }
        ), 404

    class_info = CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()
    class_info.trainerId = id

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when adding trainer to the class."
            }
        ), 500

    return jsonify(
        {
            "data": class_info.json()
        }
    ), 201

#delete learner from class
@app.route("/class/delete/learner", methods=['POST'])
def cancel_learner():
    data = request.get_json()
    id = data['learnerId']

    if bool(CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()) == False:
        return jsonify(
            {
                "message": "This class does not exist."
            }
        ), 404

    class_info = CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()
    new_dict = dict(class_info.learnerIds) #pickletype is not mutable unless you assign it onto another variable
    if not(id in new_dict):
        return jsonify(
            {
                "message": "Learner is not in this class."
            }
        ), 404

    del new_dict[id]
    class_info.learnerIds = new_dict

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when deleting learner from the class."
            }
        ), 500

    return jsonify(
        {
            "data": class_info.json()
        }
    ), 201
#end of CRUD classes--------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)