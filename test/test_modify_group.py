from model.group import Group
import random
#from random import randrange


def test_modify_group_name(app, db, json_groups, check_ui):
    group = json_groups
    if len(db.get_group_list()) == 0:
        app.group.create(group)
    old_groups = db.get_group_list()
    gr = random.choice(old_groups)
    group.id = gr.id
    old_groups = list(filter(lambda obj: obj.id != gr.id, old_groups))
    app.group.modify_group_by_id(gr.id, group)
    old_groups.append(group)
    new_groups = db.get_group_list()
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)








