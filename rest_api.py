from flask import Flask, jsonify
import os

app = Flask(__name__)

DATA_FOLDER = "data"

@app.route("/files", methods=["GET"])
def list_files():
    """Mengembalikan daftar file yang ada di folder 'data'"""
    if not os.path.exists(DATA_FOLDER):
        return jsonify({"files": []}), 404

    files = os.listdir(DATA_FOLDER)
    return jsonify({"files": files})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
