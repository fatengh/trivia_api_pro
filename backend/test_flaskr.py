import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Question, Category
from flaskr import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
  
    def test_404_out_range_page(self):
        #pagination failure 404
        r = self.client().get('/questions?page=1000')
        data = json.loads(r.data)
        # make assertion on the response
        self.assertEqual(r.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_question(self):
        r = self.client().delete('/questions/4')
        data = json.loads(r.data)
        question = Question.query.get(4)
        # make assertion on the response
        self.assertEqual(data['success'], True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['deleted'], 4)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_creation_fails(self):
        #question creation failure 
        ques_before = Question.query.all()
        # load data
        r = self.client().post('/questions', json={})
        data = json.loads(r.data)
        ques_after = Question.query.all()
        # make assertion on the response
        self.assertEqual(r.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(ques_after) == len(ques_before))

    def test_questions_category_fails(self):
        #questions by category failure 
        # request category id 122
        r = self.client().get('/categories/122/questions')
        data = json.loads(r.data)
        # make assertion on the response
        self.assertEqual(r.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'your reguest is bad try again')

    def test_play_quiz_fails(self):
        # playing quiz  failure 
        r = self.client().post('/quizzes', json={})
        data = json.loads(r.data)
        # make assertion on the response
        self.assertEqual(r.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'your reguest is bad try again')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()