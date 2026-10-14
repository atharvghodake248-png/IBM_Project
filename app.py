from flask import Flask, jsonify

app = Flask(__name__)

products = {
    "Headphones": ["Tech City", "Ez PC", "GH Computers"],
    "Laptop": ["Tech City", "Ez PC", "GH Computers"],
    "Mouse": ["Tech City", "Ez PC", "GH Computers"],
    "Printer": ["Tech City", "Ez PC", "GH Computers"]
}

@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/")
def home():
    return jsonify({"message": "Product API is running"})

@app.route("/products")
def get_products():
    return jsonify({"products": list(products.keys())})

@app.route("/getdealers/<path:product>")
def get_dealers(product):
    return jsonify({"dealers": products.get(product, [])})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
