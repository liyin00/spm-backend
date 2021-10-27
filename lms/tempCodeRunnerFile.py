    #test add class
    def test_add_class(self):
        c1 = Course(courseId = 1, courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
            "classSize": 10,
            "courseId": 1,
            "endDateTime": '09/10/2021',
            "learnerIds": {'a': 1, 'b': 0, 'c': 1},
            "startDateTime": '08/10/2021',
            "trainerId": 1
        }

        response = self.client.post("/class/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "classSize": 10,
                "courseClassId": 1,
                "courseId": 1,
                "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
                "learnerIds": {'a': 1, 'b': 0, 'c': 1},
                "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
                "trainerId": 1
            }
        })