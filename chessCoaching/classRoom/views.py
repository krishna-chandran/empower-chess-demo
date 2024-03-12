from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import  check_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Course,Assignment,Enrollment,UserAssignment, Subscription, Feature, Role, Permission, Package, PackageOptions, Chapter, Page, UserPageActivity
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from .forms import RegisterForm, LoginForm
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
<<<<<<< HEAD
from django.utils import timezone
=======
from django.db.models import Q
from .models import UserActivity, Settings
from datetime import datetime
from datetime import timedelta

>>>>>>> feature_main

def permission_required(feature_name):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            if request.user.is_authenticated and hasattr(request.user, 'user'):
                role = request.user.user.role
                if Permission.objects.filter(role=role, feature__feature_name=feature_name).exists():
                    return view_func(request, *args, **kwargs)
            return render(request, 'common/no_permission.html')
        return _wrapped_view
    return decorator

def log_user_activity(request, action):
    if request.user.is_authenticated:
        user_id = request.user.user.id if hasattr(request.user, 'user') else None

        if request.user.is_superuser:
            user_id = 0

        if user_id:
            user = User.objects.get(id=user_id)
            UserActivity.objects.create(user=user, action=action)
    
@login_required
def index(request):
    log_user_activity(request, 'Viewed index page')
    return render(request,"common/index.html")

@login_required
@permission_required('View Users')
def view_users(request):
    users = User.objects.all()
    log_user_activity(request, 'Viewed users list')
    return render(request, 'users/view_users.html', {'users': users})

@login_required
@permission_required('View User')
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_activities = UserActivity.objects.filter(user=user_id).order_by('-timestamp')[:5]
    log_user_activity(request, f'Viewed user ID: {user_id}')
    return render(request, 'users/view_user.html', {'user': user, 'user_activities': user_activities})




