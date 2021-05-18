# -*- coding: utf-8 -*-
from model.contact import Contact


def test_add_contact(app):

    old_contacts = app.contact.get_contact_list()
    contact = Contact(firstname="Lis", lastname="Solo", address="Enis", email1="el@mail.ru",
                               email2="el@x5.ru", mobile="+79169928939")
    app.contact.create(contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
