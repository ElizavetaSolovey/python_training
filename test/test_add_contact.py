# -*- coding: utf-8 -*-
import pytest
from model.contact import Contact
from fixture.application import Application


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_add_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.create(Contact(firstname="Lisa", lastname="Solovey", address="Eniseyskay street", email1="elizavetasolovey@mail.ru",
                               email2="elizaveta.solovey@x5.ru", mobile="+79169928939"))
    app.session.logout()
