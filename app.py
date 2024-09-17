from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory FAQs list for demonstration purposes
faqs = []

# Error handler for 404 errors (resource not found)
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

# Error handler for 400 errors (bad requests)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Fetch all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs), 200

# Fetch a single FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    faq = next((item for item in faqs if item['id'] == faq_id), None)
    if faq is None:
        abort(404)  # Triggers the 404 error handler
    return jsonify(faq), 200

# Create a new FAQ
@app.route('/faqs', methods=['POST'])
def create_faq():
    data = request.json

    # Validation: Ensure title and description are present
    if not data or 'name' not in data or 'description' not in data:
        abort(400)  # Triggers the 400 error handler

    new_id = len(faqs) + 1
    faq = {
        'id': new_id,
        'name': data['name'],
        'description': data['description']
    }
    faqs.append(faq)
    return jsonify(faq), 201

# Update an existing FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    faq = next((item for item in faqs if item['id'] == faq_id), None)
    if faq is None:
        abort(404)  # Triggers the 404 error handler

    data = request.json

    # Validation: Ensure title or description is provided
    if not data or ('title' not in data and 'description' not in data):
        abort(400)

    faq['title'] = data.get('title', faq['title'])
    faq['description'] = data.get('description', faq['description'])
    
    return jsonify(faq), 200

# Delete an FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    global faqs
    faq = next((item for item in faqs if item['id'] == faq_id), None)
    if faq is None:
        abort(404)

    faqs = [item for item in faqs if item['id'] != faq_id]
    return jsonify({'message': 'FAQ deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
