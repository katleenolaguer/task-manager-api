from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
tasks = []

# Helper function to find a task by ID
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Get a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"message": "Task not found"}), 404

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not 'title' in data or not 'description' in data:
        return jsonify({"message": "Title and description are required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data["description"],
        "status": "Pending"
    }
    tasks.append(new_task)
    return jsonify({"message": "Task created successfully", "id": new_task["id"]}), 201

# Update a task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    task.update({
        "title": data.get("title", task["title"]),
        "description": data.get("description", task["description"]),
        "status": data.get("status", task["status"])
    })
    return jsonify({"message": "Task updated successfully"}), 200

# Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = find_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)