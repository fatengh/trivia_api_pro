import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, db_drop_and_create_all, Question, Category
from flask_migrate import Migrate


QUESTIONS_PER_PAGE = 10

def pagination_question(request, selection):
    #paginat questions
    page = request.args.get('page', 1, type=int)
    first = (page - 1) * QUESTIONS_PER_PAGE
    end = first + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    curr_question = questions[first:end]

    return curr_question

def pick_categories():
    # retrieve all categories
    categor= Category.query.all()
    categor_dict = {}
    
    for item in categor:
      categor_dict[item.id] = item.type
    
    return categor_dict

def create_app(test_config=None):
  # create and configure the app
 app = Flask(__name__)
 setup_db(app)
 migrate = Migrate(app)
 db_drop_and_create_all()



  # Set up CORS. Allow '*' for origins.
 CORS(app, resources={r"/api/*": {"origins": "*"}})
  


 @app.after_request
 def after_request(response):
   #after_request decorator to set Access-Control-Allow
    response.headers.add(
       'Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add(
       'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

    return response


 @app.route('/categories')
 def get_all_categories():
  # endpoint to handle GET requests for all available categories.
  try:
     return jsonify({
         'categories': pick_categories()
     }),200
  except:
      abort(500)



 @app.route('/questions', methods=['GET'])
 def get_question():
     #endpoint to handle GET requests for questions
    selection = Question.query.order_by(Question.id).all()
    curr_question = pagination_question(request, selection)
 
     # if not found any question
    if (len(curr_question) == 0):
         abort(404)
     # return statement
    return jsonify({
         'success': True,
         'questions': curr_question,
         'total_questions': len(selection),
         'categories': pick_categories()
         
     })

 @app.route('/questions/<int:question_id>', methods=['DELETE'])
 def delete_question(question_id):
   #endpoint to DELETE question using a question ID
    try:
        question = Question.query.get(question_id)
        if question is None:
          abort(404)
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        curr_question = pagination_question(request, selection)
      # return statment
        return jsonify({
         'success': True,
         'deleted': question_id,
         'questions': curr_question,
         'total_questions': len(selection),
         'categories': pick_categories()
    })
    except:
       abort(422)


 @app.route('/questions', methods=['POST'])
 def create_question():
        #endpoint to POST a new question 
      body = request.get_json()
      search = body.get('searchTerm', None)
            
      try:
        if search:
           selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
           questions = pagination_question(request, selection)
           total_questions = len(selection)

           if questions is None:
               abort(404)
           else:
               return jsonify ({
                  'success': True,
                  'questions': questions,
                  'total_questions': total_questions,
                  })
        else:
          new_ques = body.get('question',None)
          new_ans = body.get('answer',None)
          new_difficult = body.get('difficulty',None)
          new_category = body.get('category',None)

    
        # create new question
          question = Question(
            question=new_ques,
            answer=new_ans,
            difficulty=new_difficult,
            category=new_category)
                   # insert new question
          question.insert()
                # return statemnt
          return jsonify({
              'success': True,
              'question_created': question.question,
            
             })

      except:
          abort(422)


 @app.route('/categories/<int:category_id>')
 def get_questions_by_category(category_id):
       #endpoint to get questions based on category

    selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    curr_question = pagination_question(request, selection)
    
        # isn't found
    if selection == []:
      abort(404)
    else:
      return jsonify({
      'success': True,
      'questions': curr_question, 
      'total_questions': len(selection),
      'current_category': category_id
      })



 @app.route('/quizzes', methods=['POST'])
 def play_quiz():
       # endpoint to get questions to play the quiz.

        body = request.get_json()
        prev = body.get('prev_questions',None)
        category = body.get('quiz_category',None)
           
        questionList = Question.query.filter(Question.category == category['id']).order_by(Question.id).all()
        question = random.choice(questionList)
    
        if prev != []:
           while question.id in prev:
               question = random.choice(questionList)

        quiz = question.format()

        return jsonify({
          'success': True,
          'question': quiz,
          'current_category': category
             }), 200


# EROR handelr
 @app.errorhandler(400)
 def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request error"
        }), 400
 @app.errorhandler(404)
 def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

 @app.errorhandler(422)
 def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422
 @app.errorhandler(500)
 def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Error has occured, please try again'
        }), 500

 return app

    