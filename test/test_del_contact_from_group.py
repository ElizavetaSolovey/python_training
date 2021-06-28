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
def test_del_contact_from_group(app, group, contact):
    if len(dbORM.get_contact_list()) == 0:
        app.contact.create(contact)
    if len(dbORM.get_group_list()) == 0:
        app.group.create(group)
    with allure.step('Given a group list'):
        groups = dbORM.get_group_list()
    for i in range(len(dbORM.get_group_list())):
        with allure.step('Given contacts in group list'):
            c = dbORM.get_contacts_in_group(groups[i])
        if len(c) != 0:
            cr = random.choice(c)
            old = dbORM.get_contacts_in_group(Group(id=groups[i].id))
            with allure.step('Delete contact from group list'):
                app.contact.test_del_contact_from_group(cr.id, groups[i].id)
            with allure.step('Compare lists'):
                new = dbORM.get_contacts_in_group(Group(id=groups[i].id))
                old.remove(cr)
                assert sorted(new, key=Group.id_or_max) == sorted(old, key=Group.id_or_max)
