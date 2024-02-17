from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import  check_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Course,Assignment,Enrollment
from django.urls import reverse
from django.http import HttpResponseBadRequest
# from .forms import EnrollmentForm
# from .forms import AssignmentForm

# Create your views here.


from .forms import RegisterForm,LoginForm
from .models import Student


def index(request):
	return render(request,"index.html")

def view_users(request):
    user_data = [
        {'id': 1, 'username': 'shiv', 'email': 'sivabalanP@email.com', 'first_name': 'siva', 'last_name': 'balan'}, 
        {'id': 2, 'username': 'kumar', 'email': 'kumar@email.com', 'first_name': 'kumara', 'last_name': 'guru'}
    ]
    return render(request, 'view_users.html', {'user_data': user_data})

def view_user(request, user_id):
    user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
    return render(request, 'view_user.html', {'user_data': user_data})

def add_user(request):
    # user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
    return render(request, 'add_user.html')

def edit_user(request, user_id):
    user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
    return render(request, 'edit_user.html', {'user_data': user_data})

def delete_user(request, user_id):
	user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
	return render(request,'delete_user.html',{'user_data': user_data} )


def view_subscriptions(request):
	return render(request,"view_subscriptions.html")


def view_courses(request):
	# course_data = [
    #     {'id': 1, 'name': 'Mate in One', 'description': 'Mate in one course'}, 
	# 	{'id': 2, 'name': 'Mate in Two', 'description': 'Mate in two course'}, 
	# 	{'id': 3, 'name': 'Mate in Three', 'description': 'Mate in three course'}, 
	# 	{'id': 4, 'name': 'Forced Checkmate', 'description': 'Forced checkmate patterns course'}, 
    # ]
	course_data = Course.objects.all()
	print(course_data)
	return render(request,"view_courses.html",{'course_data': course_data} )

def view_course(request, course_id):
    course_data = get_object_or_404(Course, id=course_id)
    return render(request, 'view_course.html', {'course_data': course_data})

def add_course(request):
    # user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
	if request.method == 'POST':
		course_name = request.POST.get('course_name')
		course_description = request.POST.get('course_description')
		course = Course.objects.create(course_name=course_name, course_description=course_description)
		return redirect(reverse('view_course', kwargs={'course_id': course.id}))
	return render(request, 'add_course.html')

def edit_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.course_name = request.POST.get('course_name')
		course_data.course_description = request.POST.get('course_description')
		course_data.save()
		return redirect(reverse('view_course', kwargs={'course_id': course_id}))
	return render(request, 'edit_course.html', {'course_data': course_data})



def delete_course(request, course_id):
	course_data = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		course_data.delete()
		return redirect('view_courses')
	# course_data = {'id': course_id, 'name': 'Mate in One', 'description': 'Mate in one course'}
	return render(request,'delete_course.html',{'course_data': course_data} )



def view_enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, "view_enrollments.html", {'enrollments': enrollments})

def view_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    return render(request, 'view_enrollment.html', {'enrollment': enrollment})

def add_enrollment(request):
    courses = Course.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        enrollment_date = request.POST.get('enrollment_date')
        
        enrollment = Enrollment.objects.create(user_id=user_id, course_id=course_id, enrollment_date=enrollment_date)
        
        return redirect(reverse('view_enrollment', kwargs={'enrollment_id': enrollment.id}))
    return render(request, 'add_enrollment.html', {'courses': courses, 'users': users})

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
    
    return render(request, 'edit_enrollment.html', {'enrollment_data': enrollment_data, 'courses': courses, 'users': users})

def delete_enrollment(request, enrollment_id):
    enrollment_data = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment_data.delete()
        return redirect('view_enrollments')
    
    return render(request, 'delete_enrollment.html', {'enrollment_data': enrollment_data})

def view_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'view_assignments.html', {'assignments': assignments})

def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    return render(request, 'view_assignment.html', {'assignment': assignment})

# def add_assignment(request):
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('view_assignments')
#     else:
#         form = AssignmentForm()
#     return render(request, 'add_assignment.html', {'form': form})

# def edit_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, pk=assignment_id)
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, instance=assignment)
#         if form.is_valid():
#             form.save()
#             return redirect('view_assignments')
#     else:
#         form = AssignmentForm(instance=assignment)
#     return render(request, 'edit_assignment.html', {'form': form, 'assignment': assignment})

# def delete_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, pk=assignment_id)
#     if request.method == 'POST':
#         assignment.delete()
#         return redirect('view_assignments')
#     return render(request, 'delete_assignment.html', {'assignment': assignment})


def view_userassignments(request):
	return render(request,"view_userassignments.html")




def forgot_password(request): 
	return render(request,"forgot-password.html")

def error_404(request):
	return render(request,"404.html")

def charts(request):
	return render(request,"charts.html")

def tables(request):
	return render(request,"tables.html")

def register(request):
	context ={}

	# create object of form
	print("request",request)
	
	form = RegisterForm(request.POST or None)
	
	# # check if form data is valid
	if form.is_valid():
		# save the form data to model
		form.save()
		print(request.POST["password"]," ",form["password"])
		return redirect("registerSuccess",permanent=True)

	context['form']= form
	return render(request, "register.html", context)

def reg_success(request):
	return render(request,"registerSuccess.html")

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
		return render(request,"login.html",{'form':form})

def getUser(request):
	return Student.objects.filter(student_id=request.session['user_id'])

def home(request):
	if 'user_id' in request.session and getUser(request):
		user = getUser(request)
		# print(user)
		return render(request,'home.html')
	else:
		return redirect("login")
#always call get user and check for session id and then move to next page
def logout(request):
	user=getUser(request)
	del request.session["user_id"]
	context ={}
	form = LoginForm(request.POST or None)
	context["form"]=form
	return render(request,"login.html",context)
		

# Create
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create(username=username, password=password, email=email)
        return redirect('user_detail', pk=user.pk)
    return render(request, 'create_user.html')

# Read
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

# Update
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user_detail', pk=user.pk)
    return render(request, 'update_user.html', {'user': user})

# Delete
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'delete_user.html', {'user': user})

	


