from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import  check_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Course,Assignment,Enrollment,UserAssignment, Subscription, Feature, Role, Permission, Package, PackageOptions
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from .forms import RegisterForm,LoginForm
from .models import Student
from django.contrib.auth.models import User as AuthUser
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from functools import wraps
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Q


def permission_required(feature_name):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'user'):
                role = request.user.user.role
                if Permission.objects.filter(role=role, feature__feature_name=feature_name).exists():
                    return view_func(request, *args, **kwargs)
            return render(request, 'common/no_permission.html')
        return _wrapped_view
    return decorator

@login_required
def index(request):
	return render(request,"common/index.html")

@login_required
# @permission_required('View Users')
def view_users(request):
    users = User.objects.all()
    return render(request, 'users/view_users.html', {'users': users})

@login_required
# @permission_required('View User')
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/view_user.html', {'user': user})

@login_required
# @permission_required('Add User')
def add_user(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')
        password = request.POST.get('password')  # Assuming there's a password field in the form

        if AuthUser.objects.filter(username=username).exists():
            return render(request, 'users/add_user.html', {'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exists():
            return render(request, 'users/add_user.html', {'roles': roles, 'error_message': 'Email already exists'})

        hashed_password = make_password(password)

        role = Role.objects.get(role_name=role_name)
        auth_user = AuthUser.objects.create(username=username, email=email, password=hashed_password)
        auth_user.save()

        user = User.objects.create(user=auth_user, role=role)
        
        return redirect('view_users')

    return render(request, 'users/add_user.html', {'roles': roles})

@login_required
# @permission_required('Edit User')
def edit_user(request, user_id):
    roles = Role.objects.all()
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')  # Change variable name to role_name

        if AuthUser.objects.filter(username=username).exclude(id=user.user.id).exists():
            return render(request, 'users/edit_user.html', {'user': user, 'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exclude(id=user.user.id).exists():
            return render(request, 'users/edit_user.html', {'user': user,'roles': roles, 'error_message': 'Email already exists'})

        user.user.username = username
        user.user.email = email
        
        # Retrieve the Role instance corresponding to the selected role name
        role = Role.objects.get(role_name=role_name)
        user.role = role  # Assign the Role instance to the User's role field

        user.user.save()
        user.save()
        
        return redirect('view_user', user_id=user_id)
    
    return render(request, 'users/edit_user.html', {'user': user, 'roles': roles})

@login_required
# @permission_required('Delete User')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.user.delete()
        user.delete()
        
        return redirect('view_users')
    
    return render(request, 'users/delete_user.html', {'user': user})

@login_required
# @permission_required('View Subscriptions')
def view_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscriptions/view_subscriptions.html', {'subscriptions': subscriptions})

@login_required
# @permission_required('View Subscription')
def view_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    return render(request, 'subscriptions/view_subscription.html', {'subscription': subscription})

@login_required
# @permission_required('Add Subscription')
def add_subscription(request):
    packages = Package.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user')
        package_id = request.POST.get('package')
        payment_date = request.POST.get('payment_date')
        expiry_date = request.POST.get('expiry_date')

        subscription = Subscription.objects.create(
            user_id=user_id,
            package_id=package_id,
            payment_date=payment_date,
            expiry_date=expiry_date
        )

        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription.subscription_id}))

    return render(request, 'subscriptions/add_subscription.html', {'users': users, 'packages': packages})
@login_required
# @permission_required('Edit Subscription')
def edit_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, subscription_id=subscription_id)
    users = User.objects.all()
    packages = Package.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        package_id = request.POST.get('package')
        payment_date = request.POST.get('payment_date')
        expiry_date = request.POST.get('expiry_date')

        subscription.user_id = user_id
        subscription.package_id = package_id
        subscription.payment_date = payment_date
        subscription.expiry_date = expiry_date
        subscription.save()

        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription_id}))

    return render(request, 'subscriptions/edit_subscription.html', {'subscription': subscription, 'users': users, 'packages': packages})

@login_required
# @permission_required('Delete Subscription')
def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if request.method == 'POST':
        subscription.delete()
        return redirect('view_subscriptions') 
    return render(request, 'subscriptions/delete_subscription.html', {'subscription': subscription})

@login_required
def view_packages(request):
    packages = Package.objects.all()
    return render(request, 'packages/view_packages.html', {'packages': packages})

