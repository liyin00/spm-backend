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
