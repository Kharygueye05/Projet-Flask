from app.data import load_data, save_data

DEFINITIONS_FILE = 'course_definitions.json'

def _load_definitions():
    return load_data(DEFINITIONS_FILE)

def _save_definitions(definitions):
    save_data(DEFINITIONS_FILE, definitions)

def add_definition(title, teacher_id, class_id, description=''):
    definitions = _load_definitions()
    new_id = max([d['id'] for d in definitions], default=0) + 1
    definition = {
        'id': new_id,
        'title': title,
        'teacher_id': teacher_id,
        'class_id': class_id,
        'description': description
    }
    definitions.append(definition)
    _save_definitions(definitions)
    return definition

def update_definition(definition_id, title=None, teacher_id=None, class_id=None, description=None):
    definitions = _load_definitions()
    for d in definitions:
        if d['id'] == definition_id:
            if title is not None:
                d['title'] = title
            if teacher_id is not None:
                d['teacher_id'] = teacher_id
            if class_id is not None:
                d['class_id'] = class_id
            if description is not None:
                d['description'] = description
            _save_definitions(definitions)
            return d
    return None

def delete_definition(definition_id):
    definitions = _load_definitions()
    definitions = [d for d in definitions if d['id'] != definition_id]
    _save_definitions(definitions)

def get_definition_by_id(definition_id):
    definitions = _load_definitions()
    for d in definitions:
        if d['id'] == definition_id:
            return d
    return None

def list_definitions():
    return _load_definitions()