@login_required
def view_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'packages/view_package.html', {'package': package})

@login_required
def add_package(request):
    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        package_description = request.POST.get('package_description')
        price = request.POST.get('price')
        validity = request.POST.get('validity')

        if Package.objects.filter(package_name=package_name).exists():
            error_message = "Package with this name already exists. Choose a different name."
            return render(request, 'packages/add_package.html', {'error_message': error_message})

        try:
            package = Package.objects.create(
                package_name=package_name,
                package_description=package_description,
                price=price,
                validity=validity
            )
            return redirect('view_package', package_id=package.package_id)

        except IntegrityError:
            error_message = "An error occurred while adding the package."
            return render(request, 'packages/add_package.html', {'error_message': error_message})

    return render(request, 'packages/add_package.html')

@login_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        package_description = request.POST.get('package_description')
        price = request.POST.get('price')
        validity = request.POST.get('validity')

        if package_name != package.package_name and Package.objects.filter(package_name=package_name).exists():
            error_message = "Package with this name already exists. Choose a different name."
            return render(request, 'packages/edit_package.html', {'package': package, 'error_message': error_message})

        try:
            package.package_name = package_name
            package.package_description = package_description
            package.price = price
            package.validity = validity
            package.save()
            return redirect('view_package', package_id=package.package_id)

        except IntegrityError:
            error_message = "An error occurred while editing the package."
            return render(request, 'packages/edit_package.html', {'package': package, 'error_message': error_message})

    return render(request, 'packages/edit_package.html', {'package': package})

@login_required
def delete_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    if request.method == 'POST':
        package.delete()
        return redirect('view_packages')

    return render(request, 'packages/delete_package.html', {'package': package})

def view_package_options(request):
    package_options = PackageOptions.objects.all()
    return render(request, 'package_options/view_package_options.html', {'package_options': package_options})

def view_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    return render(request, 'package_options/view_package_option.html', {'package_option': package_option})

@login_required
def add_package_option(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        course_id = request.POST.get('course_id')

        package_option = PackageOptions.objects.create(
            package_id=package_id,
            course_id=course_id
        )

        return redirect('view_package_option', option_id=package_option.option_id)

    packages = Package.objects.all()
    courses = Course.objects.all()
    return render(request, 'package_options/add_package_option.html', {'packages': packages, 'courses': courses})

@login_required
def edit_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        course_id = request.POST.get('course_id')

        package_option.package_id = package_id
        package_option.course_id = course_id
        package_option.save()

        return redirect('view_package_option', option_id=package_option.option_id)

    packages = Package.objects.all()
    courses = Course.objects.all()
    return render(request, 'package_options/edit_package_option.html', {'package_option': package_option, 'packages': packages, 'courses': courses})

def delete_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    if request.method == 'POST':
        package_option.delete()
        return redirect('view_package_options')
    return render(request, 'package_options/delete_package_option.html', {'package_option': package_option})

@login_required
@permission_required('View Courses')
def view_courses(request):
	course_data = Course.objects.all()
	# print(course_data)
	return render(request,"courses/view_courses.html",{'course_data': course_data} )

@login_required
@permission_required('View Course')
def view_course(request, course_id):
    course_data = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/view_course.html', {'course_data': course_data})

@login_required
@permission_required('Add Course')
def add_course(request):
    # user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
	if request.method == 'POST':
		course_name = request.POST.get('course_name')
		course_description = request.POST.get('course_description')
		course = Course.objects.create(course_name=course_name, course_description=course_description)
		return redirect(reverse('view_course', kwargs={'course_id': course.id}))
	return render(request, 'courses/add_course.html')

@login_required
@permission_required('Edit Course')
def edit_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.course_name = request.POST.get('course_name')
		course_data.course_description = request.POST.get('course_description')
		course_data.save()
		return redirect(reverse('view_course', kwargs={'course_id': course_id}))
	return render(request, 'courses/edit_course.html', {'course_data': course_data})


@login_required
@permission_required('Delete Course')
def delete_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.delete()
		return redirect('view_courses')
	# course_data = {'id': course_id, 'name': 'Mate in One', 'description': 'Mate in one course'}
	return render(request,'courses/delete_course.html',{'course_data': course_data} )


@login_required
@permission_required('View Enrollments')
def view_enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, "enrollments/view_enrollments.html", {'enrollments': enrollments})

