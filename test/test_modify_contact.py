from model.contact import Contact


def test_modify_first_contact(app):
    if app.contact.count() == 0:
        app.contact.create(Contact(firstname="test", lastname="test", email1="test"))
    app.contact.modify_first_contact(Contact(firstname="Elizaveta"))
