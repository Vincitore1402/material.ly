from forms.forms import ArticleForm, MaterialFormMain, RegisterForm


def test_register_form_validates_with_matching_passwords():
    form = RegisterForm(data={
        "name": "Alice",
        "username": "alice123",
        "email": "alice@example.com",
        "password": "complex-password",
        "confirm": "complex-password",
    })

    assert form.validate() is True


def test_register_form_fails_with_mismatched_passwords():
    form = RegisterForm(data={
        "name": "Alice",
        "username": "alice123",
        "email": "alice@example.com",
        "password": "complex-password",
        "confirm": "different-password",
    })

    assert form.validate() is False
    assert "Passwords do not match" in form.password.errors


def test_article_form_enforces_minimum_body_length():
    form = ArticleForm(data={
        "title": "Title",
        "body": "Too short",
    })

    assert form.validate() is False
    assert any("Field must be at least 40 characters long." in error for error in form.body.errors)


def test_material_form_main_accepts_valid_lengths():
    form = MaterialFormMain(data={
        "classification": "classification",
        "marka": "marka",
        "primenenie": "",
        "dopolnenie": "",
    })

    assert form.validate() is True