@login_required
@permission_required('View Enrollment')
def view_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    return render(request, 'enrollments/view_enrollment.html', {'enrollment': enrollment})

@login_required
@permission_required('Add Enrollment')
def add_enrollment(request):
    courses = Course.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        enrollment_date = request.POST.get('enrollment_date')
        
        enrollment = Enrollment.objects.create(user_id=user_id, course_id=course_id, enrollment_date=enrollment_date)
        
        return redirect(reverse('view_enrollment', kwargs={'enrollment_id': enrollment.id}))
    return render(request, 'enrollments/add_enrollment.html', {'courses': courses, 'users': users})

@login_required
@permission_required('Edit Enrollment')
def edit_enrollment(request, enrollment_id):
    enrollment_data = get_object_or_404(Enrollment, id=enrollment_id)
    courses = Course.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        enrollment_date = request.POST.get('enrollment_date')

        # Validate that course_id is not None or empty
        if not course_id:
            # Return a bad request response with an error message
            return HttpResponseBadRequest("Course is required.")

        # Update enrollment data
        enrollment_data.user_id = user_id
        enrollment_data.course_id = course_id
        enrollment_data.enrollment_date = enrollment_date
        enrollment_data.save()
        
        return redirect(reverse('view_enrollment', kwargs={'enrollment_id': enrollment_id}))
    
    return render(request, 'enrollments/edit_enrollment.html', {'enrollment_data': enrollment_data, 'courses': courses, 'users': users})

@login_required
@permission_required('Delete Enrollment')
def delete_enrollment(request, enrollment_id):
    enrollment_data = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment_data.delete()
        return redirect('view_enrollments')
    
    return render(request, 'enrollments/delete_enrollment.html', {'enrollment_data': enrollment_data})

@login_required
@permission_required('View Assignments')
def view_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/view_assignments.html', {'assignments': assignments})

@login_required
@permission_required('View Assignment')
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    return render(request, 'assignments/view_assignment.html', {'assignment': assignment})

@login_required
@permission_required('Add Assignment')
def add_assignment(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        assignment_name = request.POST.get('assignment_name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        assignment = Assignment.objects.create(
            course_id=course_id,
            assignment_name=assignment_name,
            description=description,
            due_date=due_date
        )
        return redirect(reverse('view_assignment', kwargs={'assignment_id': assignment.id}))
    return render(request, 'assignments/add_assignment.html', {'courses': courses})

@login_required
@permission_required('Edit Assignment')
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    courses = Course.objects.all()
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        assignment_name = request.POST.get('assignment_name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        # Update the assignment
        assignment.course_id = course_id
        assignment.assignment_name = assignment_name
        assignment.description = description
        assignment.due_date = due_date
        assignment.save()

        # Redirect to a page showing the edited assignment
        return redirect(reverse('view_assignment', kwargs={'assignment_id': assignment.id}))

    return render(request, 'assignments/edit_assignment.html', {'assignment': assignment, 'courses': courses})

@login_required
@permission_required('Delete Assignment')
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'POST':
        assignment.delete()
        return redirect('view_assignments')  # Redirect to the assignments list view
        
    return render(request, 'assignments/delete_assignment.html', {'assignment': assignment})

@login_required
@permission_required('View Userassignments')
def view_userassignments(request):
    user_assignments = UserAssignment.objects.all()
    return render(request, 'userassignments/view_userassignments.html', {'user_assignments': user_assignments})


@login_required
@permission_required('View Userassignment')
def view_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    return render(request, 'userassignments/view_userassignment.html', {'user_assignment': user_assignment})

@login_required
@permission_required('Add Userassignment')
def add_userassignment(request):
    assignments = Assignment.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        assignment_id = request.POST.get('assignment')
        submission_date = request.POST.get('submission_date')
        grade = request.POST.get('grade')
        comments = request.POST.get('comments')

        user_assignment = UserAssignment.objects.create(
            user_id=user_id,
            assignment_id=assignment_id,
            submission_date=submission_date,
            grade=grade,
            comments=comments
        )
        return redirect(reverse('view_userassignment', kwargs={'user_assignment_id': user_assignment.id}))
    return render(request, 'userassignments/add_userassignment.html', {'assignments': assignments, 'users': users})

@login_required
@permission_required('Edit Userassignment')
def edit_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    assignments = Assignment.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        user_assignment.user_id = request.POST.get('user')
        user_assignment.assignment_id = request.POST.get('assignment')
        user_assignment.submission_date = request.POST.get('submission_date')
        user_assignment.grade = request.POST.get('grade')
        user_assignment.comments = request.POST.get('comments')
        user_assignment.save()
        
        return redirect(reverse('view_userassignment', kwargs={'user_assignment_id': user_assignment_id}))
    
    return render(request, 'userassignments/edit_userassignment.html', {'user_assignment': user_assignment, 'assignments': assignments, 'users': users})

@login_required
@permission_required('Delete Userassignment')
def delete_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    if request.method == 'POST':
        user_assignment.delete()
        return redirect('view_userassignments')
    return render(request, 'userassignments/delete_userassignment.html', {'user_assignment': user_assignment})

@login_required
# @permission_required('View Features')
def view_features(request):
    features = Feature.objects.all()
    return render(request, 'features/view_features.html', {'features': features})

@login_required
# @permission_required('View Feature'))
def view_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)
    return render(request, 'features/view_feature.html', {'feature': feature})

@login_required
# @permission_required('Add Feature')
def add_feature(request):
    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')

        try:
            new_feature = Feature.objects.create(feature_name=feature_name)
            return redirect(reverse('view_feature', kwargs={'feature_id': new_feature.id}))
        except IntegrityError:
            error_message = "A feature with this name already exists."
            return render(request, 'features/add_feature.html', {'error_message': error_message})
    else:
        return render(request, 'features/add_feature.html')

@login_required
# @permission_required('Edit Feature')    
def edit_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)

    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')
        feature.feature_name = feature_name
        try:
            feature.save()
            return redirect(reverse('view_feature', kwargs={'feature_id': feature.id}))
        except IntegrityError:
            error_message = "A feature with this name already exists."
            return render(request, 'features/edit_feature.html', {'feature': feature, 'error_message': error_message})
    
    return render(request, 'features/edit_feature.html', {'feature': feature})

