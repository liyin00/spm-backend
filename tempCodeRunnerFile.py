    # #test delete quiz 
    # def test_delete_quiz(self):
    #     q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
    #                 passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1")
    #     db.session.add(q1)
    #     db.session.commit()

    #     response = self.client.post("/quiz/delete/1")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {
    #         "message": "Quiz was successfully deleted."
    #     })
    
    # #test update existing quiz
    # def test_update_quiz(self):
    #     q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
    #                 passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1")
    #     db.session.add(q1)
    #     db.session.commit()

    #     request_body = {
    #         "quizId": 1,
    #         "lessonId": 1,
    #         "isGraded": 1,
    #         "passingMark": 7,
    #         "numOfQns": 14,
    #         "quizLink": "https://quiz-maker.com/1"
    #     }

    #     response = self.client.post("/quiz/update",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json, {
    #         "data":{
    #             "quizId": 1,
    #             "lessonId": 1,
    #             "isGraded": 1,
    #             "passingMark": 7,
    #             "numOfQns": 14,
    #             "quizLink": "https://quiz-maker.com/1"
    #         }
    #     })