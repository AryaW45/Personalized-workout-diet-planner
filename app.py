from flask import Flask, render_template, request, jsonify
from logic import generate_plan

app = Flask(__name__)   # <-- IMPORTANT FIX

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        workout, diet = generate_plan(data)
        return jsonify({"workout": workout, "diet": diet})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