@login_required
# @permission_required('Delete Feature')
def delete_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)

    if request.method == 'POST':
        feature.delete()
        return redirect('view_features')
    
    return render(request, 'features/delete_feature.html', {'feature': feature})

@login_required
# @permission_required('View Roles')
def view_roles(request):
    roles = Role.objects.all()
    return render(request, 'roles/view_roles.html', {'roles': roles})

@login_required
# @permission_required('View Role')
def view_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    return render(request, 'roles/view_role.html', {'role': role})

@login_required
# @permission_required('Add  Role')
def add_role(request):
    if request.method == 'POST':
        role_name = request.POST.get('role_name')

        try:
            new_role = Role.objects.create(role_name=role_name)
            return redirect(reverse('view_role', kwargs={'role_id': new_role.id}))
        except IntegrityError as e:
            error_message = "A role with this name already exists."
            return render(request, 'roles/add_role.html', {'error_message': error_message})
    else:
        return render(request, 'roles/add_role.html')

@login_required
# @permission_required('Edit Role')    
def edit_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        role.role_name = role_name
        try:
            role.save()
            return redirect(reverse('view_role', kwargs={'role_id': role.id}))
        except IntegrityError as e:
            error_message = "A role with this name already exists."
            return render(request, 'roles/edit_role.html', {'role': role, 'error_message': error_message})

    return render(request, 'roles/edit_role.html', {'role': role})

@login_required
# @permission_required('Delete Role')
def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
        role.delete()
        return redirect('view_roles')
    
    return render(request, 'roles/delete_role.html', {'role': role})

@login_required
# @permission_required('View Permissions')
def view_permissions(request):
    permissions = Permission.objects.all()
    return render(request, 'permissions/view_permissions.html', {'permissions': permissions})

@login_required
# @permission_required('View Permission')
def view_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    return render(request, 'permissions/view_permission.html', {'permission': permission})

@login_required
# @permission_required('Add Permission')
def add_permission(request):
    roles = Role.objects.all()
    features = Feature.objects.all()
    
    if request.method == 'POST':
        role_id = request.POST.get('role')
        feature_id = request.POST.get('feature')
        
        try:
            permission = Permission.objects.create(role_id=role_id, feature_id=feature_id)
            return redirect('view_permission', permission_id=permission.id)
        except IntegrityError:
            error_message = "A permission with this role and feature combination already exists."
            return render(request, 'permissions/add_permission.html', {'roles': roles, 'features': features, 'error_message': error_message})
    
    return render(request, 'permissions/add_permission.html', {'roles': roles, 'features': features})

