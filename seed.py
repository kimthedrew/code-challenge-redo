from app import app
from models import db, Vendor, Sweet, VendorSweet

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create vendors
        v1 = Vendor(name="Insomnia Cookies")
        v2 = Vendor(name="Cookies Cream")

        # Create sweets
        s1 = Sweet(name="Chocolate Chip Cookie")
        s2 = Sweet(name="Brownie")
        s3 = Sweet(name="M&Ms Cookie")

        # Create vendor_sweets
        vs1 = VendorSweet(price=45, vendor=v1, sweet=s1)
        vs2 = VendorSweet(price=50, vendor=v1, sweet=s2)
        vs3 = VendorSweet(price=300, vendor=v1, sweet=s3)
        vs4 = VendorSweet(price=55, vendor=v2, sweet=s1)

        db.session.add_all([v1, v2, s1, s2, s3, vs1, vs2, vs3, vs4])
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print("Database seeded!")