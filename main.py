from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
cache = {}

def get_db_uri():
    db_config = {
        "user": "myuser",
        "password": "mypassword",
        "host": "localhost",
        "port": "5432",
        "database": "recipes"
    }
    return f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

@app.route('/recipes/<string:keyword>/<string:dish_type>/<string:cuisine_type>/<string:meal_type>/<int:calories>')
def get_recipes(keyword, dish_type, cuisine_type, meal_type, calories):
    if keyword or dish_type or cuisine_type or meal_type or calories:
        if keyword not in cache:
            cache[keyword] = {}

        if dish_type not in cache[keyword]:
            db_uri = get_db_uri()
            engine = create_engine(db_uri, echo=True)

            query, args = build_query(keyword, dish_type, cuisine_type, meal_type, calories)
            result = engine.execute(query, args).fetchall()

            cache[keyword][dish_type] = result
        
        return jsonify(cache[keyword][dish_type])
    else:
        raise BadRequest("At least one parameter should be provided.")

def build_query(keyword, dish_type, cuisine_type, meal_type, calories):
    query = text("SELECT * FROM recipes WHERE 1=1")
    args = {}

    if keyword:
        query = query.where(text("Name LIKE :keyword"))
        args['keyword'] = f"%{keyword}%"

    if dish_type:
        query = query.where(text("DishType LIKE :dish_type"))
        args['dish_type'] = f"%{dish_type}%"

    if cuisine_type:
        query = query.where(text("CuisineType LIKE :cuisine_type"))
        args['cuisine_type'] = f"%{cuisine_type}%"

    if meal_type:
        query = query.where(text("MealType LIKE :meal_type"))
        args['meal_type'] = f"%{meal_type}%"

    if calories:
        query = query.where(text("Calories <= :calories"))
        args['calories'] = calories

    return query, args

if __name__ == '__main__':
    app.run(debug=True)
