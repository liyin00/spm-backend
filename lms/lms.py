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
    prerequisites = db.Column(db.String(999), nullable=False) #db cannot store list NEEDS CHANGE
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
    learnerIds = db.Column(db.String(999), nullable=False) #if it is empty, insert an empty dict
    trainerId = db.Column(db.Integer(), nullable=True)
    classSize = db.Column(db.Integer(), nullable=True)

    def change_to_dict(self):
        string = self.learnerIds
        json_acceptable_string = string.replace("'", "\"")
        new_dict = json.loads(json_acceptable_string)
        return new_dict
    
    def json(self):
        return {"courseClassId": self.courseClassId,
                "courseId": self.courseId, 
                "startDateTime": self.startDateTime, 
                "endDateTime": self.endDateTime, 
                "learnerIds": self.learnerIds, 
                "trainerId": self.trainerId,
                "classSize": self.classSize}

class Lesson(db.Model):
    __tablename__ = 'lesson'
    
    lessonId = db.Column(db.Integer(), primary_key=True)
    courseClassId = db.Column(db.Integer(), nullable = False)
    lessonName = db.Column(db.String(250), nullable=False)
    lessonContent = db.Column(db.PickleType(), nullable=True) #db cannot store list NEEDS CHANGE
    links = db.Column(db.PickleType(), nullable=True) #db cannot store list NEEDS CHANGE

    def json(self):
        return {"lessonId": self.lessonId,
                "courseClassId": self.courseClassId, 
                "lessonName": self.lessonName, 
                "lessonContent": self.lessonContent, 
                "links": self.links}

class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subrole = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def json(self):
        return {"userId": self.userId,
                "name": self.name, 
                "subrole": self.subrole, 
                "department": self.department, 
                "email": self.email}

class Quiz(db.Model):
    __tablename__ = 'quiz'
 
    quizId = db.Column(db.Integer(), primary_key=True)
    lessonId = db.Column(db.Integer(), nullable=False)
    isGraded = db.Column(db.Integer(), nullable=True)
    passingMark = db.Column(db.Integer(), nullable=True)
    numOfQns = db.Column(db.Integer(), nullable=True)

    def json(self):
        return {"quizId": self.quizId, 
                "lessonId": self.lessonId, 
                "isGraded": self.isGraded, 
                "passingMark": self.passingMark, 
                "numOfQns": self.numOfQns}

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
        for class_info in course_classes:
            class_info.learnerIds = CourseClass.change_to_dict(class_info)
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
    learnerIds = data['learnerIds']
    class_info = CourseClass(courseId=data['courseId'], startDateTime=datetime(int(startDate[2]),int(startDate[1]),int(startDate[0])),
                        endDateTime=datetime(int(endDate[2]),int(endDate[1]),int(endDate[0])), learnerIds=str(learnerIds), 
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
    class_info.learnerIds = CourseClass.change_to_dict(class_info)
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
    new_dict = CourseClass.change_to_dict(class_info)
    if id in new_dict:
        return jsonify(
            {
                "message": "Learner is already in this class."
            }
        ), 500

    new_dict[id] = 0
    class_info.learnerIds = str(new_dict)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when adding learner to the class."
            }
        ), 500
    class_info.learnerIds = CourseClass.change_to_dict(class_info)
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

#start of create sections-----------------------------------------------------------
#find lessons based on courseClassId
@app.route('/lessons/<int:courseClassId>')
def find_lesson_by_courseClassId(courseClassId):
    lessons = Lesson.query.filter_by(courseClassId=courseClassId).all()
    if lessons:
        return jsonify(
            {
                "data": {
                    "lessons": [lesson.json() for lesson in lessons]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "Lessons for this course class cannot be found."
        }
    ), 404

#add new lesson using courseClassId
@app.route("/lesson/add", methods=['POST'])
def create_lesson():
    data = request.get_json()

    if bool(CourseClass.query.filter_by(courseClassId=data['courseClassId']).first()) == False:
        return jsonify(
            {
                "message": "This class does not exist."
            }
        ), 404

    lesson_info = Lesson(courseClassId = data['courseClassId'], lessonName = data['lessonName'],
                        lessonContent = data['lessonContent'], links = data['links'])
    try:
        db.session.add(lesson_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when creating the lesson."
            }
        ), 500

    return jsonify(
        {
            "data": lesson_info.json()
        }
    ), 201

#delete lesson
@app.route("/lesson/delete/<int:lessonId>", methods=['POST'])
def delete_lesson(lessonId):
    lesson_info = Lesson.query.filter_by(lessonId=lessonId).first()
    if lesson_info:
        db.session.delete(lesson_info)
        db.session.commit()
        return jsonify(
            {
                "message": "Lesson was successfully deleted."
            }
        ),200
    return jsonify(
        {
            "message": "Lesson was not found."
        }
    ), 404

