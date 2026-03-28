#1 main py for crud and postgress
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from fastapi import HTTPException
# psycopg2 is a PostgreSQL adapter for Python, allowing us to connect and interact with a PostgreSQL database.
import psycopg2
# RealDictCursor is a cursor factory that returns query results as dictionaries instead of tuples, making it easier to work with the data.
from psycopg2.extras import RealDictCursor


app = FastAPI()


class User(BaseModel):
    name: str
    college: str
    age: int


# Database connection
try:
    conn = psycopg2.connect(
        host="localhost",
        database="Fastapi",
        user="postgres",
        password="postgres123",
        port=5432,
        cursor_factory=RealDictCursor
    )

    cursor = conn.cursor()
    print("Database connection successful")

except Exception as e:
    print("Database connection failed")
    print(e)


@app.get("/")
def read_root():
    return {"message": "FastAPI + PostgreSQL working"}


# CREATE USER
@app.post("/users/", status_code=HTTP_201_CREATED)
def create_user(user: User):
    try:
        cursor.execute(
            "INSERT INTO users (name, college, age) VALUES (%s, %s, %s) RETURNING id",
            (user.name, user.college, user.age)
        )

        new_user = cursor.fetchone()
        conn.commit()

        return {
            "id": new_user["id"],
            "name": user.name,
            "college": user.college,
            "age": user.age
        }

    except Exception as e:
        print("Error inserting user into database")
        print(e)
        return {"error": "Failed to create user"}


# READ USERS
@app.get("/users/")
def read_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

    except Exception as e:
        print("Error fetching users")
        print(e)
        return {"error": "Failed to fetch users"}



@app.get("/users/{user_id}")
def read_user(user_id: int):
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")   

        return user

    except Exception as e:
        print("Error fetching user")
        print(e)
        return {"error": "Failed to fetch user"}
    

#update user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    try:
        cursor.execute(
            "UPDATE users SET name = %s, college = %s, age = %s WHERE id = %s RETURNING *",
            (user.name, user.college, user.age, user_id)
        )

        updated_user = cursor.fetchone()
        conn.commit()

        if updated_user is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

        return updated_user

    except Exception as e:
        print("Error updating user")
        print(e)
        return {"error": "Failed to update user"}
    


# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        cursor.execute("DELETE FROM users WHERE id = %s RETURNING *", (user_id,))
        deleted_user = cursor.fetchone()
        conn.commit()

        if deleted_user is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

        return {"message": "User deleted successfully"}

    except Exception as e:
        print("Error deleting user")
        print(e)
        return {"error": "Failed to delete user"}