@login_required
# @permission_required('Edit Permission')
def edit_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    roles = Role.objects.all()
    features = Feature.objects.all()
    
    if request.method == 'POST':
        role_id = request.POST.get('role')
        feature_id = request.POST.get('feature')

        # Validate that role_id and feature_id are not None or empty
        if not role_id:
            return HttpResponseBadRequest("Role is required.")
        if not feature_id:
            return HttpResponseBadRequest("Feature is required.")

        try:
            # Update permission data
            permission.role_id = role_id
            permission.feature_id = feature_id
            permission.save()
            return redirect('view_permission', permission_id=permission_id)
        except IntegrityError:
            error_message = "A permission with this role and feature combination already exists."
            return render(request, 'permissions/edit_permission.html', {'permission': permission, 'roles': roles, 'features': features, 'error_message': error_message})
    
    return render(request, 'permissions/edit_permission.html', {'permission': permission, 'roles': roles, 'features': features})

@login_required
# @permission_required('Delete Permission')
def delete_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    
    if request.method == 'POST':
        permission.delete()
        return redirect('view_permissions')
    
    return render(request, 'permissions/delete_permission.html', {'permission': permission})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = AuthUser.objects.get(email=email)
        except AuthUser.DoesNotExist:
            user = None

        if user:
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = token_generator.make_token(user)

            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

            send_mail(
                'Password reset request',
                f'Click the following link to reset your password: {reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            
            return HttpResponseRedirect(reverse('password_reset_done'))
        else:
            return render(request, 'registration/forgot-password.html', {'error_message': 'No user found with this email'})

    return render(request, 'registration/forgot-password.html')

def register(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')
        password = request.POST.get('password')

        if AuthUser.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {'roles': roles, 'error_message': 'Email already exists'})

        hashed_password = make_password(password)
        
        role = Role.objects.get(role_name=role_name)
        auth_user = AuthUser.objects.create(username=username, email=email, password=hashed_password)
        auth_user.save()

        user = User.objects.create(user=auth_user, role=role)
        
        return render(request, "registration/registerSuccess.html")

    return render(request, 'registration/register.html', {'roles': roles})

def reg_success(request):
	return render(request,"registration/registerSuccess.html")

def login(request):
    # Print the list of email addresses in the AuthUser table
    auth_user_emails = AuthUser.objects.values_list('email', flat=True)
    print("Emails in AuthUser table:", list(auth_user_emails))

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        print("Username or Email:", username_or_email)
        print("Password:", password)

        # Check if input is email format
        if '@' in username_or_email:
            # Try to authenticate using email
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # Try to authenticate using username
            user = authenticate(request, username=username_or_email, password=password)

        print("Authenticated User:", user)

        if user is not None:
            # User is authenticated, log them in
            auth_login(request, user)
            return redirect('index')
        else:
            # Authentication failed
            error_message = 'Invalid username or password.'
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')


def getUser(request):
	return Student.objects.filter(student_id=request.session['user_id'])

def home(request):
	if 'user_id' in request.session and getUser(request):
		user = getUser(request)
		# print(user)
		return render(request,'common/home.html')
	else:
		return redirect("login")

def logout_user(request):
    logout(request)
    return redirect('login')

def error_404_view(request, exception=None , path_not_found=None):
    return render(request, 'common/404.html', status=404)	

@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request,'profiles/view_profile.html', {'user': user})

@login_required
def edit_profile(request, user_id):
    roles = Role.objects.all()
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')  # Change variable name to role_name

        if AuthUser.objects.filter(username=username).exclude(id=user.user.id).exists():
            return render(request, 'profiles/edit_profile.html', {'user': user, 'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exclude(id=user.user.id).exists():
            return render(request, 'profiles/edit_profile.html', {'user': user,'roles': roles, 'error_message': 'Email already exists'})

        user.user.username = username
        user.user.email = email
        
        # Retrieve the Role instance corresponding to the selected role name
        role = Role.objects.get(role_name=role_name)
        user.role = role  # Assign the Role instance to the User's role field

        user.user.save()
        user.save()
        
        return redirect('view_profile', user_id=user_id)
    
    return render(request, 'profiles/edit_profile.html', {'user': user, 'roles': roles})




