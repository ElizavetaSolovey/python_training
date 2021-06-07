from model.group import Group
import random


def test_delete_some_group(app, db, json_groups, check_ui):
    group = json_groups
    if len(db.get_group_list()) == 0:
        app.group.create(group)
    old_groups = db.get_group_list()
    gr = random.choice(old_groups)
    app.group.delete_group_by_id(gr.id)
    new_groups = db.get_group_list()
    old_groups.remove(gr)
    assert old_groups == new_groups
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)

