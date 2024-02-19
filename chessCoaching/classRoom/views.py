from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import  check_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Course,Assignment,Enrollment,UserAssignment, Subscription
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .forms import RegisterForm,LoginForm
from .models import Student
from django.contrib.auth.models import User as AuthUser
from django.db import IntegrityError



def index(request):
	return render(request,"common/index.html")

def view_users(request):
    users = User.objects.all()
    return render(request, 'users/view_users.html', {'users': users})

def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/view_user.html', {'user': user})

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if AuthUser.objects.filter(username=username).exists():
            return render(request, 'users/add_user.html', {'error_message': 'Username already exists'})

        auth_user = AuthUser.objects.create_user(username=username, email=email)
        user = User.objects.create(user=auth_user, role=role)
        
        return redirect('view_users')

    return render(request, 'users/add_user.html')


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.user.username = request.POST.get('username')
        user.user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        
        user.user.save()
        user.save()
        
        return redirect('view_user', user_id=user_id)
    
    return render(request, 'users/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.user.delete()
        user.delete()
        
        return redirect('view_users')
    
    return render(request, 'users/delete_user.html', {'user': user})


def view_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscriptions/view_subscriptions.html', {'subscriptions': subscriptions})

def view_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    return render(request, 'subscriptions/view_subscription.html', {'subscription': subscription})

def add_subscription(request):
    # courses = Course.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        subscription_start_date = request.POST.get('subscription_start_date')
        subscription_end_date = request.POST.get('subscription_end_date')
        payment_details = request.POST.get('payment_details')

        subscription = Subscription.objects.create(
            user_id=user_id,
            # course_id=course_id,
            subscription_start_date=subscription_start_date,
            subscription_end_date=subscription_end_date,
            payment_details=payment_details
        )

        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription.id}))


    return render(request, 'subscriptions/add_subscription.html', {'users': users})

def edit_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    users = User.objects.all()
    # courses = Course.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        # course_id = request.POST.get('course')
        subscription_start_date = request.POST.get('subscription_start_date')
        subscription_end_date = request.POST.get('subscription_end_date')
        payment_details = request.POST.get('payment_details')

        # Update subscription data
        subscription.user_id = user_id
        # subscription.course_id = course_id
        subscription.subscription_start_date = subscription_start_date
        subscription.subscription_end_date = subscription_end_date
        subscription.payment_details = payment_details
        subscription.save()

        return redirect(reverse('view_subscription', kwargs={'subscription_id': subscription_id}))

    return render(request, 'subscriptions/edit_subscription.html', {'subscription': subscription, 'users': users})

def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)
    if request.method == 'POST':
        subscription.delete()
        return redirect('view_subscriptions') 
    return render(request, 'subscriptions/delete_subscription.html', {'subscription': subscription})


def view_courses(request):
	# course_data = [
    #     {'id': 1, 'name': 'Mate in One', 'description': 'Mate in one course'}, 
	# 	{'id': 2, 'name': 'Mate in Two', 'description': 'Mate in two course'}, 
	# 	{'id': 3, 'name': 'Mate in Three', 'description': 'Mate in three course'}, 
	# 	{'id': 4, 'name': 'Forced Checkmate', 'description': 'Forced checkmate patterns course'}, 
    # ]
	course_data = Course.objects.all()
	print(course_data)
	return render(request,"courses/view_courses.html",{'course_data': course_data} )

def view_course(request, course_id):
    course_data = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/view_course.html', {'course_data': course_data})

def add_course(request):
    # user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
	if request.method == 'POST':
		course_name = request.POST.get('course_name')
		course_description = request.POST.get('course_description')
		course = Course.objects.create(course_name=course_name, course_description=course_description)
		return redirect(reverse('view_course', kwargs={'course_id': course.id}))
	return render(request, 'courses/add_course.html')

def edit_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.course_name = request.POST.get('course_name')
		course_data.course_description = request.POST.get('course_description')
		course_data.save()
		return redirect(reverse('view_course', kwargs={'course_id': course_id}))
	return render(request, 'courses/edit_course.html', {'course_data': course_data})



