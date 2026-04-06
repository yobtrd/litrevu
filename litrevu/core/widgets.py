class FormWidgetMixin:
    """
    Generic form styling mixin that standardizes field attributes.

    Automatically transforms labels into placeholders, removes visual labels,
    adds ARIA labels for accessibility, and handles password field masking.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "title": "Veuillez remplir ce champ",
                    "aria-label": field.label,
                    "placeholder": field.label,
                }
            )
            if "password" in name:
                field.widget.input_type = "password"
            field.label = ""
            field.help_text = None
