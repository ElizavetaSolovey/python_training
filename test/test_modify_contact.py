from model.contact import Contact
import random
import allure

def test_modify_some_contact(app, db, json_contacts, check_ui):
    contact = json_contacts
    if len(db.get_contact_list()) == 0:
        app.contact.create(contact)
    with allure.step('Given a contact list'):
        old_contacts = db.get_contact_list()
    with allure.step('Choose a contact for modify'):
        c = random.choice(old_contacts)
        contact.id = c.id
        old_contacts = list(filter(lambda obj: obj.id != c.id, old_contacts))
    with allure.step('When I modify a contact %s to the list' % contact):
        app.contact.modify_contact_by_id(c.id, contact)
        old_contacts.append(contact)
    with allure.step('Then the new contact list is equal to the old list with the modified contact'):
        new_contacts = db.get_contact_list()
        assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
        if check_ui:
            assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
