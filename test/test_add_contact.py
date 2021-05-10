# -*- coding: utf-8 -*-
from model.contact import Contact


def test_add_contact(app):
    app.contact.create(Contact(firstname="Lisa", lastname="Solovey", address="Eniseyskay street", email1="elizavetasolovey@mail.ru",
                               email2="elizaveta.solovey@x5.ru", mobile="+79169928939"))
