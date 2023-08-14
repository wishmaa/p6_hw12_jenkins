import datetime
from model.pages.reg_page import RegPage
from model.users.users import User
import allure


@allure.title("Fill form")
def test_fill_form(setup_browser):
    # Open registration form
    reg_page = RegPage()

    Newreguser = User(
        first_name='petr',
        last_name='Lastname',
        email='testnew@mail.ru',
        gender='Male',
        phone='1234567890',
        birthday=datetime.date(1991, 2, 10),
        subjects='Computer Science',
        hobby='Music',
        image='image.png',
        address='Ulitsa',
        state='NCR',
        city='Delhi'
    )

    with allure.step('Open browser'):
        reg_page.open()

    with allure.step('Fill form'):
        reg_page.fill_all_form(Newreguser)

    with allure.step('Check registration'):
        reg_page.should_have_user_information(Newreguser)
