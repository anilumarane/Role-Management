from django.urls import path

from . import views
from .AccountViews import question
from .views import Role
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('role_create', Role.as_view(), ),
    path('signup', views.signup),
    path('login', views.user_login, name='login'),

    # system access paths
    path('get_user_access_detail/<int:access_id>', views.get_user_access_detail),
    path('update_user_access/<int:access_id>', views.update_user_access),


    # question
    path('get_questions', question.get_questions),
    path('get_question', question.get_question),
    path('update_role', question.update_question),
    path('create_question', question.create_question),
    path('delete_role', question.delete_question),
]
