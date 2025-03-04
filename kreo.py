
import streamlit as st
import requests
import psycopg
import json

# Supabase Credentials
SUPABASE_URL = "https://ddjglolzfgrnegkmpyfw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkamdsb2x6ZmdybmVna21weWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MTk0OTUsImV4cCI6MjA1NjQ5NTQ5NX0.W2wrjgXSBlGWOAbmfresB8pLqnQgZhe9TeKAXcK8CwI"
META_API_TOKEN = "4d8dd0f8-75e6-488e-8981-f6853746c98f"

# Connect to Supabase PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="your_password_here",
        host="db.ddjglolzfgrnegkmpyfw.supabase.co",
        port="5432"
    )

# Fetch FAQ from the database
def get_faq(question):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT faq_id, tags, related_product_id FROM faq_table WHERE tags ILIKE %s", (f"%{question}%",))
    faq = cursor.fetchone()
    conn.close()
    return faq

# Fetch product info
def get_product_info(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, category, features FROM product_table WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

# Fetch chatbot response format
def get_response_format():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT response_template, response_type FROM chatbot_format_table")
    format_data = cursor.fetchone()
    conn.close()
    return format_data

# Generate response from Meta API
def generate_response(user_input):
    headers = {"Authorization": f"Bearer {META_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"prompt": user_input, "max_tokens": 100}
    response = requests.post("https://api.meta.com/generate", headers=headers, json=payload)
    return response.json().get("text", "Sorry, I couldn't generate a response.")

# Streamlit UI
st.title("KREO Chatbot")
user_input = st.text_input("Ask me anything about KREO products:")

if st.button("Send"):
    if user_input:
        faq_data = get_faq(user_input)
        
        if faq_data:
            response_template, response_type = get_response_format()
            formatted_response = response_template.replace("{question}", user_input)
            
            if response_type == "Product Recommendation" and faq_data[2]:
                product_info = get_product_info(faq_data[2])
                formatted_response += f"\nProduct: {product_info[0]}\nCategory: {product_info[1]}\nFeatures: {product_info[2]}"
                
            st.write(formatted_response)
        else:
            response = generate_response(user_input)
            st.write(response)
    else:
        st.warning("Please enter a question.")
import streamlit as st
import requests
import psycopg2
import json

# Supabase Credentials
SUPABASE_URL = "https://ddjglolzfgrnegkmpyfw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkamdsb2x6ZmdybmVna21weWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MTk0OTUsImV4cCI6MjA1NjQ5NTQ5NX0.W2wrjgXSBlGWOAbmfresB8pLqnQgZhe9TeKAXcK8CwI"
META_API_TOKEN = "4d8dd0f8-75e6-488e-8981-f6853746c98f"

# Connect to Supabase PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="your_password_here",
        host="db.ddjglolzfgrnegkmpyfw.supabase.co",
        port="5432"
    )

# Fetch FAQ from the database
def get_faq(question):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT faq_id, tags, related_product_id FROM faq_table WHERE tags ILIKE %s", (f"%{question}%",))
    faq = cursor.fetchone()
    conn.close()
    return faq

# Fetch product info
def get_product_info(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, category, features FROM product_table WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

# Fetch chatbot response format
def get_response_format():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT response_template, response_type FROM chatbot_format_table")
    format_data = cursor.fetchone()
    conn.close()
    return format_data

# Generate response from Meta API
def generate_response(user_input):
    headers = {"Authorization": f"Bearer {META_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"prompt": user_input, "max_tokens": 100}
    response = requests.post("https://api.meta.com/generate", headers=headers, json=payload)
    return response.json().get("text", "Sorry, I couldn't generate a response.")

# Streamlit UI
st.title("KREO Chatbot")
user_input = st.text_input("Ask me anything about KREO products:")

if st.button("Send"):
    if user_input:
        faq_data = get_faq(user_input)
        
        if faq_data:
            response_template, response_type = get_response_format()
            formatted_response = response_template.replace("{question}", user_input)
            
            if response_type == "Product Recommendation" and faq_data[2]:
                product_info = get_product_info(faq_data[2])
                formatted_response += f"\nProduct: {product_info[0]}\nCategory: {product_info[1]}\nFeatures: {product_info[2]}"
                
            st.write(formatted_response)
        else:
            response = generate_response(user_input)
            st.write(response)
    else:
        st.warning("Please enter a question.")
