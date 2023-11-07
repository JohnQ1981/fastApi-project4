from database import Base, engine
from models import Users, Todos  # Ensure this points to your models file

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Reset complete.")

if __name__ == "__main__":
    reset_database()
