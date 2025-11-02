from .fields import Field


class BoundField:
    def __init__(self, form, name, field):
        self.form = form
        self.name = name
        self.label = field.label
        self.validators = list(field.validators)
        self.data = ""
        self.errors = []


class FormMeta(type):
    def __new__(mcls, name, bases, attrs):
        unbound_fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                unbound_fields[key] = value
                attrs.pop(key)
        cls = super().__new__(mcls, name, bases, attrs)
        cls._unbound_fields = {}
        for base in reversed(bases):
            if hasattr(base, "_unbound_fields"):
                cls._unbound_fields.update(base._unbound_fields)
        cls._unbound_fields.update(unbound_fields)
        return cls


class Form(metaclass=FormMeta):
    def __init__(self, formdata=None, data=None):
        values = {}
        if formdata:
            values.update(formdata)
        if data:
            values.update(data)

        self._fields = {}
        for name, field in self._unbound_fields.items():
            bound = BoundField(self, name, field)
            bound.data = values.get(name, "")
            self._fields[name] = bound
            setattr(self, name, bound)

    def validate(self):
        is_valid = True
        for field in self._fields.values():
            field.errors = []
            for validator in field.validators:
                try:
                    validator(self, field)
                except ValueError as exc:
                    field.errors.append(str(exc))
                    is_valid = False
        return is_valid
