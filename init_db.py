from app import create_app, db

def init_database():
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        # Import models here to ensure they're registered with SQLAlchemy
        from app.models import User, Password

        # Drop existing tables
        print("Dropping existing tables...")
        db.drop_all()

        # Create new tables
        print("Creating new tables...")
        db.create_all()

        # Verify tables
        print("\nVerifying created tables...")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables created:")
        for table in tables:
            print(f"- {table}")

        print("\nDatabase initialization complete!")

if __name__ == "__main__":
    init_database()