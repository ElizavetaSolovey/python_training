def test_add_contact_to_default_group(app):
    app.session.login(username="admin", password="secret")
    app.contact.test_add_contact_to_default_group()
    app.session.logout()