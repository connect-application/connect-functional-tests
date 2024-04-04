# Selenium Testing Project for Web Application

This project contains Selenium tests for a React-based web application, focusing on automated testing of the sign-in functionality. The tests are written in Python and use the Pytest framework for test execution.

## Prerequisites

Before you begin, ensure you have Python and pip installed on your system. These tests are developed with Python 3.10, but they should be compatible with Python 3.6 and newer versions.

## Getting Started

To set up your testing environment and run the tests, follow these steps:

### 1. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/connect-application/connect-functional-tests.git

cd connect-functional-tests
```

### 2. Clone the Backend and Frontend Repositories

Clone the backend and frontend code repositories for the application:

- For the backend:

```bash
git clone https://github.com/connect-application/connect.git
```

- For the frontend:

```bash
git clone https://github.com/connect-application/connect-frontend.git
```

### 3. Create a Virtual Environment

It's recommended to create a virtual environment to manage the project's dependencies separately from your global Python environment:

```bash
python3 -m venv testing_env
```

This command creates a new directory named testing_env that contains the virtual environment.

### 4. Activate the Virtual Environment

Activate the virtual environment with the following command:

- On Windows:

```bash
testing_env\Scripts\activate
```

- On macOS and Linux:

```bash
source testing_env/bin/activate
```

You should now see the name of your virtual environment (testing_env) in your terminal prompt, indicating that it is active.

### 5. Install Dependencies

Install the project's dependencies using pip and the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

Additionally, it's necessary to install Maildev for the test environment:

```bash
npm install -g maildev
```

This commands installs all the necessary Python packages, including Selenium, Pytest, and WebDriver Manager, as well as Maildev for email testing.

### 6. Modify 'application.properties' File

Modify the application.properties file in the backend project, located in connect/src/main/resources/application.properties as follows:

![alt text](image.png "properties modifications")

- Uncomment the lines within the red rectangles.
- Comment out the line within the blue rectangle.
- Modify the lines within the orange rectangles as needed.

### 7. Pre-Test Setup

Before executing pytest, ensure the following processes are running:

- The frontend application
- The backend application
- Maildev

These processes must be running concurrently for the tests to function correctly.

### 6. Running Tests

To run the tests, use the pytest command from the root directory of the project:

```bash
pytest
```

To run the tests and generate an HTML report, use the following command:

```bash
pytest --html=report.html --self-contained-html
```

This command runs all the test cases and generates a self-contained HTML report named 'report.html'.

### 6. Deactivating the Virtual Environment

After you're done, you can deactivate the virtual environment by running:

```bash
deactivate
```

This command returns you to your global Python environment.

## Structure

The project's directory structure is as follows:

```markdown
.
├── conftest.py
├── README.md
├── requirements.txt
├── test_cases
└── test_utils.py
```

- conftest.py: Contains shared fixture functions for setting up and tearing down tests.
- test_cases: Contains the test cases for various features.
- test_utils.py: Contains utility functions for test setup and data management.
- requirements.txt: Lists the Python packages required for the tests.
