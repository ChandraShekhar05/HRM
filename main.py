import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


# Base Page
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def click_element(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def send_keys_to_element(self, by_locator, text):
        self.wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def get_element_text(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator)).text

    def is_element_visible(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def hover_over_element(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        ActionChains(self.driver).move_to_element(element).perform()


# Login Page
class LoginPage(BasePage):
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def login(self, username, password):
        self.send_keys_to_element(self.USERNAME_INPUT, username)
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)


# Dashboard Page
class DashboardPage(BasePage):
    DASHBOARD_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    LOGOUT_OPTION = (By.XPATH, "//a[contains(text(), 'Logout')]")

    def is_dashboard_displayed(self):
        return self.is_element_visible(self.DASHBOARD_TITLE)

    def navigate_to_pim(self):
        self.click_element(self.PIM_MENU)

    def logout(self):
        self.click_element(self.USER_DROPDOWN)
        self.click_element(self.LOGOUT_OPTION)


# PIM Page
class PIMPage(BasePage):
    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[contains(., 'Add')]")
    EMPLOYEE_LIST_MENU = (By.XPATH, "//a[contains(@class, 'oxd-topbar-body-nav-tab-item') and contains(., 'Employee List')]")

    def click_add_employee(self):
        time.sleep(1)
        self.click_element(self.ADD_EMPLOYEE_BUTTON)

    def navigate_to_employee_list(self):
        self.click_element(self.EMPLOYEE_LIST_MENU)


# Add Employee Page
class AddEmployeePage(BasePage):
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    CREATE_LOGIN_TOGGLE = (By.XPATH, "//span[contains(text(), 'Create Login Details')]/../span")
    USERNAME_INPUT = (By.XPATH, "//label[contains(text(), 'Username')]/following::div[1]/input")
    PASSWORD_INPUT = (By.XPATH, "//label[contains(text(), 'Password')]/following::div[1]/input")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[contains(text(), 'Confirm Password')]/following::div[1]/input")
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Save')]")

    def add_employee(self, first_name, middle_name, last_name, create_login=False, username=None, password=None):
        self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        self.send_keys_to_element(self.MIDDLE_NAME_INPUT, middle_name)
        self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)

        if create_login:
            self.click_element(self.CREATE_LOGIN_TOGGLE)
            self.send_keys_to_element(self.USERNAME_INPUT, username)
            self.send_keys_to_element(self.PASSWORD_INPUT, password)
            self.send_keys_to_element(self.CONFIRM_PASSWORD_INPUT, password)

        self.click_element(self.SAVE_BUTTON)


# Employee List Page
class EmployeeListPage(BasePage):
    SEARCH_NAME_INPUT = (By.XPATH, "//label[contains(text(), 'Employee Name')]/following::div[1]/div/input")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(., 'Search')]")
    EMPLOYEE_LIST = (By.XPATH, "//div[@class='oxd-table-body']/div")
    EMPLOYEE_NAME_CELL = (By.XPATH, ".//div[contains(@class, 'oxd-table-cell')][3]/div")

    def search_employee(self, employee_name):
        self.send_keys_to_element(self.SEARCH_NAME_INPUT, employee_name)
        self.click_element(self.SEARCH_BUTTON)

    def verify_employees_in_list(self, employee_names):
        time.sleep(3)
        employees = self.driver.find_elements(By.XPATH, "//div[@class='oxd-table-body']/div")
        verified_names = []

        for employee in employees:
            try:
                name_cell = employee.find_element(*self.EMPLOYEE_NAME_CELL)
                employee_name = name_cell.text
                for target_name in employee_names:
                    if target_name in employee_name and target_name not in verified_names:
                        print(f"Name Verified: {employee_name}")
                        verified_names.append(target_name)
                        break
            except:
                continue

        return len(verified_names) == len(employee_names)


# Test Runner
class OrangeHRMTest:
    def __init__(self):
        # Automatically install the right ChromeDriver for your Chrome version
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

        self.employees = [
            {"first_name": "John", "middle_name": "A", "last_name": "Doe"},
            {"first_name": "Jane", "middle_name": "B", "last_name": "Smith"},
            {"first_name": "Robert", "middle_name": "C", "last_name": "Johnson"},
            {"first_name": "Emily", "middle_name": "D", "last_name": "Williams"}
        ]

    def run_test(self):
        try:
            print("Step 1: Logging in...")
            login_page = LoginPage(self.driver)
            login_page.login("Admin", "admin123")

            dashboard_page = DashboardPage(self.driver)
            assert dashboard_page.is_dashboard_displayed(), "Login failed"
            print("Login successful")

            print("Step 2: Navigating to PIM module...")
            dashboard_page.navigate_to_pim()
            pim_page = PIMPage(self.driver)

            print("Step 3: Adding employees...")
            added_employees = []

            for employee in self.employees:
                pim_page.click_add_employee()
                add_employee_page = AddEmployeePage(self.driver)

                username = f"{employee['first_name'].lower()}{random.randint(1000, 9999)}"
                password = "Password123!"

                add_employee_page.add_employee(
                    employee["first_name"],
                    employee["middle_name"],
                    employee["last_name"],
                    create_login=True,
                    username=username,
                    password=password
                )

                full_name = f"{employee['first_name']} {employee['last_name']}"
                added_employees.append(full_name)
                print(f"Added employee: {full_name}")

                dashboard_page.navigate_to_pim()

            print("Step 4: Verifying added employees...")
            pim_page.navigate_to_employee_list()
            employee_list_page = EmployeeListPage(self.driver)
            employee_list_page.click_element(employee_list_page.SEARCH_BUTTON)
            assert employee_list_page.verify_employees_in_list(added_employees), "Employee verification failed"
            print("All employees verified")

            print("Step 5: Logging out...")
            dashboard_page.logout()
            assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Logout failed"
            print("Logout successful. Test passed!")

        except Exception as e:
            print(f"Test failed: {e}")

        finally:
            self.driver.quit()


# Run the script
if __name__ == "__main__":
    test = OrangeHRMTest()
    test.run_test()
