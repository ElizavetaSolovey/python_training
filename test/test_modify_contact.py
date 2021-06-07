from model.contact import Contact
import random

def test_modify_some_contact(app, db, json_contacts, check_ui):
    contact = json_contacts
    if len(db.get_contact_list()) == 0:
        app.contact.create(contact)
    old_contacts = db.get_contact_list()
    c = random.choice(old_contacts)
    contact.id = c.id
    old_contacts = list(filter(lambda obj: obj.id != c.id, old_contacts))
    app.contact.modify_contact_by_id(c.id, contact)
    old_contacts.append(contact)
    new_contacts = db.get_contact_list()
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
