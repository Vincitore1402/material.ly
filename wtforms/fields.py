class Field:
    def __init__(self, label, validators=None):
        self.label = label
        self.validators = list(validators or [])


class StringField(Field):
    pass


class TextAreaField(Field):
    pass


class PasswordField(Field):
    pass
