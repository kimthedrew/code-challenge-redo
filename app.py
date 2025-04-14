from flask import Flask, jsonify, request
from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorsweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([vendor.to_dict() for vendor in vendors])

@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if not vendor:
        return jsonify({'error': 'Vendor not found'}), 404
    
    vendor_data = vendor.to_dict()
    vendor_data['vendor_sweets'] = []
    
    for vs in vendor.vendor_sweets:
        vs_data = vs.to_dict()
        vs_data['sweet'] = vs.sweet.to_dict()
        vendor_data['vendor_sweets'].append(vs_data)
    
    return jsonify(vendor_data)

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([sweet.to_dict() for sweet in sweets])

@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if not sweet:
        return jsonify({'error': 'Sweet not found'}), 404
    return jsonify(sweet.to_dict())

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    
    try:
        new_vs = VendorSweet(
            price=data['price'],
            vendor_id=data['vendor_id'],
            sweet_id=data['sweet_id']
        )
        db.session.add(new_vs)
        db.session.commit()
    except Exception as e:
        return jsonify({'errors': [str(e)]}), 400
    
    response_data = new_vs.to_dict()
    response_data['vendor'] = new_vs.vendor.to_dict()
    response_data['sweet'] = new_vs.sweet.to_dict()
    
    return jsonify(response_data), 201

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vs = VendorSweet.query.get(id)
    if not vs:
        return jsonify({'error': 'VendorSweet not found'}), 404
    
    db.session.delete(vs)
    db.session.commit()
    return jsonify({})

if __name__ == '__main__':
    app.run(port=5555, debug=True)