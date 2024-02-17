from django.urls import path
from .views import reg_success,home,logout,index,register,login,forgot_password,error_404
from .views import view_users,view_user, edit_user, add_user, delete_user
from .views import view_users,view_course, edit_course, add_course, delete_course,view_courses
from .views import view_subscriptions,view_subscription,add_subscription,edit_subscription
from .views import view_assignments, view_assignment, add_assignment, edit_assignment, delete_assignment
from .views import view_enrollments, view_enrollment, add_enrollment, edit_enrollment,delete_enrollment
from .views import view_userassignments,view_userassignment, add_userassignment,edit_userassignment,delete_userassignment


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
    path('subscription/<int:subscription_id>/', view_subscription, name='view_subscription'),
    path('subscription/add/', add_subscription, name='add_subscription'),
    path('subscription/<int:subscription_id>/edit/', edit_subscription, name='edit_subscription'),  # URL pattern for editing subscriptions

    path('courses/',view_courses,name="view_courses"),
    path('course/<int:course_id>/',view_course, name="view_course"),
    path('course/<int:course_id>/edit/',edit_course, name="edit_course"),
    path('course/add/',add_course, name="add_course"),
    path('course/<int:course_id>/delete/',delete_course, name="delete_course"),

    path('enrollments/',view_enrollments,name="view_enrollments"),
    path('enrollment/<int:enrollment_id>/',view_enrollment,name="view_enrollment"),
    path('enrollment/add/', add_enrollment, name="add_enrollment"),
    path('enrollment/<int:enrollment_id>/edit/',edit_enrollment, name="edit_enrollment"),
    path('enrollment/<int:enrollment_id>/delete/',delete_enrollment, name="delete_enrollment"),

    path('assignments/', view_assignments, name='view_assignments'),
    path('assignment/<int:assignment_id>/', view_assignment, name='view_assignment'),
    path('assignment/add/', add_assignment, name='add_assignment'),
    path('assignment/<int:assignment_id>/edit/', edit_assignment, name='edit_assignment'),
    path('assignment/<int:assignment_id>/delete/', delete_assignment, name='delete_assignment'),

    path('userassignments/',view_userassignments,name="view_userassignments"),
    path('userassignment/<int:user_assignment_id>/', view_userassignment, name='view_userassignment'),
    path('userassignment/add/', add_userassignment, name='add_userassignment'),
    path('userassignment/<int:user_assignment_id>/edit/',edit_userassignment, name='edit_userassignment'),
    path('userassignment/<int:user_assignment_id>/delete/',delete_userassignment, name='delete_userassignment'),

]