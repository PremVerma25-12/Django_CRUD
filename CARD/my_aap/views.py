from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import registration,Query
from django.db.models import Q
def userregistration(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if not all([name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "registration.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration.html")

        if registration.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "registration.html")

        registration.objects.create(name=name, email=email, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "registration.html")


def userlogin(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = registration.objects.get(email=email, password=password)
            data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,} 

            return render(request, "dashbord.html", {
                'pk':user.id,
                "name": user.name,
                "email": user.email,
                "data" : data
            })
        except registration.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

    return render(request, "login.html")

def query(req,x):
    # print(x)
    user=registration.objects.get(id=x)
    data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,} 
    return render(req,"dashbord.html",{'data':data,'query1':data})

def querydata(req,pk):
    # print(req.POST)
    # print(pk)
    name=req.POST.get('name')
    email=req.POST.get('email')
    query=req.POST.get('query')
    # print(name,email,query)
    Query.objects.create(name=name,email=email,query=query)
    user=registration.objects.get(id=pk)
    data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,} 
    return render(req,"dashbord.html",{'data':data})

def allquery(req,x):
    userdata=registration.objects.get(id=x)
    email=userdata.email
    aquery=Query.objects.filter(email=email)
    return render(req,'dashbord.html',{'data':userdata,'aquery':aquery})

def search(req,pk):
    searchdata = req.POST.get('search')
    userdata=registration.objects.get(id=pk)
    # data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,} 
    aquery = Query.objects.filter(Q(query__icontains=searchdata) & Q(email = userdata.email))
    return render(req,'dashbord.html',{'data':userdata,'aquery':aquery})

def logout_view(req):
    logout(req)
    return redirect('login')

def edit(req,id,pk):
    editdata = Query.objects.get(id = id)
    editqurey = editdata.query
    user=registration.objects.get(id=pk)
    data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,'editqurey': editqurey} 
    return render(req,"dashbord.html",{'data':data,'edit':editdata})
    
def updatedata(req,id,pk):
    if req.method == "POST":
        # name=req.POST.get('name')
        email=req.POST.get('email')
        updatequery=req.POST.get('query')
        olddata = Query.objects.get(id = id)    
        olddata.query = updatequery    
        olddata.save()
        userdata=registration.objects.get(id=pk)
        aquery=Query.objects.filter(email=email)
    return render(req,'dashbord.html',{'data':userdata,'aquery':aquery})



def delete(req , pk , id):
    deletequrey = Query.objects.get(id = id)
    deletequrey.delete()
    user=registration.objects.get(id=pk)
    data={'id':user.id,'name':user.name,'email':user.email,'password':user.password,}
    aquery=Query.objects.filter(email=user.email)
    return render(req,'dashbord.html',{'data':data,'aquery':aquery}) 
    

