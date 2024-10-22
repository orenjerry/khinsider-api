from flask import Flask, jsonify
from api.khinsider import data_blueprint
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"})

app.register_blueprint(data_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=8001, host="0.0.0.0")
