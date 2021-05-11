from model.contact import Contact


def test_edit_first_contact(app):
    app.contact.edit_first_contact(Contact(firstname="Lisa1", lastname="Solovey1", address="Eniseyskay stree1t", email1="1elizavetasolovey@mail.ru",
                               email2="1elizaveta.solovey@x5.ru", mobile="+79119928939"))