from models.bases.object_base import Object


class Building(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'building'
    }

    def get_floors(self):
        return [child for child in self.children if child.type == 'floor']
