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

### 2. Create a Virtual Environment

It's recommended to create a virtual environment to manage the project's dependencies separately from your global Python environment:

```bash
python3 -m venv testing_env
```

This command creates a new directory named testing_env that contains the virtual environment.

### 3. Activate the Virtual Environment

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

### 4. Install Dependencies

Install the project's dependencies using pip and the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

This command installs all the necessary Python packages, including Selenium, Pytest, and WebDriver Manager.

### 5. Running Tests

To run the tests, use the pytest command from the root directory of the project:

```bash
pytest
```

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
├── **init**.py
├── README.md
├── requirements.txt
├── test_cases
└── test_utils.py
```

- conftest.py: Contains shared fixture functions for setting up and tearing down tests.
- test_cases: Contains the test cases for various features.
- test_utils.py: Contains utility functions for test setup and data management.
- requirements.txt: Lists the Python packages required for the tests.
