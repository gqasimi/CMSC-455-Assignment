# product_service.py

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample product data
products = [
    {'id': 1, 'name': 'Apples', 'price': 1.2, 'quantity': 100},
    {'id': 2, 'name': 'Bananas', 'price': 0.5, 'quantity': 150},
    {'id': 3, 'name': 'Carrots', 'price': 0.8, 'quantity': 200}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.json
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(debug=True)
