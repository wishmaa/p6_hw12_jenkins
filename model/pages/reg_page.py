from selene import browser, have
from model.users.users import User
from test.conftest import path


class RegPage:
    def __init__(self):
        self.fill_firstname = browser.element("#firstName")
        self.fill_lastname = browser.element("#lastName")
        self.fill_email = browser.element("#userEmail")
        self.fill_gender = browser.all("[name=gender]")
        self.fill_phone = browser.element("#userNumber")
        self.fill_subjects = browser.element("#subjectsInput")
        self.fill_hobby = browser.all('[for^=hobbies-checkbox]')
        self.upload_file = browser.element('#uploadPicture')
        self.fill_currentadress = browser.element("#currentAddress")

    def open(self):
        browser.open('/automation-practice-form')
        browser.element(".practice-form-wrapper").should(have.text("Student Registration Form"))
        browser.driver.execute_script("$('footer').remove()")
        browser.driver.execute_script("$('#fixedban').remove()")
        return self

    def fill_all_form(self, user: User):
        self.fill_firstname.type(user.first_name)
        self.fill_lastname.type(user.last_name)
        self.fill_email.type(user.email)
        self.fill_gender.element_by(have.value(user.gender)).element('..').click()
        self.fill_phone.type(user.phone)
        self.fill_dateofbirth(user.birthday)
        self.fill_subjects.type(user.subjects).press_enter()
        self.fill_hobby.element_by(have.text(user.hobby)).element('..').click()
        self.upload_file.send_keys(path(user.image))
        self.fill_currentadress.type(user.address)
        self.fill_state(user.state)
        self.fill_city(user.city)
        self.submitting()

    def fill_dateofbirth(self, date):
        year = date.year
        month = date.month - 1
        day = date.strftime('%d')
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__year-select').click()
        browser.element(f'.react-datepicker__year-select option[value="{year}"]').click()
        browser.element('.react-datepicker__month-select').click()
        browser.element(f'.react-datepicker__month-select option[value="{month}"]').click()
        browser.element(f'.react-datepicker__day--0{day}').click()
        return self

    def fill_state(self, value):
        browser.element("#state").click()
        browser.all("#state div").element_by(have.exact_text(value)).click()
        return self

    def fill_city(self, value):
        browser.element("#city").click()
        browser.all('[id^=react-select][id*=option]').element_by(have.exact_text(value)).click()
        return self

    def submitting(self):
        browser.element('#submit').click()
        return self

    def should_have_user_information(
            self, user):
        browser.element('.table').all('td').even.should(
            have.exact_texts(
                f'{user.first_name} {user.last_name}',
                f'{user.email}',
                f'{user.gender}',
                f"{user.phone}",
                '{0} {1},{2}'.format(
                    user.birthday.strftime("%d"),
                    user.birthday.strftime("%B"),
                    user.birthday.year),
                f"{user.subjects}",
                f"{user.hobby}",
                f"{user.image}",
                f"{user.address}",
                f"{user.state} {user.city}"
            )
        )
        return self