#end of create sections--------------------------------------------------------------------------

#start of CRUD users-----------------------------------------------------------
#find all users
@app.route("/user", methods=['GET'])
def get_all_users():
    users = User.query.all()
    if len(users):
        return jsonify(
            {
                "data": {
                    "users": [user.json() for user in users]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "There are no available users."
        }
    ), 404

#search user by user's name
@app.route("/user/name/<string:name>", methods=['GET'])
def get_user_by_name(name):
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify(
            {
                "data": user.json()
            }
        ), 200
    return jsonify(
        {
            "message": "User not found."
        }
    ), 404

#search user by userId
@app.route("/user/id/<string:userId>", methods=['GET'])
def get_user_by_userId(userId):
    user = User.query.filter_by(userId=userId).first()
    if user:
        return jsonify(
            {
                "data": user.json()
            }
        ), 200
    return jsonify(
        {
            "message": "User not found."
        }
    ), 404

#add new user
@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()

    if bool(User.query.filter_by(name=data['name']).first()):
        return jsonify(
            {
                "message": "There is an existing user with the same name."
            }
        ), 500
    
    user_info = User(name=data['name'], subrole=data['subrole'],
                        department=data['department'], email=data['email'])
    try:
        db.session.add(user_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when creating the user."
            }
        ), 500

    return jsonify(
        {
            "data": user_info.json()
        }
    ), 201

#delete user by userId
@app.route("/user/<int:userId>", methods=['DELETE'])
def delete_user(userId):
    user = User.query.filter_by(userId=userId).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(
            {
                "message": "User was successfully deleted."
            }
        ),200
    return jsonify(
        {
            "message": "User was not found."
        }
    ), 404

#update user by userId
@app.route("/user", methods=['PATCH'])
def update_user_by_userId():
    data = request.get_json()
    userId = data['userId']
    
    if bool(User.query.filter_by(userId=userId).first()) == False:
        return jsonify(
            {
                "message": "This user does not exist."
            }
        ), 404

    user_info = User.query.filter_by(userId=userId).first()
    user_info.name = data['name']
    user_info.subrole = data['subrole']
    user_info.department = data['department']
    user_info.email = data['email']
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when updating the user."
            }
        ), 500

    return jsonify(
        {
            "data": user_info.json()
        }
    ), 201

@app.route("/user/engineer/name/<string:name>", methods=['GET'])
def get_engineers_by_name(name):
    engineers = db.session.query(User).filter(User.department=="Engineer", User.name.like("%"+name+"%")).all()
    if engineers:
        return jsonify(
            {
                "data": engineers.json()
            }
        ), 200
    return jsonify(
        {
            "message": "Engineer not found."
        }
    ), 404
#end of CRUD users--------------------------------------------------------------------------
#start of CRUD Quizzes-------------------------

#add new quiz
@app.route("/quiz/add", methods=['POST'])
def create_quiz():
    data = request.get_json()
    
    quiz_info = Quiz(lessonId=data['lessonId'], 
                        isGraded=data['isGraded'],
                        passingMark=data['passingMark'], 
                        numOfQns=data['numOfQns'])
    try:
        db.session.add(quiz_info)
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when creating quiz."
            }
        ), 500

    return jsonify(
        {
            "data": quiz_info.json()
        }
    ), 201

#retrieve quiz by quizId
@app.route("/quiz/<int:quizId>", methods=['GET'])
def view_quiz_by_quizId(quizId):
    course = Quiz.query.filter_by(quizId=quizId).first()
    if course:
        return jsonify(
            {
                "data": course.json()
            }
        ), 200
    return jsonify(
        {
            "message": "Quiz is not found."
        }
    ), 404


#delete quiz by quiz
@app.route("/quiz/delete/<int:quizId>", methods=['POST'])
def delete_quiz(quizId):
    quiz = Quiz.query.filter_by(quizId=quizId).first()
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        return jsonify(
            {
                "message": "Quiz was successfully deleted."
            }
        ),200
    return jsonify(
        {
            "message": "Quiz was not found."
        }
    ), 404

#update quiz by quizId
@app.route("/quiz/update", methods=['POST'])
def update_by_quizId():
    data = request.get_json()
    quizId = data['quizId']
    
    if bool(Quiz.query.filter_by(quizId=quizId).first()) == False:
        return jsonify(
            {
                "message": "This quiz does not exist."
            }
        ), 404

    quiz_info = Quiz.query.filter_by(quizId=quizId).first()
    quiz_info.isGraded = data['isGraded']
    quiz_info.passingMark = data['passingMark']
    quiz_info.numOfQns = data['numOfQns']
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "message": "An error occurred when updating the quiz."
            }
        ), 500

    return jsonify(
        {
            "data": quiz_info.json()
        }
    ), 201
    
#End of Quiz Crud ----------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)