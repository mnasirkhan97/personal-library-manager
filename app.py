import streamlit as st
import json
import os

FILE = "library.json"

# Load the library
def load_library():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save the library
def save_library(library):
    with open(FILE, "w") as f:
        json.dump(library, f)

# Initialize
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Add Book
def add_book():
    with st.form("Add a Book", clear_on_submit=True):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ["Yes", "No"])
        submitted = st.form_submit_button("Add Book")

        if submitted and title and author:
            st.session_state.library.append({
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": True if read == "Yes" else False
            })
            save_library(st.session_state.library)
            st.success("Book added successfully!")

# Remove Book
def remove_book():
    titles = [book['title'] for book in st.session_state.library]
    if titles:
        selected = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            st.session_state.library = [b for b in st.session_state.library if b["title"] != selected]
            save_library(st.session_state.library)
            st.success("Book removed!")

# Search Book
def search_book():
    keyword = st.text_input("Search by Title or Author").lower()
    if keyword:
        results = [b for b in st.session_state.library if keyword in b["title"].lower() or keyword in b["author"].lower()]
        if results:
            st.write("### Matching Books:")
            for b in results:
                status = "Read" if b["read"] else "Unread"
                st.write(f"- **{b['title']}** by {b['author']} ({b['year']}) - {b['genre']} - {status}")
        else:
            st.info("No matching books found.")

# Display All Books
def display_books():
    if st.session_state.library:
        st.write("### Your Library:")
        for b in st.session_state.library:
            status = "Read" if b["read"] else "Unread"
            st.write(f"- **{b['title']}** by {b['author']} ({b['year']}) - {b['genre']} - {status}")
    else:
        st.info("Library is empty.")

# Display Stats
def display_stats():
    total = len(st.session_state.library)
    read_count = sum(1 for b in st.session_state.library if b["read"])
    if total > 0:
        percent = (read_count / total) * 100
        st.metric("Total Books", total)
        st.metric("Books Read (%)", f"{percent:.1f}%")
    else:
        st.info("No books in library.")

# Sidebar Menu
st.sidebar.title("📚 Library Menu")
option = st.sidebar.radio("Select an action", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Stats"])

# Routes
if option == "Add Book":
    add_book()
elif option == "Remove Book":
    remove_book()
elif option == "Search Book":
    search_book()
elif option == "Display All Books":
    display_books()
elif option == "Display Stats":
    display_stats()
