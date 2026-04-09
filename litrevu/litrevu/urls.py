import accounts.views
import core.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("feed/", core.views.feed, name="feed"),
    path("posts/", core.views.posts, name="posts"),
    path("signup/", accounts.views.signup, name="signup"),
    path(
        "",
        accounts.views.CustomLoginView.as_view(
            template_name="accounts/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="feed"), name="logout"),
    path("ticket/create/", core.views.create_ticket, name="create_ticket"),
    path(
        "ticket/<int:ticket_id>/change/", core.views.change_ticket, name="change_ticket"
    ),
    path(
        "ticket/<int:ticket_id>/delete/", core.views.delete_ticket, name="delete_ticket"
    ),
    path(
        "ticket/<int:ticket_id>/review/create/",
        core.views.create_review,
        name="create_review",
    ),
    path(
        "ticket/<int:ticket_id>/review/<int:review_id>/change/",
        core.views.change_review,
        name="change_review",
    ),
    path(
        "ticket/<int:ticket_id>/review/<int:review_id>/delete/",
        core.views.delete_review,
        name="delete_review",
    ),
    path(
        "ticket/create_ticket_review/",
        core.views.create_ticket_and_review,
        name="create_ticket_review",
    ),
    path("follow/", core.views.follow_user, name="follow"),
    path(
        "follow/<int:follows_id>/unfollow/", core.views.unfollow_user, name="unfollow"
    ),
    path("block/<int:user_id>/", core.views.block_user, name="block"),
    path("block/<int:block_id>/unblock", core.views.unblock_user, name="unblock"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
