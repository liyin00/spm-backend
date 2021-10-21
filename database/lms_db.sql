DROP schema IF EXISTS lms;

CREATE SCHEMA lms;
USE lms;


create table user
(
	userId int NOT NULL AUTO_INCREMENT,
	name varchar(100) NOT NULL,
    subrole varchar(100) NOT NULL,
    department varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    PRIMARY KEY (userId)
);

create table course
(
	courseId int NOT NULL AUTO_INCREMENT,
	courseName varchar(250) NOT NULL,
    courseDesc varchar(999) NOT NULL,
    prerequisites varchar(999) NOT NULL,
    isActive boolean NOT NULL,
    PRIMARY KEY (courseid)
);

create table courseclass
(
	courseClassId int NOT NULL AUTO_INCREMENT,
    courseId int NOT NULL,
    startDateTime datetime,
    endDateTime datetime,
    learnerIds varchar(999) NULL,
    trainerId int NULL,
    classSize int NULL,
    PRIMARY KEY (courseClassId),
    FOREIGN KEY fk1 (courseId) REFERENCES course(courseId)
);

create table courseprogress
(
	learnerId int NULL,
    courseClassId int NOT NULL,
    courseId int NOT NULL,
    isComplete boolean NULL,
    completedDateTime datetime NULL,
    currentLessonId int NULL,
    completedLessonIDs varchar(999) NULL,
    incompleteLessonIDs varchar(999) NULL,
    FOREIGN KEY fk1 (learnerId) REFERENCES user(userId),
    FOREIGN KEY fk2 (courseClassId) REFERENCES courseclass(courseClassId),
    FOREIGN KEY fk3 (courseId) REFERENCES course(courseId)
);

create table lesson
(
	lessonId int NOT NULL AUTO_INCREMENT,
    courseClassId int NOT NULL,
	lessonName varchar(200),
    lessonContent varchar(999),
    links varchar(999),
    PRIMARY KEY (lessonId),
    FOREIGN KEY fk1 (courseClassId) REFERENCES courseclass(courseClassId)
);

create table quiz
(
	quizId int NOT NULL AUTO_INCREMENT,
    lessonId int NOT NULL,
    isGraded boolean NULL,
    passingMark int NULL,
    numOfQns int NULL,
    PRIMARY KEY (quizId),
    FOREIGN KEY fk1 (lessonId) REFERENCES lesson(lessonId)
);

create table question
(
	questionId int NOT NULL AUTO_INCREMENT,
    quizId int NOT NULL,
    type varchar(99) NULL,
    numOfOptions int NULL,
    questionText varchar(999) NULL,
    questionOptions varchar(999) NULL,
    answer char(1) NULL,
    PRIMARY KEY (questionId),
    FOREIGN KEY fk1 (quizId) REFERENCES quiz(quizId)
);

create table quizoutcome
(
	quizOutcomeId int NOT NULL AUTO_INCREMENT,
	quizId int,
    lessonId int,
    userId int,
    courseId int,
    courseClassId int,
    marks int,
    passed boolean,
    attemptedNumber int,  
    PRIMARY KEY (quizOutcomeId),
    FOREIGN KEY fk1 (quizId) REFERENCES quiz(quizId),
    FOREIGN KEY fk2 (lessonId) REFERENCES quiz(lessonId),
    FOREIGN KEY fk3 (courseId) REFERENCES course(courseId),
    FOREIGN KEY fk4 (courseClassId) REFERENCES courseClass(courseClassId),
    FOREIGN KEY fk5 (userId) REFERENCES user(userId)
);

create table questionoutcome
(
	quizId int,
    lessonId int,
    userId int,
    courseId int,
    courseClassId int,
    questionId int,
    quizOutcomeId int,
    selectedOption char(1),
    isCorrect boolean,    
    FOREIGN KEY fk1 (quizId) REFERENCES quiz(quizId),
    FOREIGN KEY fk2 (lessonId) REFERENCES quiz(lessonId),
    FOREIGN KEY fk3 (courseId) REFERENCES quiz(courseId),
    FOREIGN KEY fk4 (courseClassId) REFERENCES courseClass(courseClassId),
    FOREIGN KEY fk5 (questionId) REFERENCES question(questionId),
    FOREIGN KEY fk6 (quizOutcomeId) REFERENCES quizOutcome(quizOutcomeId),
    FOREIGN KEY fk7 (userId) REFERENCES user(userId)
);
