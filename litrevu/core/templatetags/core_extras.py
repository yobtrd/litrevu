from django import template
from django.utils.safestring import mark_safe

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


@register.simple_tag
def alert_info(message, css=None):
    return mark_safe(
        f"""
        <div class="alert alert-info bg-taupe-50 {css}">
            <svg id="icon-info"
                 xmlns="http://www.w3.org/2000/svg"
                 fill="none"
                 viewBox="0 0 24 24"
                 class="h-6 w-6 shrink-0 stroke-current"
                 aria-label="icon-info">
                <path stroke-linecap="round" stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>{message}</span>
        </div>
        """
    )
