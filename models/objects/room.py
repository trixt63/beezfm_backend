from models.bases.object_base import Object


class Room(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'room'
    }

    def get_devices(self):
        return [child for child in self.children if child.type == 'device']

    @property
    def floor(self):
        return self.parent

    @property
    def building(self):
        if self.parent:
            return self.parent.parent
        return None
