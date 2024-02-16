from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import  check_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import User

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

def edit_user(request, user_id):
    user_data = {'id': user_id, 'username': 'example_username', 'email': 'example@email.com', 'first_name': 'John', 'last_name': 'Doe'}
    return render(request, 'edit_user.html', {'user_data': user_data})


def view_subscriptions(request):
	return render(request,"view_subscriptions.html")

def view_courses(request):
	return render(request,"view_courses.html")

def view_enrollments(request):
	return render(request,"view_enrollments.html")

def view_assignments(request):
	return render(request,"view_assignments.html")

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

	


