from model.group import Group
import random
import pytest
import allure
from data.groups import testdata as group
from data.contacts import testdata as contact
from fixture.orm import ORMFixture
dbORM = ORMFixture(host ="127.0.0.1", name = "addressbook", user = "root", password = "")


@pytest.mark.parametrize("group", group, ids=[repr(x) for x in group])
@pytest.mark.parametrize("contact", contact, ids=[repr(x) for x in contact])
def test_add_contact_to_group(app, group, contact):
    if len(dbORM.get_contact_list()) == 0:
        app.contact.create(contact)
    if len(dbORM.get_group_list()) == 0:
        app.group.create(group)
    with allure.step('Given a contact list'):
        contacts = dbORM.get_contact_list()
    with allure.step('Given a group list'):
        groups = dbORM.get_group_list()
    with allure.step('Choose a group'):
        gr = random.choice(groups)
    with allure.step('Choose a contact'):
        c = random.choice(contacts)
    old = dbORM.get_contacts_in_group(Group(id=gr.id))
    if len(old) == 0:
        with allure.step('When I add a contact %s to the group %s' % c.id % gr.id):
            app.contact.test_add_contact_to_group(c.id, gr.id)
        with allure.step('Compare lists'):
            new = dbORM.get_contacts_in_group(Group(id=gr.id))
            old.append(c)
            assert sorted(new, key=Group.id_or_max) == sorted(old, key=Group.id_or_max)
    else:
        for i in range(len(old)):
            if old[i].id != c.id:
                with allure.step('When I add a contact %s to the group %s' % c.id % gr.id):
                    app.contact.test_add_contact_to_group(c.id, gr.id)
                with allure.step('Compare lists'):
                    new = dbORM.get_contacts_in_group(Group(id=gr.id))
                    old.append(c)
                    assert sorted(new, key=Group.id_or_max) == sorted(old, key=Group.id_or_max)
