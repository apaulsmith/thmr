class Dao:
    def __init__(self, session, entity):
        self.session = session
        self.entity = entity

    def all(self):
        return self.session.query(self.entity).all()

    def first(self):
        return self.session.query(self.entity).first()

    def id(self, id):
        items = self.session.query(self.entity).filter(self.entity.id == id).all()
        if len(items) > 1:
            raise ValueError('Found multiple entities for id {}!'.format(id))

        return items[0]
