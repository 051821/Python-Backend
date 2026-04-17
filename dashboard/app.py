import streamlit as st
import requests

# 🔗 Your deployed FastAPI URL
API_URL = "http://127.0.0.1:8000/"
st.set_page_config(page_title="FastAPI Dashboard", layout="wide")

st.title("🚀 FastAPI Dashboard")

# -------------------------------
# 🔐 LOGIN
# -------------------------------
st.sidebar.subheader("Login")

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    res = requests.post(
        f"{API_URL}/auth/login",
        data={"username": email, "password": password}
    )
    if res.status_code == 200:
        token = res.json()["access_token"]
        st.session_state["token"] = token
        st.success("Logged in successfully!")
    else:
        st.error("Login failed")

# Authorization header
headers = {}
if "token" in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# -------------------------------
# 📌 MENU
# -------------------------------
menu = [
    "View Posts",
    "Get Post by ID",
    "Create Post",
    "Update Post",
    "Delete Post",
    "Vote",
    "Create User"
]

choice = st.sidebar.selectbox("Menu", menu)

# -------------------------------
# 📄 VIEW POSTS
# -------------------------------
if choice == "View Posts":
    st.subheader("All Posts")

    res = requests.get(f"{API_URL}/posts/", headers=headers)
    if res.status_code == 200:
        data = res.json()
        for post in data:
            st.card = st.container()
            with st.card:
                st.markdown(f"### {post['title']}")
                st.write(post["content"])
                st.write(f"👍 Votes: {post.get('votes', 0)}")
                st.write("---")
    else:
        st.error(res.text)

# -------------------------------
# 🔍 GET POST BY ID
# -------------------------------
elif choice == "Get Post by ID":
    st.subheader("Get Post")

    post_id = st.number_input("Post ID", min_value=1)

    if st.button("Fetch"):
        res = requests.get(f"{API_URL}/posts/{post_id}", headers=headers)
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Post not found")

# -------------------------------
# ➕ CREATE POST
# -------------------------------
elif choice == "Create Post":
    st.subheader("Create Post")

    title = st.text_input("Title")
    content = st.text_area("Content")
    published = st.checkbox("Published", value=True)

    if st.button("Create"):
        payload = {
            "title": title,
            "content": content,
            "published": published
        }

        res = requests.post(f"{API_URL}/posts/", json=payload, headers=headers)
        if res.status_code == 201:
            st.success("Post created!")
        else:
            st.error(res.text)

# -------------------------------
# ✏️ UPDATE POST
# -------------------------------
elif choice == "Update Post":
    st.subheader("Update Post")

    post_id = st.number_input("Post ID", min_value=1)
    title = st.text_input("New Title")
    content = st.text_area("New Content")
    published = st.checkbox("Published", value=True)

    if st.button("Update"):
        payload = {
            "title": title,
            "content": content,
            "published": published
        }

        res = requests.put(
            f"{API_URL}/posts/{post_id}",
            json=payload,
            headers=headers
        )

        if res.status_code == 200:
            st.success("Post updated!")
        else:
            st.error(res.text)

# -------------------------------
# ❌ DELETE POST
# -------------------------------
elif choice == "Delete Post":
    st.subheader("Delete Post")

    post_id = st.number_input("Post ID", min_value=1)

    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/posts/{post_id}", headers=headers)

        if res.status_code == 204:
            st.success("Post deleted!")
        else:
            st.error(res.text)

# -------------------------------
# 👍 VOTE
# -------------------------------
elif choice == "Vote":
    st.subheader("Vote on Post")

    post_id = st.number_input("Post ID", min_value=1)
    dir = st.selectbox("Vote", [1, 0])  # 1 = upvote, 0 = remove vote

    if st.button("Submit Vote"):
        payload = {
            "post_id": post_id,
            "dir": dir
        }

        res = requests.post(f"{API_URL}/vote/", json=payload, headers=headers)

        if res.status_code == 201:
            st.success("Vote submitted!")
        else:
            st.error(res.text)

# -------------------------------
# 👤 CREATE USER
# -------------------------------
elif choice == "Create User":
    st.subheader("Create User")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create User"):
        payload = {
            "email": email,
            "password": password
        }

        res = requests.post(f"{API_URL}/users", json=payload)

        if res.status_code == 201:
            st.success("User created!")
        else:
            st.error(res.text)