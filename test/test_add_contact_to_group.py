from model.group import Group
import random
import pytest
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
    contacts = dbORM.get_contact_list()
    groups = dbORM.get_group_list()
    gr = random.choice(groups)
    c = random.choice(contacts)
    old = dbORM.get_contacts_in_group(Group(id=gr.id))
    if len(old) == 0:
        app.contact.test_add_contact_to_group(c.id, gr.id)
        new = dbORM.get_contacts_in_group(Group(id=gr.id))
        old.append(c)
        assert sorted(new, key=Group.id_or_max) == sorted(old, key=Group.id_or_max)
    else:
        for i in range(len(old)):
            if old[i].id != c.id:
                app.contact.test_add_contact_to_group(c.id, gr.id)
                new = dbORM.get_contacts_in_group(Group(id=gr.id))
                old.append(c)
                assert sorted(new, key=Group.id_or_max) == sorted(old, key=Group.id_or_max)
