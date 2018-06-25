from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages
from django.contrib.messages import error

# render routes
def index(request):
    print("hello from index")
    return render(request,"user_dashboard/index.html")

def signin(request):
    if request.method == "POST":
        result = User.objects.validate_signin(request.POST)
        print("hello from User signin")
        if type(result) == User:
            print("hello from sigin")
            request.session['user_id'] = result.id
            messages.success(request, 'Successfully logged in!!!')
            if result.user_level == 9:
                return redirect(reverse('dd:dashadmin'))
            return redirect(reverse('dd:dash'))
        else:
            for err in result:
                messages.error(request,err)
    return render(request,"user_dashboard/signin.html")

def register(request):
    if request.method == "POST":        
        result = User.objects.validate(request.POST)
        
        if type(result) == User:
        # we can also do if type(result) == list, but we consider the best ones first
            request.session['user_id'] = result.id
            messages.success(request, 'Successfully registered!!!')
            if result.user_level == 9:
                return redirect(reverse('dd:dashadmin'))
            return redirect(reverse('dd:dash'))
        else:
            for err in result:
                messages.error(request, err)    
    print("hello from register")        
    return render(request,"user_dashboard/register.html")

def dashadmin(request):
    admin_display ={
        "users": User.objects.all()
    }
    print User.objects.all()
    return render(request,"user_dashboard/dashadmin.html", admin_display)

def dash(request):
    user_display ={
        "users": User.objects.all()
    }
    print User.objects.all()
    return render(request,"user_dashboard/dash.html", user_display)

def show(request, id):
    this_user = User.objects.get(id=id)
    # this_messages = this_user.received_messages.all().order_by("-created_at")
    # # Grouping done in views:
    # message_models = []
    # for message in this_messages:
    #     message_models.append(MessageModel(message,message.comments.all()))
    # print message_models    
    message_models = Message.objects.retrieve_comments_with_msg(this_user)
    show_data={
        "individual": this_user,
        "message_models": message_models
    }
    return render(request,"user_dashboard/show.html", show_data)

 
def logout(request):
    return redirect(reverse('dd:index'))

def add_new(request):
    print("in add neww user")
    return render(request,"user_dashboard/add_new.html")
    
def admin_edit_user_page(request, id):
    print("hello from admin edit user page")
    edit_data={
        'individual':User.objects.get(id=id)
    }
    return render(request,"user_dashboard/admin_edit_user_page.html", edit_data)

def post_message(request, id):
    logged_user = request.session['user_id']
    wall_user = User.objects.get(id=id)
    Message.objects.create(desc=request.POST['message_desc'], author= User.objects.get(id=logged_user), receiver=wall_user)
    return redirect(reverse('dd:show', kwargs={'id':id}))

def post_comment(request, indi_id, msg_id):
    posted_comment = request.POST['comment_desc']
    logged_user = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=msg_id)
    Comment.objects.create(desc=posted_comment, author=logged_user, message=message )
    return redirect(reverse('dd:show', kwargs={'id':indi_id}))


def admin_edit_user_info(request, id):
    if request.method == 'POST':
        result = User.objects.get(id=id)
        result.firstname = request.POST['first_name']
        result.lastname = request.POST['last_name']
        result.email = request.POST['email'] 
        if request.POST['user_level'] == "admin":
            result.user_level = 9
        else:
            result.user_level = 1
        result.save()
        return redirect(reverse('dd:dashadmin'))
    return redirect(reverse('dd:admin_edit_user_page', kwargs={'id':id}))

def admin_edit_user_pwd(request, id):
    if request.method == 'POST':
        result = User.objects.validate_user_pwd(request.POST, user_id=id)
        if type(result) == User:
            print("hello from admin edit user info")
            return redirect(reverse('dd:dashadmin'))
        else:
            for err in result:
                error(request, err, 'red')
    return redirect(reverse('dd:admin_edit_user_page', kwargs={'id':id}))
    

def edit_user_page(request):
    print User.objects.get(id=request.session['user_id'])
    print("hello from edit user page")
    edit_data={
        'individual':User.objects.get(id=request.session['user_id'])
    }
    return render(request,"user_dashboard/edit_user_page.html", edit_data)

def edit_user_info(request, id):
    if request.method == "POST":  
        result = User.objects.validate_user_info(request.POST, user_id=id)
        if type(result) == User:
            print("hello from edit user info")
            return redirect(reverse('dd:dash'))
        else:
            for err in result:
                error(request, err, 'red')
    return redirect(reverse('dd:edit_user_page'))

def edit_user_pwd(request, id):
    if request.method == "POST":  
        result = User.objects.validate_user_pwd(request.POST, user_id=id)
        if type(result) == User:
            print("hello from edit user info")
            return redirect(reverse('dd:dash'))
        else:
            for err in result:
                error(request, err, 'red')
    return redirect(reverse('dd:edit_user_page'))

def edit_user_desc(request, id):
    if request.method == "POST":  
        b = User.objects.get(id=id)
        b.desc = request.POST['desc']
        b.save()
        return redirect(reverse('dd:dash'))
    return redirect(reverse('dd:edit_user_page'))
