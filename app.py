from flask import Flask, request, jsonify
import mysql.connector as ms

app = Flask(__name__)

# Function to get a database connection
def get_connection():
    try:
        connection = ms.connect(
            host="localhost", 
            user="root", 
            password="iamsql", 
            port=3308, 
            database="work"
        )
        return connection
    except ms.Error as err:
        print(f"Error: {err}")
        return None

# API endpoint to create a user (CREATE)
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the User API!"

@app.route('/users', methods=['POST'])
def api_create_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or age is None:
        return jsonify({"error": "Invalid input"}), 400
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (name, age) VALUES (%s, %s)"
            cursor.execute(query, (name, age))
            connection.commit()
            return jsonify({"message": "Record inserted successfully", "id": cursor.lastrowid}), 201
        except ms.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            connection.close()
    return jsonify({"error": "Connection error"}), 500

# API endpoint to retrieve users (READ)
@app.route('/users', methods=['GET'])
def api_read_users():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            data = cursor.fetchall()
            users = [{"id": row[0], "name": row[1], "age": row[2]} for row in data]
            return jsonify(users), 200
        except ms.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            connection.close()
    return jsonify({"error": "Connection error"}), 500

# API endpoint to update a user (UPDATE)
@app.route('/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or age is None:
        return jsonify({"error": "Invalid input"}), 400
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
            cursor.execute(query, (name, age, user_id))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({"message": "Record updated successfully"}), 200
            else:
                return jsonify({"message": "No record found with that ID"}), 404
        except ms.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            connection.close()
    return jsonify({"error": "Connection error"}), 500

# API endpoint to delete a user (DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({"message": "Record deleted successfully"}), 200
            else:
                return jsonify({"message": "No record found with that ID"}), 404
        except ms.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            connection.close()
    return jsonify({"error": "Connection error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
