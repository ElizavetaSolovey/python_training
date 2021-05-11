from model.contact import Contact

def test_add_contact_to_default_group(app):
    if app.contact.count() == 0:
        app.contact.create(Contact(firstname="test", lastname="test", email1="test"))
    app.contact.test_add_contact_to_default_group()
