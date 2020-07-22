from flask import Flask, jsonify
from flask_cors import CORS

COURSES = [
    {
        "title": "Effective JavaScript: 68 Specific Ways to Harness the Power of JavaScript ",
        "author": "David Herman",
        "paperback": True,
    },
    {
        "title": "JavaScript: The Good Parts",
        "author": "Douglas Crockford",
        "paperback": False,
    },
    {
        "title": "Eloquent JavaScript: A Modern Introduction to Programming",
        "author": "Marijn Haverbeke",
        "paperback": True,
    },
]

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/courses", methods=["GET"])
def all_courses():
    return jsonify({"status": "success", "courses": COURSES})


if __name__ == "__main__":
    app.run(debug=True)
