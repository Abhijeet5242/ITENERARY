from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'abhi5242',
    'database': 'ferryite',
    'auth_plugin': 'mysql_native_password'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-ferry-route', methods=['POST'])
def add_ferry_route():
    data = request.form
    ferry_name = data.get('ferryName')
    capacity = data.get('capacity')
    start_point = data.get('startPoint')
    end_point = data.get('endPoint')
    distance = data.get('distance')
    dinner_Lunch = data.get('dinner/Lunch')
    meal_type = data.get('mealType')
    activities_list = request.form.getlist('activities')  # Handle multiple values
    return_plan = data.get('returnPlan')
    description = data.get('description')

    # Convert activities list to a comma-separated string
    activitiesl = ','.join(activities_list) if activities_list else None

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        sql = "INSERT INTO users (ferry_name, capacity, start_point, end_point, distance, dinner_Lunch, activitiesl, returnPlan, mealType, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (ferry_name, capacity, start_point, end_point, distance, dinner_Lunch, activitiesl, return_plan, meal_type, description)
        
        # Ensure all required data is provided
        if None in val or '' in val:
            return "Missing required data", 400

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500

    return redirect(url_for('index'))


@app.route('/get-ferry-routes')
def get_ferry_routes():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM FerryRoutes")
        routes = cursor.fetchall()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Database error: {err}", 500

    return jsonify(routes)

if __name__ == '__main__':
    app.run(debug=True)
