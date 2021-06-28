import re
import random
import allure
from model.contact import Contact


def test_all_info_on_home_page(app):
    with allure.step('Given a contact list from homepage'):
        contact_from_home_page = app.contact.get_contact_list()[0]
    with allure.step('Given a contact list from editpage'):
        contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    with allure.step('Compare contact lists'):
        assert contact_from_home_page.firstname == contact_from_edit_page.firstname
        assert contact_from_home_page.lastname == contact_from_edit_page.lastname
        assert contact_from_home_page.address == contact_from_edit_page.address
        assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)
        assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)


def test_all_info_on_home_page_db(app, db):
    with allure.step('Given a contact list from homepage'):
        contact_from_home_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    with allure.step('Given a contact list from DB'):
        contact_from_db = sorted(db.get_contact_list(), key=Contact.id_or_max)
    with allure.step('Compare contact lists'):
        for i in range(len(db.get_contact_list())):
            assert clear(contact_from_home_page[i].firstname) == clear(contact_from_db[i].firstname)
            assert clear(contact_from_home_page[i].lastname) == clear(contact_from_db[i].lastname)
            assert clear(contact_from_home_page[i].address) == clear(contact_from_db[i].address)
            assert clear(contact_from_home_page[i].all_phones_from_home_page) == clear(merge_phones_like_on_home_page(contact_from_db[i]))
            assert clear(contact_from_home_page[i].all_emails_from_home_page) == clear(merge_emails_like_on_home_page(contact_from_db[i]))


def test_phones_on_contact_view_page(app):
    with allure.step('Given a contact list from viewpage'):
     contact_from_view_page = app.contact.get_contact_from_view_page(0)
    with allure.step('Given a contact list from editpage'):
        contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    with allure.step('Compare contact lists'):
        assert contact_from_view_page.homephone == contact_from_edit_page.homephone
        assert contact_from_view_page.workphone == contact_from_edit_page.workphone
        assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
        assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone


def clear(s):
    return re.sub("[() -]", "", s)


def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x !="",
                                filter(lambda x: x is not None,
                                       [contact.email1, contact.email2, contact.email3])))


def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x !="",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       [contact.homephone, contact.mobilephone, contact.workphone, contact.secondaryphone]))))



