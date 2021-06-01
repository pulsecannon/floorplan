import json

import config


class BaseModel(config.db.Model):
    __abstract__ = True

    id = config.db.Column(
        config.db.Integer, primary_key=True, autoincrement=True)
    active = config.db.Column(config.db.Boolean, nullable=False, default=True)

    @property
    def columns(self):
        return set(column.name for column in self.__table__.columns)

    def to_dict(self, exclude=()):
        all_columns = self.columns
        columns = all_columns - set(exclude)
        instance_dict = {}
        for column in columns:
            instance_dict[column] = getattr(self, column)
        return instance_dict

    @classmethod
    def from_dict(cls, raw_dict):
        return cls(**raw_dict)

    def to_json(self, exclude=()):
        return json.dumps(
            self.to_dict(exclude), indent=4, sort_keys=True, default=str)


class Project(BaseModel):
    name = config.db.Column(
        config.db.Unicode, unique=True, nullable=False)


class Floorplan(BaseModel):
    name = config.db.Column(config.db.Unicode, nullable=False)
    project_id = config.db.Column(
        config.db.Integer, config.db.ForeignKey('project.id'), nullable=False)
    file_id = config.db.Column(config.db.String, unique=True, nullable=False)

    project = config.db.relationship(
        'Project', backref=config.db.backref('floorplans', lazy='dynamic'))


class Thumb(BaseModel):
    floorplan_id = config.db.Column(
        config.db.Integer, config.db.ForeignKey('floorplan.id'),
        nullable=False)
    thumb_id = config.db.Column(config.db.String, unique=True, nullable=False)

    floorplan = config.db.relationship(
        'Floorplan', backref=config.db.backref('thumbs', lazy='dynamic'))
