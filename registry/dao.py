class Dao:
    def __init__(self, session, entity):
        self.session = session
        self.entity = entity

    @staticmethod
    def find_entity_class(entity_name):
        entity_class = getattr(__import__('registry.schema', fromlist=['schema']), entity_name)
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