@login_required
@permission_required('Add User')
def add_user(request):
    roles = Role.objects.all()
    
    is_super_admin = request.user.is_superuser
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')
        password = request.POST.get('password')  # Assuming there's a password field in the form

        if AuthUser.objects.filter(username=username).exists():
            return render(request, 'users/add_user.html', {'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exists():
            return render(request, 'users/add_user.html', {'roles': roles, 'error_message': 'Email already exists'})

        # Check if the requested role is admin and the user is not a super admin
        if role_name == 'Admin' and not is_super_admin:
            return render(request, 'users/add_user.html', {'roles': roles, 'error_message': 'Only super admin can register admin users'})

        hashed_password = make_password(password)

        role = Role.objects.get(role_name=role_name)
        auth_user = AuthUser.objects.create(username=username, email=email, password=hashed_password)
        auth_user.save()

        user = User.objects.create(user=auth_user, role=role)
        
        log_user_activity(request, f'Added a new user with ID: {user.id}')
        return redirect('view_users')

    return render(request, 'users/add_user.html', {'roles': roles})

@login_required
@permission_required('Edit User')
def edit_user(request, user_id):
    roles = Role.objects.all()
    user = get_object_or_404(User, id=user_id)
    
    # Check if the user is super admin
    is_super_admin = request.user.is_superuser
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role_name = request.POST.get('role')  # Change variable name to role_name

        if AuthUser.objects.filter(username=username).exclude(id=user.user.id).exists():
            return render(request, 'users/edit_user.html', {'user': user, 'roles': roles, 'error_message': 'Username already exists'})
        
        if AuthUser.objects.filter(email=email).exclude(id=user.user.id).exists():
            return render(request, 'users/edit_user.html', {'user': user,'roles': roles, 'error_message': 'Email already exists'})

        # Check if the requested role is admin and the user is not a super admin
        if role_name == 'Admin' and not is_super_admin:
            return render(request, 'users/edit_user.html', {'user': user, 'roles': roles, 'error_message': 'Only super admin can edit admin users'})

        user.user.username = username
        user.user.email = email
        
        # Retrieve the Role instance corresponding to the selected role name
        role = Role.objects.get(role_name=role_name)
        user.role = role  # Assign the Role instance to the User's role field

        user.user.save()
        user.save()
        
        log_user_activity(request, f'Edited user ID: {user_id}')
        return redirect('view_user', user_id=user_id)
    
    return render(request, 'users/edit_user.html', {'user': user, 'roles': roles})

@login_required
@permission_required('Delete User')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.user.delete()
        user.delete()
        
        log_user_activity(request, f'Deleted user ID: {user_id}')
        return redirect('view_users')
    
    return render(request, 'users/delete_user.html', {'user': user})

@login_required
def view_user_activities(request, user_id):
    user_activities = UserActivity.objects.filter(user=user_id).order_by('-id')
    return render(request, 'user_activities/view_user_activities.html', {'user_activities': user_activities})

@login_required
def view_user_activity(request, activity_id):
    user_activity = get_object_or_404(UserActivity, pk=activity_id)
    return render(request, 'user_activities/view_user_activity.html', {'user_activity': user_activity})

@login_required
def edit_user_activity(request, activity_id):
    user_activity = get_object_or_404(UserActivity, id=activity_id)
    if request.method == 'POST':
        user_activity.action = request.POST.get('action')
        user_activity.timestamp = request.POST.get('timestamp')
        user_activity.save()
        return redirect('view_user_activity', activity_id=user_activity.id)
    return render(request, 'user_activities/edit_user_activity.html', {'user_activity': user_activity})

@login_required
def delete_user_activity(request, activity_id):
    user_activity = get_object_or_404(UserActivity, id=activity_id)
    if request.method == 'POST':
        user_activity.delete()
        return redirect('view_user_activities', user_activity.user.id)
    return render(request, 'user_activities/delete_user_activity.html', {'user_activity': user_activity})

@login_required
@permission_required('View Subscriptions')
def view_subscriptions(request):
    subscriptions = Subscription.objects.all()
    log_user_activity(request, 'Viewed subscriptions')
    return render(request, 'subscriptions/view_subscriptions.html', {'subscriptions': subscriptions})

@login_required
@permission_required('View Subscription')
def view_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    log_user_activity(request, f'Viewed subscription ID: {subscription_id}')
    return render(request, 'subscriptions/view_subscription.html', {'subscription': subscription})

@login_required
@permission_required('Add Subscription')
def add_subscription(request):
    packages = Package.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        package_id = request.POST.get('package')
        payment_date = request.POST.get('payment_date')
        expiry_date = request.POST.get('expiry_date')

        # Check if a subscription with the same package for the same user exists
        existing_subscription = Subscription.objects.filter(user_id=user_id, package_id=package_id).order_by('-expiry_date').first()

        payment_date = datetime.strptime(request.POST.get('payment_date'), '%Y-%m-%d').date()

        if existing_subscription:
            # Check if the expiry date of the existing subscription is greater than the payment date
            if existing_subscription.expiry_date > payment_date:
                # Calculate new expiry date based on existing subscription's expiry date and package validity
                new_expiry_date = existing_subscription.expiry_date + timedelta(days=existing_subscription.package.validity)
                return render(request, 'subscriptions/confirm_extension.html', {'existing_subscription': existing_subscription, 'new_expiry_date': new_expiry_date})
            else:
                subscription = Subscription.objects.create(
                    user_id=user_id,
                    package_id=package_id,
                    payment_date=payment_date,
                    expiry_date=expiry_date
                )

                log_user_activity(request, f'Added subscription ID: {subscription.subscription_id}')
                return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription.subscription_id}))
        subscription = Subscription.objects.create(
            user_id=user_id,
            package_id=package_id,
            payment_date=payment_date,
            expiry_date=expiry_date
        )

        log_user_activity(request, f'Added subscription ID: {subscription.subscription_id}')
        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription.subscription_id}))

    razorpay_key = Settings.objects.get(key='razorpay_key').value
    stripe_key = Settings.objects.get(key='stripe_key').value

    return render(request, 'subscriptions/add_subscription.html', {'users': users, 'packages': packages, 'razorpay_key': razorpay_key, 'stripe_key': stripe_key})
