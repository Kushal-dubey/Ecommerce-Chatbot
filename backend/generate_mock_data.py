from app import create_app, db
from app.models import Product
from faker import Faker
import random

app = create_app()
faker = Faker()

CATEGORIES = ['Mobiles', 'Headphones', 'Books', 'Laptops', 'Fashion']

def create_mock_products(n=100):
    with app.app_context():
        db.drop_all()  # Reset DB
        db.create_all()

        for _ in range(n):
            product = Product(
                name=faker.word().capitalize() + " " + random.choice(["Pro", "Max", "Lite", "Plus"]),
                category=random.choice(CATEGORIES),
                price=round(random.uniform(100, 9999), 2),
                description=faker.sentence(nb_words=8),
                rating=round(random.uniform(3.0, 5.0), 1)
            )
            db.session.add(product)

        db.session.commit()
        print(f"✅ Successfully inserted {n} mock products.")

if __name__ == "__main__":
    create_mock_products()
