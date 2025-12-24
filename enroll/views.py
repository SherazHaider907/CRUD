from django.shortcuts import render, HttpResponseRedirect
from .forms import UserForm
from .models import User
from django.db import transaction
# Create your views here.

# This function view to add and show user
def add_show(request):
    if request.method == 'POST':
        # Handle form submission logic here
        fm = UserForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw =  fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            fm = UserForm()  # Clear the form after saving

        # second method to save form data directly
        # if fm.is_valid():
        #     fm.save()
        #     fm = UserForm()  # Clear the form after saving
    else:
        fm = UserForm()  
    UserFrom =User.objects.all() # fetch all records from User table and send to template
    return render(request, 'enroll/add_and_show.html',{'form': fm, 'user': UserFrom})


# This function  update/Edit data
def update_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = UserForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm = UserForm(instance=pi)
    return render(request, 'enroll/update.html', {'form': fm}) 


# This function  delete data
def delete_data(request, id):
    if request.method == 'POST':
        with transaction.atomic():
            # Delete the requested user
            User.objects.get(pk=id).delete()
            
            # Get all users with id greater than the deleted id
            users_to_update = User.objects.filter(id__gt=id).order_by('id')
            
            # Update their IDs to fill the gap
            for index, user in enumerate(users_to_update, start=id):
                User.objects.filter(id=user.id).update(id=index)
                
        return HttpResponseRedirect('/') 
    
# End of views.py 

# # This function  delete data
# def delete_data(request, id):
#     if request.method == 'POST':
#         pi = User.objects.get(pk=id)
#         pi.delete()
#         return HttpResponseRedirect ('/')