@login_required
@permission_required('Edit Subscription')
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

        log_user_activity(request, f'Edited subscription ID: {subscription_id}')
        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription_id}))

    return render(request, 'subscriptions/edit_subscription.html', {'subscription': subscription, 'users': users, 'packages': packages})

@login_required
@permission_required('Delete Subscription')
def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if request.method == 'POST':
        subscription.delete()
        log_user_activity(request, f'Deleted subscription ID: {subscription_id}')
        return redirect('view_subscriptions') 
    return render(request, 'subscriptions/delete_subscription.html', {'subscription': subscription})

@login_required
@permission_required('View Packages')
def view_packages(request):
    packages = Package.objects.all()
    log_user_activity(request, 'Viewed packages')
    return render(request, 'packages/view_packages.html', {'packages': packages})

@login_required
@permission_required('View Package')
def view_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    log_user_activity(request, f'Viewed package ID: {package_id}')
    return render(request, 'packages/view_package.html', {'package': package})

@login_required
@permission_required('Add Package')
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
            log_user_activity(request, f'Added package Id: {package.package_id}')
            return redirect('view_package', package_id=package.package_id)

        except IntegrityError:
            error_message = "An error occurred while adding the package."
            return render(request, 'packages/add_package.html', {'error_message': error_message})

    return render(request, 'packages/add_package.html')

@login_required
@permission_required('Edit Package')
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
            log_user_activity(request, f'Edited package ID: {package_id}')
            return redirect('view_package', package_id=package.package_id)

        except IntegrityError:
            error_message = "An error occurred while editing the package."
            return render(request, 'packages/edit_package.html', {'package': package, 'error_message': error_message})

    return render(request, 'packages/edit_package.html', {'package': package})

@login_required
@permission_required('Delete Package')
def delete_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    if request.method == 'POST':
        package.delete()
        log_user_activity(request, f'Deleted package ID: {package_id}')
        return redirect('view_packages')

    return render(request, 'packages/delete_package.html', {'package': package})

@login_required
@permission_required('View Package Options')
def view_package_options(request):
    package_options = PackageOptions.objects.all()
    log_user_activity(request, 'Viewed package options')
    return render(request, 'package_options/view_package_options.html', {'package_options': package_options})

@login_required
@permission_required('View Package Option')
def view_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    log_user_activity(request, f'Viewed package option ID: {option_id}')
    return render(request, 'package_options/view_package_option.html', {'package_option': package_option})

@login_required
@permission_required('Add Package Option')
def add_package_option(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        course_id = request.POST.get('course_id')

        package_option = PackageOptions.objects.create(
            package_id=package_id,
            course_id=course_id
        )
        log_user_activity(request, f'Added package option ID: {package_option.option_id}')
        return redirect('view_package_option', option_id=package_option.option_id)

    packages = Package.objects.all()
    courses = Course.objects.all()
    return render(request, 'package_options/add_package_option.html', {'packages': packages, 'courses': courses})

@login_required
@permission_required('Edit Package Option')
def edit_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        course_id = request.POST.get('course_id')

        package_option.package_id = package_id
        package_option.course_id = course_id
        package_option.save()

        log_user_activity(request, f'Edited package option ID: {option_id}')
        return redirect('view_package_option', option_id=package_option.option_id)

    packages = Package.objects.all()
    courses = Course.objects.all()
    return render(request, 'package_options/edit_package_option.html', {'package_option': package_option, 'packages': packages, 'courses': courses})

@login_required
@permission_required('Delete Package Option')
def delete_package_option(request, option_id):
    package_option = get_object_or_404(PackageOptions, pk=option_id)
    if request.method == 'POST':
        package_option.delete()
        log_user_activity(request, f'Deleted package option ID: {option_id}')
        return redirect('view_package_options')
    return render(request, 'package_options/delete_package_option.html', {'package_option': package_option})

@login_required
@permission_required('View Courses')
def view_courses(request):
	course_data = Course.objects.all()
	log_user_activity(request, 'Viewed courses')
	return render(request,"courses/view_courses.html",{'course_data': course_data} )

@login_required
@permission_required('View Course')
def view_course(request, course_id):
    course_data = get_object_or_404(Course, id=course_id)
    log_user_activity(request, f'Viewed course ID: {course_id}')
    return render(request, 'courses/view_course.html', {'course_data': course_data})

@login_required
@permission_required('Add Course')
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        course = Course.objects.create(course_name=course_name, course_description=course_description)
        log_user_activity(request, f'Added course ID: {course.id}')
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
        log_user_activity(request, f'Edited course ID: {course_id}')
        return redirect(reverse('view_course', kwargs={'course_id': course_id}))
    return render(request, 'courses/edit_course.html', {'course_data': course_data})


@login_required
@permission_required('Delete Course')
def delete_course(request, course_id):
<<<<<<< HEAD
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.delete()
		return redirect('view_courses')
	# course_data = {'id': course_id, 'name': 'Mate in One', 'description': 'Mate in one course'}
	return render(request,'courses/delete_course.html', {'course_data': course_data} )
=======
    course_data = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course_data.delete()
        log_user_activity(request, f'Deleted course ID: {course_id}')
        return redirect('view_courses')
    return render(request,'courses/delete_course.html',{'course_data': course_data} )
>>>>>>> feature_main

@login_required
# @permission_required('View Chapters')
def view_chapters(request):
    chapters = Chapter.objects.all()
    print(chapters)
    return render(request,"chapters/view_chapters.html",{'chapters': chapters} )

@login_required
# @permission_required('View Chapter')
def view_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request, 'chapters/view_chapter.html', {'chapter': chapter})

