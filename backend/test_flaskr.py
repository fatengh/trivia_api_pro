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
        self.database_path = "postgres://{}/{}".format( 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        with self.app.app_context():
           self.db = SQLAlchemy()
           self.db.init_app(self.app)
            # create all tables
           self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
  
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
       
        
    def test_404_sent_requesting_non_existing_category(self):
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_question(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
       

    def test_delete_question(self):
        question = Question(question='new question', answer='new answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_422_sent_deleting_non_existing_question(self):
        res = self.client().delete('/questions/a')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

     
    
      
    def test_post_questions(self):
        
        new_data = {
            'question': 'This is a fake question',
            'answer': 'this is a fake answer',
            'difficulty': 1,
            'category': 1,
        }

        response = self.client().post('/questions', json=new_data )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_create_question_with_empty_data(self):
        """Test for ensuring data with empty fields are not processed."""
        emp_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }

        response = self.client().post('/questions', json=emp_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

  

    def test_get_questions_by_category_fail(self):
        category_id = 0
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_quiz_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client().post('/quizzes', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'],
                             request_data['previous_questions'])

    def test_get_quiz_questions_fail(self):
        res = self.client().post('/quizzes', data=json.dumps({}),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
