from model.contact import Contact

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
        self.contact_cache = None

    def open_contact_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def return_to_home(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("First name")) > 0):
            wd.find_element_by_link_text("home").click()

    def modify_first_contact(self, new_contact_data):
        self.modify_contact_by_index(0, new_contact_data)

    def modify_contact_by_index(self, index, new_contact_data):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Select contact
        if index == 0:
            a = str("(//img[@alt='Edit'])")
        else:
            a = str("(//img[@alt='Edit'])[") + str(index+1) + str("]")
        # Open edit page
        wd.find_element_by_xpath(a).click()
        # Edit
        self.fill_contact_form(new_contact_data)
        # Update
        wd.find_element_by_xpath("(//input[@name='update'])[2]").click()
        self.return_to_home()
        self.contact_cache = None

    def test_add_contact_to_default_group(self):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Select first contact
        self.select_first_contact()
        # Add to default group
        # Select first group
        wd.find_element_by_name("add").click()

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # select first contact
        self.select_contact_by_index(index)
        # click Delete
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        # Confirm
        wd.switch_to_alert().accept()
        self.return_to_home()
        self.contact_cache = None

    def select_first_contact(self):
        self.select_contact_by_index(0)

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

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

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.return_to_home()
            self.contact_cache = []
            for element in wd.find_elements_by_css_selector("tr[name='entry']"):
                id = element.find_element_by_name("selected[]").get_attribute("value")
                text = element.text
                new_list = text.split()
                last_name = "".join(new_list[0])
                first_name = "".join(new_list[1])
                self.contact_cache.append(Contact(firstname=first_name, lastname=last_name, id=id))
        return list(self.contact_cache)

