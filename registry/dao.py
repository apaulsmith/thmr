class Dao:
    def __init__(self, session, entity):
        self.session = session
        self.entity = entity

    @staticmethod
    def find_entity_class(entity_name):
        entity_class = getattr(__import__('app.models', fromlist=['models']), entity_name)
        return entity_class

    @staticmethod
    def find_dao(session, entity_name: str):
        entity_class = Dao.find_entity_class(entity_name)
        return Dao(session, entity_class)

    @staticmethod
    def new(entity_name: str):
        entity_class = Dao.find_entity_class(entity_name)
        return entity_class()

    def find_all(self):
        return self.session.query(self.entity).all()

    def find_first(self):
        return self.session.query(self.entity).first()

    def find_id(self, id):
        items = self.session.query(self.entity).filter(self.entity.id == id).all()
        if len(items) > 1:
            raise ValueError('Found multiple entities for id {}!'.format(id))

        return items[0]

    def apply_update(self, d: dict):
        entity = self.find_id(d['id'])
        for k, v in d.items():
            if k not in ['id', 'version_id']:
                setattr(entity, k, v)

        return self.session.commit()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def add_all(self, entities):
        self.session.add_all(entities)
        return self.session.commit()
