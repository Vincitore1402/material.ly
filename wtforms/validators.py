class Length:
    def __init__(self, min=0, max=None):
        self.min = min
        self.max = max

    def __call__(self, form, field):
        data = field.data or ""
        length = len(data)

        if self.min is not None and length < self.min:
            message = f"Field must be at least {self.min} characters long."
            raise ValueError(message)

        if self.max is not None and length > self.max:
            message = f"Field cannot be longer than {self.max} characters."
            raise ValueError(message)


class DataRequired:
    def __call__(self, form, field):
        data = field.data
        if data is None or (isinstance(data, str) and not data):
            raise ValueError("This field is required.")


class EqualTo:
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message or f"Field must be equal to {fieldname}."

    def __call__(self, form, field):
        other = getattr(form, self.fieldname, None)
        other_data = getattr(other, "data", None) if other is not None else None
        if field.data != other_data:
            raise ValueError(self.message)
