# Learning Management System (LMS) Backend

This repositry contains the backend system for our Software Project Management class. It is a python Flask backend for our Learning Management System, which is a platform for Learners, Trainers and Admins to do perform the following duties: 
+ Learners to take the courses assigned to them and go through the learning materials 
+ Trainers to upload materials and keep track of learner's progress 
+ Admins for assigning learners and trainers to the courses and classes 

## Information 
This repository has been configured with a CI/CD pipeline which leverages on Gitlab for testing and ultimately AWS ECS for deployment. The database involved is a MySQL database which has been deployed to AWS RDS.

Backend EC2 URL: 
> http://54.80.18.11:5000/ 

## Instructions for running locally 

### Create virtual environment

In your project root directory:
``` 
python3 -m venv venv
```

### Start virtual environment
```
.\venv\Scripts\activate
```

### Download dependencies
```
pip install -r requirements.txt
```

### Running instructions 
```
python app.py 
```

### Group Members: Ling Li Yin, Glenda Marie Satuito, Goh Wei Jie, Jeremy Tan E-Shen
