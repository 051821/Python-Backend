AI/ML Project API Platform

Build a backend that manages ML models and datasets. This is perfect for you because you already work with machine learning projects.

Example:
“ML Model Management API”

Users can:

Register / login

Upload datasets

Upload ML models

Run predictions

Track experiment results

This project will make you use all important backend concepts.


# ORM - Object-Relational Mapping
*layers of abstraction between the database and the application code, allowing developers to interact with the database using high-level programming constructs instead of raw SQL queries.*

*Instead of going to pgadin define table and then write sql query to insert data, we can define a class in python and then use that class to insert data into the database. This makes it easier to work with the database and also makes the code more readable.*

FastPi- python - SQLAlchemy - ORM - pgcopg2/sql - database

*SqlAlchemy need daabase driver to connect to the database,  psycopg2 which is a PostgreSQL adapter for Python. It allows us to connect and interact with a PostgreSQL database.*

*For mysql we can use mysql-connector-python or pymysql as the database driver.*

*For ora




Authentication and Authorization
File handling (for datasets and models)
API design and development\

HAsing, Routers, 


JWT Token Authentication
clinet                    API
*To keep track whether user is logged in or logged out*
*Jwt Token is used to authenticate user like login(username, password) verfying credentials is valid sign JWT token*
*Headers: Authorization: Bearer <token>*
*Header(Algorithm and Token Type)-payload(Data)-verifysignature*
![alt text](image.png)

# Hashing is one way
![alt text](image-1.png)

*JWTError is an exception (error class) provided by the python-jose library.It is raised when something goes wrong while decoding or validating a JWT (JSON Web Token).*


# 🔐 OAuth2 with JWT Authentication (FastAPI)

This project demonstrates how to implement authentication using **OAuth2 Password Flow** with **JWT (JSON Web Tokens)** in FastAPI.

---

## 📌 What is OAuth2?

OAuth2 is an **authorization framework** that allows users to access resources without sharing their credentials directly.

- It defines the **flow of authentication**
- It does NOT define token format

---

## 📌 What is JWT?

JWT (JSON Web Token) is a **compact, secure token format** used to transmit user information.

### Structure:
HEADER.PAYLOAD.SIGNATURE

Example:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...


---

## 🔗 OAuth2 + JWT

- OAuth2 → Defines authentication flow
- JWT → Used as access token

👉 Together: Secure authentication system

---

## 🔁 Authentication Flow

1. User sends **username & password**
2. Server verifies credentials
3. Server generates JWT token
4. Token is sent to client
5. Client sends token in headers
6. Server verifies token
7. Access is granted

---

## 📥 Request Example


POST /login
{
"username": "user",
"password": "password"
}


---

## 📤 Response Example


{
"access_token": "your_jwt_token",
"token_type": "bearer"
}


---

## 🔑 Using Token

Include token in request headers:


Authorization: Bearer <your_token>


---

## ⚙️ Implementation (FastAPI)

### 1. OAuth2 Setup
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
2. Create Token
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
3. Verify Token
def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
4. Protect Routes
@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Authorized"}
🧠 Key Concepts
Bearer Token → Token used in Authorization header
Stateless Auth → No session stored on server
Claims → Data inside JWT (e.g., user_id, exp)

Example payload:

{
  "user_id": 1,
  "exp": 1712345678
}
⚠️ Common Mistakes
Not adding token expiry (exp)
Not verifying algorithm
Exposing sensitive data in JWT
Not handling token errors
Missing "Bearer" in headers

🆚 OAuth2 vs JWT
Feature	       |         OAuth2	        |    JWT
Type	       |        Framework	    |   Token
Purpose	       |        Auth flow	    |   Data transfer
Usage	       |       Defines process	|   Carries data
🚀 Summary

OAuth2 handles authentication flow, while JWT securely stores and transmits user data. Together, they provide a scalable and stateless authentication system.

📚 Tech Stack
FastAPI
Python
python-jose (JWT)
OAuth2PasswordBearer


#### Common Algorithms in JWT

1️⃣ HS256 (HMAC + SHA-256)
Type: Symmetric
Same secret key used for both encoding & decoding
jwt.encode(payload, SECRET_KEY, algorithm="HS256")

👉 Most commonly used in FastAPI projects

2️⃣ RS256 (RSA Signature)
Type: Asymmetric
Uses:
Private key → sign token
Public key → verify token

👉 More secure for large systems (microservices, external APIs)

3️⃣ ES256 (ECDSA)
Based on elliptic curve cryptography
Faster & more secure but less commonly used
🧠 How Algorithm Works in JWT

When you create a token:

HEADER + PAYLOAD → SIGNED using ALGORITHM → SIGNATURE

So final JWT:
The payload is the middle part of a JWT that contains the actual data (claims) about the user.
HEADER.PAYLOAD.SIGNATURE
🔍 Example Header
{
  "alg": "HS256",
  "typ": "JWT"
}

👉 "alg" tells which algorithm is used

⚙️ In Your Code
ALGORITHM = "HS256"
jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
⚠️ Important Security Notes

Always specify algorithm while decoding

jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
Never trust token without verification
Keep SECRET_KEY secure


*join post and writer tables*

SELECT * 
FROM posts 
LEFT JOIN writer ON posts.user_id = writer.id

select writers.id,Count(*) from posts LEFT JOIN writers on posts.user_id = writers.id  group by writers.id



## Alembic- data base migration tool
## DATABASE MIGRATION

**Allow to track and rollback easily withof database schemas
Alembic can automatically generate migration scripts based on changes to your database structure**

TO setup alembic
1. create Alembic directory *alembic init dir_name*
2. connect to base import base from ur file and set target = base in env file of alembic dir*
3. in alembic ini file set sqlalchemy.url = "postgresql://user:password@localhost:5432/db_name"*
4.*alembic revision -m "first migration"*
5.*alembic upgrade head*
6. in alembic version 
alembic revision -m "create table"
def upgrade() -> None:
this is for upgrading schema
    """Upgrade schema."""
    pass

for rolling back
def downgrade() -> None:
    """Downgrade schema."""
    pass
rum in terminal *alemic upgrade revno or head*
run in terminal *alembic downgrade revno or head* 
for roll bck
alembic downgrade -1 for rolling back 1 time
alembic downgrade -2 for rolling back 2 times and so on


##CORS handling - cross origin resource sharing