@login_required
# @permission_required('Add Chapter')
def add_chapter(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        order = request.POST.get('order')
        
        if not course_id:
            return HttpResponseBadRequest("Course is required.")
        chapter = Chapter.objects.create(course_id=course_id, title=title, order=order,)
        return redirect(reverse('view_chapter', kwargs={'chapter_id': chapter.id}))
    return render(request, 'chapters/add_chapter.html', {'courses': courses})

@login_required
# @permission_required('Edit Chapter')
def edit_chapter(request, chapter_id):
    chapter_data = get_object_or_404(Chapter, pk=chapter_id)
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        order = request.POST.get('order')
        if not course_id:
            return HttpResponseBadRequest("Course is required.")
        chapter_data.course_id = course_id
        chapter_data.title = title
        chapter_data.order = order
        chapter_data.save()
        return redirect(reverse('view_chapter', kwargs={'chapter_id': chapter_id}))
    return render(request, 'chapters/edit_chapter.html', {'chapter_data': chapter_data, 'courses': courses})

@login_required
# @permission_required('Delete Chapter')
def delete_chapter(request, chapter_id):
    chapter_data = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        chapter_data.delete()
        return redirect('view_chapters')
    return render(request, 'chapters/delete_chapter.html', {'chapter_data': chapter_data})

@login_required
# @permission_required('View Pages')
def view_pages(request):
	pages = Page.objects.all()
	return render(request,"pages/view_pages.html",{'pages': pages} )

@login_required
# @permission_required('View Page')
def view_page(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render(request, 'pages/view_page.html', {'page': page})


@login_required
# @permission_required('Add Page')
def add_page(request):
    chapters = Chapter.objects.all()
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter')
        title = request.POST.get('title')
        content = request.POST.get('content')
        order = request.POST.get('order')
        if not chapter_id:
            return HttpResponseBadRequest("Chapter is required.")
        page = Page.objects.create(chapter_id=chapter_id, title=title, content=content, order=order)
        return redirect(reverse('view_page', kwargs={'page_id': page.id}))
    return render(request, 'pages/add_page.html', {'chapters': chapters})

@login_required
# @permission_required('Edit Page')
def edit_page(request, page_id):
    page_data = get_object_or_404(Page, id=page_id)
    chapters = Chapter.objects.all()
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter')
        title = request.POST.get('title')
        content = request.POST.get('content')
        order = request.POST.get('order')
        if not chapter_id:
            return HttpResponseBadRequest("Chapter is required.")
        page_data.chapter_id = chapter_id
        page_data.title = title
        page_data.content = content
        page_data.order = order
        page_data.save()
        return redirect(reverse('view_page', kwargs={'page_id': page_id}))
    return render(request, 'pages/edit_page.html', {'page_data': page_data, 'chapters' : chapters})

@login_required
# @permission_required('Delete Page')
def delete_page(request, page_id):
    page_data = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        page_data.delete()
        return redirect('view_pages')
    return render(request, 'pages/delete_page.html', {'page_data': page_data})

@login_required
@permission_required('View Page Activity')
def view_page_activity(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_page_activity = UserPageActivity.objects.filter(user=user)
    return render(request, 'user_page_activity.html', {'user_page_activity': user_page_activity})

@login_required
def track_page_activity(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    time_spent_seconds = 300
    UserPageActivity.objects.update_or_create(
        user=request.user,
        page=page,
        defaults={
            'percentage_completed': 100, 
            'time_spent_seconds': time_spent_seconds,
            'last_accessed': timezone.now()
        }
    )
    return redirect('page_detail', page_id=page_id)

@login_required
@permission_required('View Enrollments')
def view_enrollments(request):
    enrollments = Enrollment.objects.all()
    log_user_activity(request, 'Viewed enrollments')
    return render(request, "enrollments/view_enrollments.html", {'enrollments': enrollments})

@login_required
@permission_required('View Enrollment')
def view_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    log_user_activity(request, f'Viewed enrollment ID: {enrollment_id}')
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
        log_user_activity(request, f'Added enrollment ID: {enrollment.id}')
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
        
        log_user_activity(request, f'Edited enrollment ID: {enrollment_id}')
        return redirect(reverse('view_enrollment', kwargs={'enrollment_id': enrollment_id}))
    
    return render(request, 'enrollments/edit_enrollment.html', {'enrollment_data': enrollment_data, 'courses': courses, 'users': users})

@login_required
@permission_required('Delete Enrollment')
def delete_enrollment(request, enrollment_id):
    enrollment_data = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment_data.delete()
        log_user_activity(request, f'Deleted enrollment ID: {enrollment_id}')
        return redirect('view_enrollments')
    
    return render(request, 'enrollments/delete_enrollment.html', {'enrollment_data': enrollment_data})

@login_required
@permission_required('View Assignments')
def view_assignments(request):
    assignments = Assignment.objects.all()
    log_user_activity(request, 'Viewed assignments')
    return render(request, 'assignments/view_assignments.html', {'assignments': assignments})

@login_required
@permission_required('View Assignment')
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    log_user_activity(request, f'Viewed assignment ID: {assignment_id}')
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
        log_user_activity(request, f'Added assignment ID: {assignment.id}')
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

        log_user_activity(request, f'Edited assignment ID: {assignment_id}')
        return redirect(reverse('view_assignment', kwargs={'assignment_id': assignment.id}))

    return render(request, 'assignments/edit_assignment.html', {'assignment': assignment, 'courses': courses})

@login_required
@permission_required('Delete Assignment')
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'POST':
        assignment.delete()
        log_user_activity(request, f'Deleted assignment ID: {assignment_id}')
        return redirect('view_assignments')  # Redirect to the assignments list view
        
    return render(request, 'assignments/delete_assignment.html', {'assignment': assignment})

@login_required
@permission_required('View Userassignments')
def view_userassignments(request):
    user_assignments = UserAssignment.objects.all()
    log_user_activity(request, 'Viewed user assignments')
    return render(request, 'userassignments/view_userassignments.html', {'user_assignments': user_assignments})


@login_required
@permission_required('View Userassignment')
def view_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    log_user_activity(request, f'Viewed user assignment ID: {user_assignment_id}')
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
        log_user_activity(request, f'Added user assignment ID: {user_assignment.id}')
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
        
        log_user_activity(request, f'Edited user assignment ID: {user_assignment_id}')
        return redirect(reverse('view_userassignment', kwargs={'user_assignment_id': user_assignment_id}))
    
    return render(request, 'userassignments/edit_userassignment.html', {'user_assignment': user_assignment, 'assignments': assignments, 'users': users})

@login_required
@permission_required('Delete Userassignment')
def delete_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    if request.method == 'POST':
        user_assignment.delete()
        log_user_activity(request, f'Deleted user assignment ID: {user_assignment_id}')
        return redirect('view_userassignments')
    return render(request, 'userassignments/delete_userassignment.html', {'user_assignment': user_assignment})

@login_required
@permission_required('View Features')
def view_features(request):
    features = Feature.objects.all()
    log_user_activity(request, 'Viewed features')
    return render(request, 'features/view_features.html', {'features': features})

@login_required
@permission_required('View Feature')
def view_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)
    log_user_activity(request, f'Viewed feature ID: {feature_id}')
    return render(request, 'features/view_feature.html', {'feature': feature})

@login_required
@permission_required('Add Feature')
def add_feature(request):
    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')

        try:
            new_feature = Feature.objects.create(feature_name=feature_name)
            log_user_activity(request, f'Added feature ID: {new_feature.id}')
            return redirect(reverse('view_feature', kwargs={'feature_id': new_feature.id}))
        except IntegrityError:
            error_message = "A feature with this name already exists."
            return render(request, 'features/add_feature.html', {'error_message': error_message})
    else:
        return render(request, 'features/add_feature.html')

@login_required
@permission_required('Edit Feature')    
def edit_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)

    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')
        feature.feature_name = feature_name
        try:
            feature.save()
            log_user_activity(request, f'Edited feature ID: {feature_id}')
            return redirect(reverse('view_feature', kwargs={'feature_id': feature.id}))
        except IntegrityError:
            error_message = "A feature with this name already exists."
            return render(request, 'features/edit_feature.html', {'feature': feature, 'error_message': error_message})
    
    return render(request, 'features/edit_feature.html', {'feature': feature})

@login_required
@permission_required('Delete Feature')
def delete_feature(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)

    if request.method == 'POST':
        feature.delete()
        log_user_activity(request, f'Deleted feature ID: {feature_id}')
        return redirect('view_features')
    
    return render(request, 'features/delete_feature.html', {'feature': feature})

@login_required
@permission_required('View Roles')
def view_roles(request):
    roles = Role.objects.all()
    log_user_activity(request, 'Viewed roles')
    return render(request, 'roles/view_roles.html', {'roles': roles})

@login_required
@permission_required('View Role')
def view_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    log_user_activity(request, f'Viewed role ID: {role_id}')
    return render(request, 'roles/view_role.html', {'role': role})

@login_required
@permission_required('Add  Role')
def add_role(request):
    if request.method == 'POST':
        role_name = request.POST.get('role_name')

        try:
            new_role = Role.objects.create(role_name=role_name)
            log_user_activity(request, f'Added role ID: {new_role.id}')
            return redirect(reverse('view_role', kwargs={'role_id': new_role.id}))
        except IntegrityError as e:
            error_message = "A role with this name already exists."
            return render(request, 'roles/add_role.html', {'error_message': error_message})
    else:
        return render(request, 'roles/add_role.html')

@login_required
@permission_required('Edit Role')    
def edit_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        role.role_name = role_name
        try:
            role.save()
            log_user_activity(request, f'Edited role ID: {role_id}')
            return redirect(reverse('view_role', kwargs={'role_id': role.id}))
        except IntegrityError as e:
            error_message = "A role with this name already exists."
            return render(request, 'roles/edit_role.html', {'role': role, 'error_message': error_message})

    return render(request, 'roles/edit_role.html', {'role': role})

@login_required
@permission_required('Delete Role')
def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)

    if request.method == 'POST':
        role.delete()
        log_user_activity(request, f'Deleted role ID: {role_id}')
        return redirect('view_roles')
    
    return render(request, 'roles/delete_role.html', {'role': role})

@login_required
@permission_required('View Permissions')
def view_permissions(request):
    permissions = Permission.objects.all()
    log_user_activity(request, 'Viewed permissions')
    return render(request, 'permissions/view_permissions.html', {'permissions': permissions})

@login_required
@permission_required('View Permission')
def view_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    log_user_activity(request, f'Viewed permission ID: {permission_id}')
    return render(request, 'permissions/view_permission.html', {'permission': permission})

@login_required
@permission_required('Add Permission')
def add_permission(request):
    roles = Role.objects.all()
    features = Feature.objects.all()
    
    if request.method == 'POST':
        role_id = request.POST.get('role')
        feature_id = request.POST.get('feature')
        
        try:
            permission = Permission.objects.create(role_id=role_id, feature_id=feature_id)
            log_user_activity(request, f'Added permission ID: {permission.id}')
            return redirect('view_permission', permission_id=permission.id)
        except IntegrityError:
            error_message = "A permission with this role and feature combination already exists."
            return render(request, 'permissions/add_permission.html', {'roles': roles, 'features': features, 'error_message': error_message})
    
    return render(request, 'permissions/add_permission.html', {'roles': roles, 'features': features})

@login_required
@permission_required('Edit Permission')
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
            log_user_activity(request, f'Edited permission ID: {permission_id}')
            return redirect('view_permission', permission_id=permission_id)
        except IntegrityError:
            error_message = "A permission with this role and feature combination already exists."
            return render(request, 'permissions/edit_permission.html', {'permission': permission, 'roles': roles, 'features': features, 'error_message': error_message})
    
    return render(request, 'permissions/edit_permission.html', {'permission': permission, 'roles': roles, 'features': features})

@login_required
@permission_required('Delete Permission')
def delete_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    
    if request.method == 'POST':
        permission.delete()
        log_user_activity(request, f'Deleted permission ID: {permission_id}')
        return redirect('view_permissions')
    
    return render(request, 'permissions/delete_permission.html', {'permission': permission})

@login_required
@permission_required('View Settings')
def view_settings(request):
    settings = Settings.objects.all()
    log_user_activity(request, 'Viewed settings')
    return render(request, 'settings/view_settings.html', {'settings': settings})

@login_required
@permission_required('View Setting')
def view_setting(request, setting_id):
    setting = get_object_or_404(Settings, pk=setting_id)
    log_user_activity(request, f'Viewed Setting ID: {setting_id}')
    return render(request, 'settings/view_setting.html', {'setting': setting})

@login_required
@permission_required('Add Setting')
def add_setting(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')

        setting = Settings.objects.create(
            key=key,
            value=value
        )
        log_user_activity(request, f'Added setting ID: {setting.id}')
        return redirect('view_setting', setting_id=setting.id)

    return render(request, 'settings/add_setting.html')

@login_required
@permission_required('Edit Setting')
def edit_setting(request, setting_id):
    setting = get_object_or_404(Settings, pk=setting_id)
    if request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')

        setting.key = key
        setting.value = value
        setting.save()

        log_user_activity(request, f'Edited setting ID: {setting_id}')
        return redirect('view_setting', setting_id=setting.id)

    return render(request, 'settings/edit_setting.html', {'setting': setting})

@login_required
@permission_required('Delete Setting')
def delete_setting(request, setting_id):
    setting = get_object_or_404(Settings, pk=setting_id)
    if request.method == 'POST':
        setting.delete()
        log_user_activity(request, f'Deleted setting ID: {setting_id}')
        return redirect('view_settings')
    return render(request, 'settings/delete_setting.html', {'setting': setting})


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
        
        is_super_admin = request.user.is_superuser
        
        # Check if the requested role is admin and the user is not a super admin
        if role_name == 'Admin' and not is_super_admin:
            return render(request, 'registration/register.html', {'roles': roles, 'error_message': 'Only super admin can register admin users'})

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
    # auth_user_emails = AuthUser.objects.values_list('email', flat=True)
    # print("Emails in AuthUser table:", list(auth_user_emails))

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # print("Username or Email:", username_or_email)
        # print("Password:", password)

        # Check if input is email format
        if '@' in username_or_email:
            # Try to authenticate using email
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # Try to authenticate using username
            user = authenticate(request, username=username_or_email, password=password)

        # print("Authenticated User:", user)

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




