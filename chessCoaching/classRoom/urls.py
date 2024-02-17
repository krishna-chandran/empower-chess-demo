from django.urls import path
from .views import reg_success,home,logout,index,register,login,forgot_password,error_404
from .views import view_users,view_user, edit_user, add_user, delete_user
from .views import view_users,view_course, edit_course, add_course, delete_course
from .views import view_subscriptions,view_courses,view_enrollments,view_assignments,view_userassignments
from .views import view_assignments, view_assignment
# , add_assignment, edit_assignment, delete_assignment


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
    path('user/<int:user_id>/delete/',delete_user, name="delete_user"),

    path('subscriptions/',view_subscriptions,name="view_subscriptions"),

    path('courses/',view_courses,name="view_courses"),
    path('course/<int:course_id>/',view_course, name="view_course"),
    path('course/<int:course_id>/edit/',edit_course, name="edit_course"),
    path('course/add/',add_course, name="add_course"),
    path('course/<int:course_id>/delete/',delete_course, name="delete_course"),

    path('enrollments/',view_enrollments,name="view_enrollments"),

    path('assignments/', view_assignments, name='view_assignments'),
    path('assignment/<int:assignment_id>/', view_assignment, name='view_assignment'),
    # path('assignment/add/', add_assignment, name='add_assignment'),
    # path('assignment/<int:assignment_id>/edit/', edit_assignment, name='edit_assignment'),
    # path('assignment/<int:assignment_id>/delete/', delete_assignment, name='delete_assignment'),

    path('userassignments/',view_userassignments,name="view_userassignments"),
]