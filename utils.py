import os
import config


def db_exists() -> bool:
    return os.path.exists(config.DB_PATH)


def floorplan_dir_exists() -> bool:
    return os.path.exists(config.FLOORPLAN_IMG_DIR)


def create_floorplan_dir():
    os.mkdir(config.FLOORPLAN_IMG_DIR)


def clean_columns(object_dict, columns):
    for key in list(object_dict):
        if key not in columns:
            object_dict.pop(key)


def instance_exists(instance_id, sa_model) -> bool:
    instance = sa_model.query.get(instance_id)
    return instance is not None and instance.active
