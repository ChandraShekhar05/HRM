# 🧪 OrangeHRM Test Automation Framework (Selenium + Python)

This is a Python-based test automation framework for the [OrangeHRM](https://opensource-demo.orangehrmlive.com/) application. It uses **Selenium WebDriver**, **Page Object Model (POM)** design pattern, and **webdriver-manager** to handle ChromeDriver management.

---

## 🚀 Features

- ✅ Login to OrangeHRM
- ✅ Navigate to PIM Module
- ✅ Add new employees with login credentials
- ✅ Verify added employees in the Employee List
- ✅ Logout from the system

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **Automation Tool**: Selenium WebDriver
- **Driver Management**: webdriver-manager
- **Design Pattern**: Page Object Model (POM)

---

## 📁 Project Structure

QA/
│
├── main.py # Main test runner script
├── README.md # Project documentation
├── requirements.txt # List of required packages

markdown
Copy
Edit

> Optionally, you can refactor into:
> ```
> pages/
> ├── base_page.py
> ├── login_page.py
> ├── dashboard_page.py
> ├── pim_page.py
> ├── add_employee_page.py
> ├── employee_list_page.py
> ```

---

## 📦 Installation

1. **Clone the repository or download the code**:

```bash
git clone https://github.com/yourusername/orangehrm-automation.git
cd orangehrm-automation
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is missing, run this instead:

bash
Copy
Edit
pip install selenium webdriver-manager
🧪 Running the Test
To start the automated test:

bash
Copy
Edit
python main.py
It will:

Launch the OrangeHRM login page.

Log in with default credentials (Admin/admin123).

Navigate to the PIM module.

Add 4 employees with random login credentials.

Verify if the employees appear in the Employee List.

Log out and close the browser.

⚙️ Requirements
Google Chrome (v136 or latest)

Python 3.8 or later

Internet connection (to download ChromeDriver dynamically)

❓ Troubleshooting
ChromeDriver Version Error
If you see an error like:

pgsql
Copy
Edit
session not created: This version of ChromeDriver only supports Chrome version 114...
🔧 Fix:

Make sure webdriver-manager is up to date:

bash
Copy
Edit
pip install --upgrade webdriver-manager
Delete cached drivers (optional):

bash
Copy
Edit
# Windows
rmdir /S /Q %USERPROFILE%\.wdm
✅ Credentials Used
Demo credentials used in the OrangeHRM demo:

Username: Admin

Password: admin123

📄 License
This project is for educational and demonstration purposes only. It uses the public OrangeHRM demo site.
