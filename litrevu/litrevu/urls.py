from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

import core.views
import accounts.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', core.views.home, name='home'),
    path('posts/', core.views.posts, name='posts'),
    path('signup/', accounts.views.signup, name='signup'),
    path('', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('ticket/create/', core.views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/change/', core.views.change_ticket, name='change_ticket'),
    path('ticket/<int:ticket_id>/delete/', core.views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/review/create/', core.views.create_review, name='create_review'),
    path('ticket/<int:ticket_id>/review/<int:review_id>/change/', core.views.change_review, name='change_review'),
    path('ticket/<int:ticket_id>/review/<int:review_id>/delete/', core.views.delete_review, name='delete_review'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
