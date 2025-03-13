from models.bases.object_base import Object


class Device(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'device'
    }

    @property
    def room(self):
        return self.parent

    @property
    def floor(self):
        if self.parent:
            return self.parent.parent
        return None

    @property
    def building(self):
        if self.parent and self.parent.parent:
            return self.parent.parent.parent
        return None
