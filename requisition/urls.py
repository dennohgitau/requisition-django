from django.urls import path
from . import views
from .views import RequisitionTemplateView, ManageRequisitionTemplateView, AdminManageRequisitionTemplateView,ViewRequisitionTemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.home, name="home"),
    path('user_login', views.user_login, name="user_login"),
    path("apply", login_required(RequisitionTemplateView.as_view(), login_url='user_login'), name="apply"),
    path("manage", login_required(ManageRequisitionTemplateView.as_view(), login_url='user_login'), name="manage"),
    path("admin_manage", login_required(AdminManageRequisitionTemplateView.as_view(), login_url='user_login'), name="admin_manage"),
    path('logout', views.log_out, name='logout'),
    path('requisitions_view', login_required(ViewRequisitionTemplateView.as_view(), login_url='user_login'), name="requisitions_view"),
    path('all_requisitions', views.all_requisitions, name="all_requisitions"),
]