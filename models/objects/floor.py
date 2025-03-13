from models.bases.object_base import Object


class Floor(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'building'
    }

    def get_rooms(self):
        return [child for child in self.children if child.type == 'room']

    @property
    def building(self):
        return self.parent