def delete_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.delete()
		return redirect('view_courses')
	# course_data = {'id': course_id, 'name': 'Mate in One', 'description': 'Mate in one course'}
	return render(request,'courses/delete_course.html',{'course_data': course_data} )



def view_enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, "enrollments/view_enrollments.html", {'enrollments': enrollments})

def view_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    return render(request, 'enrollments/view_enrollment.html', {'enrollment': enrollment})

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

def delete_enrollment(request, enrollment_id):
    enrollment_data = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment_data.delete()
        return redirect('view_enrollments')
    
    return render(request, 'enrollments/delete_enrollment.html', {'enrollment_data': enrollment_data})

def view_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/view_assignments.html', {'assignments': assignments})

def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    return render(request, 'assignments/view_assignment.html', {'assignment': assignment})

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

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'POST':
        assignment.delete()
        return redirect('view_assignments')  # Redirect to the assignments list view
        
    return render(request, 'assignments/delete_assignment.html', {'assignment': assignment})


def view_userassignments(request):
    user_assignments = UserAssignment.objects.all()
    return render(request, 'userassignments/view_userassignments.html', {'user_assignments': user_assignments})


def view_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    return render(request, 'userassignments/view_userassignment.html', {'user_assignment': user_assignment})

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
        return redirect('view_userassignments')
    return render(request, 'userassignments/add_userassignment.html', {'assignments': assignments, 'users': users})

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
        
        return redirect('view_userassignments')
    
    return render(request, 'userassignments/edit_userassignment.html', {'user_assignment': user_assignment, 'assignments': assignments, 'users': users})

def delete_userassignment(request, user_assignment_id):
    user_assignment = get_object_or_404(UserAssignment, pk=user_assignment_id)
    if request.method == 'POST':
        user_assignment.delete()
        return redirect('view_userassignments')
    return render(request, 'userassignments/delete_userassignment.html', {'user_assignment': user_assignment})

def forgot_password(request): 
	return render(request,"registration/forgot-password.html")

def error_404(request):
	return render(request,"common/404.html")


def register(request):
    context ={}

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()
            # print(request.POST["password"]," ",form["password"])
            # return redirect("registerSuccess",permanent=True)
            return render(request, "registration/register_success.html")
    else:
        form = RegisterForm()

    context['form']= form
    return render(request, "registration/register.html")

def reg_success(request):
	return render(request,"registration/register_success.html")

def login(request):
	print(request.POST,"reqjjd")
	form=LoginForm(request.POST or None) # always send the data to teh class for validation
	print('form.is_valid()',form.is_valid())
	if form.is_valid():
		if request.method == "POST":
			username = form.cleaned_data['username']
			password = request.POST['password']

        #sql
			if Student.objects.filter(student_id=username).exists():
				user=Student.objects.get(student_id=username)
              
				if check_password(password, user.password):
					request.session['user_id']=user.student_id
					
					return redirect("home")
	else:
		return render(request,"registration/login.html",{'form':form})

def getUser(request):
	return Student.objects.filter(student_id=request.session['user_id'])

def home(request):
	if 'user_id' in request.session and getUser(request):
		user = getUser(request)
		# print(user)
		return render(request,'common/home.html')
	else:
		return redirect("login")
#always call get user and check for session id and then move to next page
def logout(request):
	user=getUser(request)
	del request.session["user_id"]
	context ={}
	form = LoginForm(request.POST or None)
	context["form"]=form
	return render(request,"registration/login.html",context)
		

# # Create
# def create_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         user = User.objects.create(username=username, password=password, email=email)
#         return redirect('user_detail', pk=user.pk)
#     return render(request, 'create_user.html')

# # Read
# def user_detail(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     return render(request, 'user_detail.html', {'user': user})

# # Update
# def update_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         user.username = request.POST.get('username')
#         user.password = request.POST.get('password')
#         user.email = request.POST.get('email')
#         user.save()
#         return redirect('user_detail', pk=user.pk)
#     return render(request, 'update_user.html', {'user': user})

# # Delete
# def delete_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'users/delete_user.html', {'user': user})

	


