from model.contact import Contact
import re

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
        self.open_contact_to_edit_by_index(index)
        # Edit
        self.fill_contact_form(new_contact_data)
        # Update
        wd.find_element_by_xpath("(//input[@name='update'])[2]").click()
        self.return_to_home()
        self.contact_cache = None

    def modify_contact_by_id(self, id, new_contact_data):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        self.open_contact_to_edit_by_id(id)
        # Edit
        self.fill_contact_form(new_contact_data)
        # Update
        wd.find_element_by_xpath("(//input[@name='update'])[2]").click()
        self.return_to_home()
        self.contact_cache = None

    def test_add_contact_to_group(self, id_contact, id_group):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Select contact
        self.select_contact_by_id(id_contact)
        # Add to group
        wd.find_element_by_name("to_group").click()
        wd.find_element_by_xpath("(//option[@value='%s'])[2]" % id_group).click()
        wd.find_element_by_name("add").click()

    def test_del_contact_from_group(self, id_contact, id_group):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # Select group with contacts
        wd.find_element_by_name("group").click()
        wd.find_element_by_xpath("(//option[@value='%s'])" % id_group).click()
        # Select contact in group
        self.select_contact_by_id(id_contact)
        # Delete from group
        wd.find_element_by_name("remove").click()

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

    def delete_contact_by_id(self, id):
        wd = self.app.wd
        # Open home page - all contacts
        self.return_to_home()
        # select first contact
        self.select_contact_by_id(id)
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

    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[id='%s']" % id).click()

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("address", contact.address)
        self.change_field_value("home", contact.homephone)
        self.change_field_value("mobile", contact.mobilephone)
        self.change_field_value("work", contact.workphone)
        self.change_field_value("phone2", contact.secondaryphone)
        self.change_field_value("email", contact.email1)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("email3", contact.email3)

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
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                lastname = cells[1].text
                firstname = cells[2].text
                address = cells[3].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("value")
                all_emails = cells[4].text
                all_phones = cells[5].text
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, address=address, id=id,
                                                  all_phones_from_home_page=all_phones,
                                                  all_emails_from_home_page=all_emails))
        return list(self.contact_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        address = wd.find_element_by_name("address").text
        id = wd.find_element_by_name("id").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")
        email1 = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Contact(firstname=firstname, lastname=lastname,
                       address=address,
                       email1=email1, email2=email2, email3=email3,
                       homephone=homephone, workphone=workphone,
                       mobilephone=mobilephone,
                       secondaryphone=secondaryphone, id=id)

    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_to_edit_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_xpath(f"//*[@href='edit.php?id={id}']").click()

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        return Contact(homephone=homephone, workphone=workphone,
                       mobilephone=mobilephone,
                       secondaryphone=secondaryphone)
