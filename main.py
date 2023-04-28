#API Hackathon 
#Yaseen Alli 
#Alex Urban 

#part 2 creating API
#import libraries 

from flask import Flask 
import json 
import requests
import pymysql
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from flask import request


@app.route('/recipes/<keyword>/<dish_type>/<cuisine_type>/<meal_type>/<calories>', methods=['GET'])
def get_recipes(keyword, dish_type, cuisine_type, meal_type, calories ):
    
    #connect to MySQL database
    conn = pymysql.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='b412eb82ae100c',
        password='bf509678',
        db='heroku_d732b73e337efe8',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    #build SQL query based on filters
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
    

    #execute SQL query to retrieve recipes based on filters
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        results = cursor.fetchall()

    #convert results to a dictionary format
    recipes=[]
    for row in results:
        recipe={
            'Name':row['Name'],
            'Image':row['Image'],
            'Calories':row['ROUND(Calories,0)'],
            'CuisineType':row['CuisineType'],
            'MealType':row['MealType'],
            'DishType':row['DishType'],
            'CookTime':row['CookTime'],
            'Ingredients':row['Ingredients'],
            'url':row['url']
        }

        recipes.append(recipe)

    #close database connection
    conn.close()

    #return the data in JSON format 
    return json.dumps({'recipes':recipes})


if __name__ == '__main__':
    app.run(debug=True)


