from model.group import Group
import random
import allure

def test_modify_group_name(app, db, json_groups, check_ui):
    group = json_groups
    if len(db.get_group_list()) == 0:
        app.group.create(group)
    with allure.step('Given a group list'):
        old_groups = db.get_group_list()
    with allure.step('Choose a group for modify'):
        gr = random.choice(old_groups)
        group.id = gr.id
        old_groups = list(filter(lambda obj: obj.id != gr.id, old_groups))
    with allure.step('When I modify a group %s to the list' % group):
        app.group.modify_group_by_id(gr.id, group)
        old_groups.append(group)
    with allure.step('Then the new group list is equal to the old list with the modified group'):
        new_groups = db.get_group_list()
        assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
        if check_ui:
            assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)








