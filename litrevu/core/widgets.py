class FormWidgetMixin:
    """
    Generic form styling mixin that standardizes field attributes.

    Automatically transforms labels into placeholders, handles accessibility
    and password field masking.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "title": "Veuillez remplir ce champ",
                    "placeholder": field.label,
                    "class": "base-field",
                    "tabindex": "0",
                }
            )
            if "password" in field_name:
                field.widget.input_type = "password"
