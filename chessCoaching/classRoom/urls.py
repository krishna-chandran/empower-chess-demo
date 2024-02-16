from django.urls import path
from .views import reg_success,home,logout,index,register,login,forgot_password,error_404
from .views import view_users,view_user, edit_user, add_user
from .views import view_subscriptions,view_courses,view_enrollments,view_assignments,view_userassignments


urlpatterns = [
    path('registersuccess/',reg_success,name="registerSuccess"),
    path('home/',home,name="home"),
    path('logout/',logout,name="logout"),
    path('',index,name="index"),
    path('register/',register,name="register"),
    path('login/',login,name="login"),
    path('forgot_password/',forgot_password,name="forgot_password"),
    path('error_404/',error_404,name="error_404"),


    path('users/', view_users, name="view_users"),
    path('user/<int:user_id>/',view_user, name="view_user"),
    path('user/<int:user_id>/edit/',edit_user, name="edit_user"),
    path('user/add/',add_user, name="add_user"),

    path('subscriptions/',view_subscriptions,name="view_subscriptions"),

    path('courses/',view_courses,name="view_courses"),

    path('enrollments/',view_enrollments,name="view_enrollments"),

    path('assignments/',view_assignments,name="view_assignments"),

    path('userassignments/',view_userassignments,name="view_userassignments"),
]