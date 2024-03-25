# test_utils.py


import requests
import psycopg2
from bs4 import BeautifulSoup



def setup_test_user(i=0):
    url = "http://localhost:8080/api/v1/signup" 
    user_data = {
        "firstName": "User_" + str(i),
        "lastName": "Lastname_" + str(i),
        "userName": "testuser_" + str(i),
        "email": "test."+str(i)+"@example.com",
        "password": "1234",
        "dateOfBirth": "2000-01-01"
    }
    response = requests.post(url, json=user_data)
    if response.status_code != 200:
        raise Exception("Failed to create test user", response.content)
    return user_data


def confirm_email():
    # Get all emails
    response = requests.get('http://localhost:1080/email')
    if response.status_code != 200:
        raise Exception("Failed to fetch emails")

    emails = response.json()

    # Find the confirmation email (assuming it's the latest email)
    confirmation_email = emails[-1]

    confirmation_link = parse_confirmation_link(confirmation_email['html'])

    response = requests.get(confirmation_link)
    if response.status_code != 200:
        raise Exception("Failed to confirm email")

def parse_confirmation_link(raw_email):
    soup = BeautifulSoup(raw_email, 'html.parser')
    link = soup.find('a')['href']

    return link

def teardown_test_user(i=0):
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="connect",
        user="postgres",
        password="connect",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = '"+"test."+str(i)+"@example.com';")
    user_id = cur.fetchone()[0]

    cur.execute("DELETE FROM token WHERE user_id = %s;", (user_id,))

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))

    conn.commit()

    cur.close()
    conn.close()