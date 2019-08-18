import pytest

from app import restful
from registry.dao import Dao

entities_to_test = ['User',
                    'Patient',
                    'Hospital',
                    'Episode',
                    'Surgery']


@pytest.mark.parametrize('entity_name', entities_to_test)
def test_find(database_session, entity_name):
    dao = Dao.find_dao(database_session, entity_name)
    all = dao.find_all()
    assert len(all) > 0
    for item in all:
        assert item == dao.find_id(item.id)

        new_item = dao.new(entity_name)
        new_item.from_dict(restful.json_loads(restful.json_dumps(item.as_dict())))
        assert new_item.as_dict() == item.as_dict()

@pytest.mark.parametrize('entity_name', ['User', 'Patient', 'Hospital'])
def test_apply_update(database_session, entity_name):
    dao = Dao.find_dao(database_session, entity_name)
    d = dao.find_id(1).as_dict()
    d['name'] = 'Updated -- ' + d['name']
    dao.apply_update(d)

    new_d = dao.find_id(1).as_dict()
    assert new_d['id'] == d['id']
    assert new_d['version_id'] > d['version_id']
    assert new_d['name'] == d['name']
