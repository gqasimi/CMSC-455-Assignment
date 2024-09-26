from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Simulating user carts (cart is a dictionary of user_id -> list of product dicts)
carts = {}

# Endpoint to retrieve a user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, [])
    total_price = sum([item['price'] * item['quantity'] for item in cart])
    return jsonify({'cart': cart, 'total_price': total_price})

# Endpoint to add a product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    # Fetch product details from the Product Service
    product_service_url = f'http://localhost:5000/products/{product_id}'
    product_response = requests.get(product_service_url)

    if product_response.status_code == 404:
        return jsonify({'error': 'Product not found'}), 404
    
    product = product_response.json()
    quantity = request.json.get('quantity', 1)
    
    # Add product to the user's cart (including the 'id' field)
    cart = carts.get(user_id, [])
    cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': quantity})
    carts[user_id] = cart

    return jsonify({'message': 'Product added to cart', 'cart': cart})

# Endpoint to remove a product from the user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    cart = carts.get(user_id, [])
    cart = [item for item in cart if item['id'] != product_id]
    carts[user_id] = cart
    return jsonify({'message': 'Product removed from cart', 'cart': cart})

if __name__ == '__main__':
    app.run(port=5001, debug=True)


