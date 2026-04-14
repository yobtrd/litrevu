from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_display(context, user):
    if user == context["user"]:
        return "Vous avez"
    return f"{user.username} a"


@register.simple_tag(takes_context=True)
def get_pronoun_display(context, ticket):
    if ticket.user == context["user"]:
        return "votre"
    return "un"


@register.simple_tag(takes_context=True)
def get_username_display(context, user):
    if user == context["user"]:
        return "vous"
    return user.username
