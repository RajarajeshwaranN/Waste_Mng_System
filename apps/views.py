from django.shortcuts import render, redirect
import mysql.connector as sql

name=''
email=''
pwd=''
cnfpwd=''

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def signupaction(request):
    
    if request.method=="POST":
        try:
            m = sql.connect(host='localhost', user='root', passwd='root', database='waste')
            cursor = m.cursor()

            name = request.POST.get("full_name")
            email = request.POST.get("email")
            pwd = request.POST.get("password")
            cnfpwd = request.POST.get("confirm_password")

            c = "INSERT INTO user (full_name, email, password, confirm_password) VALUES (%s, %s, %s, %s)"
            cursor.execute(c, (name, email, pwd, cnfpwd))
            m.commit()
            print("Data inserted successfully!")
        except Exception as e:
            print("An error occurred:", e)
        finally:
            cursor.close()
            m.close()

    return render(request,'login.html')


def loginaction(request):
    global email,pwd
    if request.method=="POST":
        m=sql.connect(host='localhost',user='root',passwd='root',database='waste')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                email=value
            if key=="password":
                pwd=value
            
            
        c="select * from user where email='{}' and password='{}'".format(email,pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            return render(request,"error.html")
        else:
            return render(request,"index.html")
        

    return render(request,'login.html')

