# Import libraries
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set up the database connection
engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4".format(
    host='us-cdbr-east-06.cleardb.net',
    user='b543b1c5defb62',
    password='28c47692',
    database='heroku_0fd2f804d4d62c0'
))

@app.route('/recipes/<keyword>/<dish_type>/<cuisine_type>/<meal_type>/<calories>', methods=['GET'])
def get_recipes(keyword, dish_type, cuisine_type, meal_type, calories):
    print('Request received')
    
    # Build SQL query based on filters
    query = text("SELECT Name, Image, ROUND(Calories,0), CuisineType, MealType, DishType, CookTime, Ingredients, url FROM Recipes WHERE Name LIKE :keyword")
    args = {'keyword': '%' + keyword + '%'} 

    if dish_type:
        query = text(query.text + " AND (DishType LIKE :dish_type)")
        args['dish_type'] = '%' + dish_type + '%'
        
    if cuisine_type:
        query = text(query.text + " AND (CuisineType LIKE :cuisine_type)")
        args['cuisine_type'] = '%' + cuisine_type + '%'

    if meal_type:
        query = text(query.text + " AND (MealType LIKE :meal_type)")
        args['meal_type'] = '%' + meal_type + '%'
    
    if calories:
        query = text(query.text + " AND (Calories <= :calories)")
        args['calories'] = calories
    
    # Execute SQL query to retrieve recipes based on filters
    with engine.connect() as conn:
        results = conn.execute(query, args)

    # Convert results to a dictionary format
    recipes = []
    for row in results:
        recipe = {
            'Name': row['Name'],
            'Image': row['Image'],
            'Calories': row['ROUND(Calories,0)'],
            'CuisineType': row['CuisineType'],
            'MealType': row['MealType'],
            'DishType': row['DishType'],
            'CookTime': row['CookTime'],
            'Ingredients': row['Ingredients'],
            'url': row['url']
        }

        recipes.append(recipe)

    # Return the data in JSON format 
    return jsonify({'recipes': recipes})

if __name__ == '__main__':
    # Set the port number to 5000 (default Flask port number is 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
