# API Hackathon 
# Yaseen Alli 
# Alex Urban 

# Part 2 creating API
# Import libraries 
from flask import Flask, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/recipes/<keyword>/<dish_type>/<cuisine_type>/<meal_type>/<calories>', methods=['GET'])
def get_recipes(keyword, dish_type, cuisine_type, meal_type, calories):
    print('Request received')
    
    # Connect to MySQL database
    conn = pymysql.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='b543b1c5defb62',
        password='28c47692',
        db='heroku_0fd2f804d4d62c0',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # Build SQL query based on filters
    query = "SELECT Name, Image, ROUND(Calories,0), CuisineType, MealType, DishType, CookTime, Ingredients, url FROM Recipes WHERE Name LIKE %s"
    args = ('%' + keyword + '%',) 

    if dish_type:
        query += " AND (DishType LIKE %s)"
        args += ('%' + dish_type + '%',)
        
    if cuisine_type:
        query += " AND (CuisineType LIKE %s)"
        args += ('%' + cuisine_type + '%',)

    if meal_type:
        query += " AND (MealType LIKE %s)"
        args += ('%' + meal_type + '%',)
    
    if calories:
        query += " AND (Calories <= %s)"
        args += (calories,)
    
    # Execute SQL query to retrieve recipes based on filters
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        results = cursor.fetchall()

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

    # Close database connection
    conn.close()

    # Return the data in JSON format 
    return jsonify({'recipes': recipes})

if __name__ == '__main__':
    # Set the port number to 5000 (default Flask port number is 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
