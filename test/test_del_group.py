from model.group import Group
import random
import allure

def test_delete_some_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="test", header="test", footer="test"))
    with allure.step('Given a group list'):
        old_groups = db.get_group_list()
    with allure.step('Choose a group for delete'):
        gr = random.choice(old_groups)
    with allure.step('When I delete a group %s to the list' % gr.id):
        app.group.delete_group_by_id(gr.id)
    with allure.step('Then the new group list is equal to the old list with the deleted group'):
        new_groups = db.get_group_list()
        old_groups.remove(gr)
        assert old_groups == new_groups
        if check_ui:
            assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)

