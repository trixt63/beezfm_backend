from models.bases.object_base import Object


class Building(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'building'
    }

    def get_floors(self):
        return [child for child in self.children if child.type == 'floor']


class Floor(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'building'
    }

    def get_rooms(self):
        return [child for child in self.children if child.type == 'room']

    @property
    def building(self):
        return self.parent


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
