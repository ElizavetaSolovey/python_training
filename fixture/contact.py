class ContactHelper:

    def __init__(self, app):
        self.app = app

    def create(self, new_contact_data):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Open contact page
        self.open_contact_page()
        # Fill contact firm
        self.fill_contact_form(new_contact_data)
        # Submit contact creation
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_home()

    def open_contact_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def return_to_home(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("First name")) > 0):
            wd.find_element_by_link_text("home").click()

    def modify_first_contact(self, new_contact_data):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Open edit page
        wd.find_element_by_xpath("//img[@alt='Edit']").click()
        # Edit
        self.fill_contact_form(new_contact_data)
        # Update
        wd.find_element_by_xpath("(//input[@name='update'])[2]").click()
        self.return_to_home()

    def test_add_contact_to_default_group(self):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Select first contact
        wd.find_element_by_name("selected[]").click()
        # Add to default group
        # Select first group
        wd.find_element_by_name("add").click()

    def delete_first_contact(self):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # select first contact
        wd.find_element_by_name("selected[]").click()
        # click Delete
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        # Confirm
        wd.switch_to_alert().accept()
        self.return_to_home()

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("address", contact.address)
        self.change_field_value("email", contact.email1)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("mobile", contact.mobile)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def count(self):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        return len(wd.find_elements_by_name("selected[]"))
