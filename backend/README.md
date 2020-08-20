# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash  
python3 -m venv ./venv
source ./venv/bin/activate
```
To remove the virtual environment

```bash  
deactivate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Endpoints (API Documentation)

#### GET / categories

- General: Returns All categories.
- Sample: curl ```http://127.0.0.1:5000/categories```
```
  {
      "categories": {
          "1": "Art", 
          "2": "Science", 
          "3": "Geography"
      }
  }
```
#### GET /questions

- General (Returns all questions,  paginated 10 questions, returns categories with all thier questions )
- Sample: curl ```http://127.0.0.1:5000/questions```
```
  {
      "categories": {
          "1": "Art", 
          "2": "Science", 
          "3": "Geography"
      }, 
      "questions": [
              {
              "answer": "Red", 
              "category": 1, 
              "difficulty": 3, 
              "id": 1, 
              "question": "Which is a primary color?"
          }, 
          {
              "answer": "Everst", 
              "category": 3, 
              "difficulty": 3, 
              "id": 4, 
              "question": "Which is the worlds highest mountain?"
          },  
          {
              "answer": "San Francisco", 
              "category": 3, 
              "difficulty": 2, 
              "id": 14, 
              "question": "In which American city is the Golden Gate Bridge located?"
          }, 
          {
              "answer": "Egypt", 
              "category": 3, 
              "difficulty": 3, 
              "id": 3, 
              "question": "Cairo is the capital of which country?"
          }
      ], 
      "success": true, 
      "total_questions": 4
  }
  ```
#### POST /questions

- General (post new question)
- Sampal ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which US state contains an area known as the Upper Penninsula?", "answer": "Michigan", "difficulty": 3, "category": "3" }'```

```
  { 
      "question_created": "Which US state contains an area known as the Upper Penninsula?",
       "success": true 
      }
  ```

#### DELETE /questions/<question_id>

- General (Delete question by id,  return succssefly with id of question )
- Sample:  ```curl -X DELETE http://127.0.0.1:5000/questions/3 ```
```
  {
    "categories": 
    { 
        "1": "Science",
        "2": "Art",
        "3": "Geography" 
        },
         "deleted": 3,
        "questions": [ { 
            "answer": "Egypt", 
              "category": 3, 
              "difficulty": 3, 
              "id": 3, 
              "question": "Cairo is the capital of which country?"
            ],
            "success": true, 
            "total_questions": 3 
     }
  }
 ``` 

#### POST /questions (search)

- General: Get questions based on a search term
- Sample: curl ``` curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Egypt"}' http://localhost:5000/questions```
```
{
  "questions": [
    {
    "answer": "Egypt", 
              "category": 3, 
              "difficulty": 3, 
              "id": 15, 
              "question": "Cairo is the capital of which country?"
    }
  ],
  "success": true,
  "total_questions": 3
}
 ```

 #### GET /categories/<category_id>

- General: Gets questions by category 
- Sample: curl ```curl http://localhost:5000/categories/1 ```
```
{
  "current_category": "Geography",
  "questions": [
    {
              "answer": "Red", 
              "category": 1, 
              "difficulty": 3, 
              "id": 1, 
              "question": "Which is a primary color?"
    }
  ],
  "success": true,
  "total_questions": 1
}
 ```


 #### POST /quizzes

- General: (Get questions to play the quiz  )
- Sample: curl ```curl -X POST http://localhost:5000/categories/quizzes```
```
{ 
      "question": {
          "answer": "Red", 
          "category": 1, 
          "difficulty": 4, 
          "id": 1, 
          "question": " Which is a primary color?"
      }, 
      "success": true,
      current_category:1

  }

 ```

## Error Handling

This API will return four types of errors:

- 400 - Bad request error
- 404 - Resource not found
- 422 - Unprocessable entity
- 500 - Error has occured, please try again