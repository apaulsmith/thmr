from registry.dao import Dao
from registry.schema import Hospitals


def test_hospitals_dao(database_session):
    dao = Dao(session=database_session,
              entity=Hospitals)

    all = dao.all()
    assert len(all) > 0
    for item in all:
        assert item == dao.id(item.id)
