from django.urls import path
from .views import reg_success,home,logout_user,index,register,login,forgot_password,error_404
from .views import view_users,view_user, edit_user, add_user, delete_user
from .views import view_users,view_course, edit_course, add_course, delete_course,view_courses
from .views import view_subscriptions,view_subscription,add_subscription,edit_subscription, delete_subscription
from .views import view_assignments, view_assignment, add_assignment, edit_assignment, delete_assignment
from .views import view_enrollments, view_enrollment, add_enrollment, edit_enrollment,delete_enrollment
from .views import view_userassignments,view_userassignment, add_userassignment,edit_userassignment,delete_userassignment
from .views import view_features, view_feature, add_feature, edit_feature, delete_feature
from .views import view_roles, view_role, add_role, edit_role, delete_role
from .views import view_permissions, view_permission, add_permission
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registersuccess/',reg_success,name="registerSuccess"),
    path('home/',home,name="home"),
    path('logout/',logout_user,name="logout"),
    path('',index,name="index"),
    path('register/',register,name="register"),
    path('accounts/login/', login, name='login'),
    path('error_404/',error_404,name="error_404"),
    
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('users/', view_users, name="view_users"),
    path('user/<int:user_id>/',view_user, name="view_user"),
    path('user/<int:user_id>/edit/',edit_user, name="edit_user"),
    path('user/add/',add_user, name="add_user"),
    path('user/<int:user_id>/delete/',delete_user, name="delete_user"),

    path('subscriptions/',view_subscriptions,name="view_subscriptions"),
    path('subscription/<int:subscription_id>/', view_subscription, name='view_subscription'),
    path('subscription/add/', add_subscription, name='add_subscription'),
    path('subscription/<int:subscription_id>/edit/', edit_subscription, name='edit_subscription'),
    path('subscription/<int:subscription_id>/delete/', delete_subscription, name='delete_subscription'),

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

    path('features/', view_features, name='view_features'),
    path('feature/<int:feature_id>/', view_feature, name='view_feature'),
    path('feature/add/', add_feature, name='add_feature'),
    path('feature/<int:feature_id>/edit/', edit_feature, name='edit_feature'),
    path('feature/<int:feature_id>/delete/', delete_feature, name='delete_feature'),
    
    path('roles/', view_roles, name='view_roles'),
    path('role/<int:role_id>/', view_role, name='view_role'),
    path('role/add/', add_role, name='add_role'),
    path('role/<int:role_id>/edit/', edit_role, name='edit_role'),
    path('role/<int:role_id>/delete/', delete_role, name='delete_role'),
    
    path('permissions/', view_permissions, name='view_permissions'),
    path('permission/<int:permission_id>/', view_permission, name='view_permission'),
    path('permission/add/', add_permission, name='add_permission'),
]