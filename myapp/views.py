import base64
import random
import smtplib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views.decorators.cache import never_cache

from myapp.classify_alzheimers import classify_image_alzheimers
from myapp.classify_bone_fracture import classify_image
from myapp.classify_lung_cancer import classify_image_lung_cancer
from .models import *


    # admin details
    # username : admin@gmail.com
    # password : superuser


# Create your views here.

def loginn(request):
    return render(request, "login.html")
def loginn_post(request):
    un=request.POST['email']
    ps=request.POST['password']
    data=authenticate(request, username=un, password=ps)
    if data is not None:
        if data.is_superuser:
            login(request, data)
            return HttpResponse("<script>alert('Welcome admin');window.location='/adm_home'</script>")
        return HttpResponse("<script>alert('Unauthorized details');window.location='/'</script>")
    return HttpResponse("<script>alert('Invalid details');window.location='/'</script>")

@login_required(login_url='/')
@never_cache
def adm_home(request):
    return render(request, "admin/index.html")
    # return render(request, "admin/adminhome.html")

@login_required(login_url='/')
@never_cache
def adm_change_password(request):
    return render(request, "admin/change_password.html")

@login_required(login_url='/')
@never_cache
def adm_change_password_post(request):
    current=request.POST['current']
    neww=request.POST['neww']
    confirm=request.POST['confirm']
    data = check_password(current,request.user.password)
    if data:
        if neww == confirm:
            obj = request.user
            obj.set_password(neww)
            obj.save()
            return HttpResponse("<script>alert('Password Updated');window.location='/'</script>")
        return HttpResponse("<script>alert('Password Must Be Equal');window.location='/adm_change_password'</script>")
    return HttpResponse("<script>alert('Invalid Credentials');window.location='/adm_change_password'</script>")


@login_required(login_url='/')
@never_cache
def adm_send_notification(request):
    return render(request, "admin/send_notification.html")

@login_required(login_url='/')
@never_cache
def adm_send_notification_post(request):
    notific=request.POST['notification']
    obj=m_notify()
    obj.notification=notific
    obj.date=datetime.now().date()
    obj.save()
    return HttpResponse("<script>alert('notification sent succesfull');window.location='/adm_send_notification'</script>")


@login_required(login_url='/')
@never_cache
def adm_view_hospital(request):
    data=hospital.objects.all()
    return render(request, "admin/view_hospital.html", {"data":data})

@login_required(login_url='/')
@never_cache
def adm_viewfeedback(request):
    data=v_feedback.objects.all()
    return render(request, "admin/viewfeedback.html", {"data":data})

@login_required(login_url='/')
@never_cache
def adm_viewnotification(request):
    data=m_notify.objects.all()
    return render(request, "admin/viewnotification.html", {"data":data})

@login_required(login_url='/')
@never_cache
def adm_delete_notification(request, id):
    m_notify.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('notification deleted');window.location='/adm_viewnotification'</script>")




def logouts(request):
    logout(request)
    return HttpResponse("<script>alert('Logout');window.location='/'</script>")


########################            HOSPITAL

def hosp_login(request):
    un=request.POST['un']
    ps=request.POST['ps']
    data=authenticate(request, username=un, password=ps)
    if data is not None:
        print("hospital")
        login(request, data)
        data2=hospital.objects.get(LOGIN_id=request.user.id)
        print(data2.id)
        return JsonResponse({"status": "ok", "hid":str(data2.id)})
    return JsonResponse({"status": "no"})

def hosp_register(request):
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    district=request.POST['district']
    password=request.POST['password']
    lati=request.POST['lati']
    longi=request.POST['longi']
    image=request.POST['image']
    if User.objects.filter(username=email).exists():
        return JsonResponse({'status':'Exist'})

    dt=datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg"
    with open(r"C:\Users\sanoh\Documents\medi ai\web\AI_POWERED_MEDICAL_PREDICTION\myapp\static\images\\"+dt, "wb") as file:
        data=base64.b64decode(image)
        file.write(data)
        file.close()
    path="/static/images/"+dt

    obj=User()
    obj.username=email
    obj.password=make_password(password)
    obj.save()
    obj.groups.add(Group.objects.get(name="hospital"))


    obj2=hospital()
    obj2.LOGIN=obj
    obj2.name=name
    obj2.email=email
    obj2.phone=phone
    obj2.place=place
    obj2.district=district
    obj2.latitude=lati
    obj2.longitude=longi
    obj2.proof=path
    obj2.save()
    return JsonResponse({"status": "ok"})


def hosp_view_feedback(request):
    hid = request.POST['hid']
    data=v_feedback.objects.all().order_by("-id")
    ar=[]
    for i in data:
        ar.append({
            "date":i.date, "feedback":i.feedback, "hospname":i.HOSPITAL.name
        })
    return JsonResponse({"status":"ok", "data":ar})


def hosp_view_notify(request):
    data=m_notify.objects.all()
    ar=[]
    for i in data:
        ar.append({
            "date":i.date, "notification":i.notification
        })
    return JsonResponse({"status":"ok", "data":ar})

def hosp_view_profile(request):
    hid=request.POST['hid']
    data=hospital.objects.filter(id=hid)
    ar=[]
    for i in data:
        ar.append({
            "name":i.name, "email":i.email, "phone":i.phone, "place":i.place, "district":i.district
        })
    return JsonResponse({"status":"ok", "data":ar})

def hosp_view_results(request):
    hid=request.POST['hid']
    data=prediction.objects.filter(HOSPITAL_id=hid).order_by("-id")
    ar=[]
    for i in data:
        ar.append({
            "date":i.date, "patient":i.patient_name, "phone":i.phone, "prediction":i.prediction_type,
            "algorithm":i.algorithm, "image":i.image, "result":i.result
        })
    return JsonResponse({"status":"ok", "data":ar})



def alzheimers_predict(request):
        uploaded_file = request.FILES['file']
        name = request.POST['name']
        phone = request.POST['phone']
        uid = request.POST['uid']
        print(name, phone)
        print(uploaded_file, "pppppppppppppppppp")
        dt = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        if uploaded_file:
            try:
                # Save the file in the MEDIA_ROOT directory
                with open(f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}', 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
            except Exception as e:
                pass

        path = f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}'
        res, scr=classify_image_alzheimers(path)
        obj=prediction()
        obj.date=datetime.now().date()
        obj.prediction_type="Alzheimers Detection"
        obj.algorithm="CNN"
        obj.image=f"/media/uploads/{dt}"
        obj.result=res
        obj.patient_name=name
        obj.phone=phone
        obj.HOSPITAL_id=uid
        obj.save()

        return JsonResponse({"res": "true", "result":res})

def bone_fracture_predict(request):
        uploaded_file = request.FILES['file']
        name = request.POST['name']
        phone = request.POST['phone']
        uid = request.POST['uid']
        print(name, phone)
        print(uploaded_file, "pppppppppppppppppp")
        dt = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        if uploaded_file:
            try:
                # Save the file in the MEDIA_ROOT directory
                with open(f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}', 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
            except Exception as e:
                pass

        path = f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}'
        res, scr=classify_image(path)
        obj=prediction()
        obj.date=datetime.now().date()
        obj.prediction_type="Bone Fracture Detection"
        obj.algorithm="CNN"
        obj.image=f"/media/uploads/{dt}"
        obj.result=res
        obj.patient_name=name
        obj.phone=phone
        obj.HOSPITAL_id=uid
        obj.save()

        return JsonResponse({"res": "true", "result":res})

def lung_cancer_predict(request):
        uploaded_file = request.FILES['file']
        name = request.POST['name']
        phone = request.POST['phone']
        uid = request.POST['uid']
        print(name, phone)
        print(uploaded_file, "pppppppppppppppppp")
        dt = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        if uploaded_file:
            try:
                # Save the file in the MEDIA_ROOT directory
                with open(f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}', 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
            except Exception as e:
                pass

        path = f'C:/Users/sanoh/Documents/medi ai/web/AI_POWERED_MEDICAL_PREDICTION/media/uploads/{dt}'
        res, scr=classify_image_lung_cancer(path)
        obj=prediction()
        obj.date=datetime.now().date()
        obj.prediction_type="Lung Cancer Detection"
        obj.algorithm="CNN"
        obj.image=f"/media/uploads/{dt}"
        obj.result=res
        obj.patient_name=name
        obj.phone=phone
        obj.HOSPITAL_id=uid
        obj.save()

        return JsonResponse({"res": "true", "result":res})



def change_password_hospital(request):
    current = request.POST['current']
    neww = request.POST['neww']
    confirm = request.POST['confirm']
    hid = request.POST['hid']
    passw = request.POST['password']
    if passw == current:
        if neww == confirm:
            obj = hospital.objects.get(id=hid).LOGIN_id
            User.objects.filter(id=obj).update(password = make_password(neww))
            return JsonResponse({'status':'ok'})
        return JsonResponse({'status':'invalid'})
    return JsonResponse({'status':'invalid'})




#######  web forgot pass

def forgotpassword(request):
    return render(request,"forgotpassword.html")
def forgotpasswordbuttonclick(request):
    email = request.POST['textfield']
    if User.objects.filter(username=email).exists():
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        sender_email = "get.mediai.health@gmail.com"
        receiver_email = email  # change to actual recipient
        app_password = "mizv brbx yldj wcuw"  # App Password from Google
        pwd = str(random.randint(1100,9999))  # Example password to send
        request.session['otp'] = pwd
        request.session['email'] = email

        # Setup SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Your OTP"

        # Plain text (backup)
        # text = f"""
        # Hello,

        # Your password for Smart Donation Website is: {pwd}

        # Please keep it safe and do not share it with anyone.
        # """

        # HTML (attractive)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #ffffff; -webkit-font-smoothing: antialiased;">

            <div style="max-width: 440px; margin: 40px auto; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;">

                <!-- Simple Header with brand name only -->
                <div style="padding: 32px 32px 8px 32px;">
                    <div style="font-size: 24px; font-weight: 600; color: #1e293b;">MEDI <span style="font-weight: 400; color: #3b82f6;">AI</span></div>
                </div>

                <!-- Main Content -->
                <div style="padding: 8px 32px 24px 32px;">

                    <!-- Greeting -->
                    <div style="margin-bottom: 24px;">
                        <h1 style="font-size: 20px; font-weight: 600; color: #0f172a; margin: 0 0 4px 0;">Verification code</h1>
                        <p style="font-size: 15px; color: #475569; margin: 0; line-height: 1.5;">Hello, use the following code to complete your login</p>
                    </div>

                    <!-- OTP Display - Clean and prominent -->
                    <div style="margin-bottom: 28px;">
                        <div style="background: #f8fafc; border-radius: 16px; padding: 24px; text-align: center; border: 1px solid #e2e8f0;">
                            <div style="font-size: 42px; font-weight: 600; color: #0f172a; letter-spacing: 12px; font-family: 'Inter', monospace;">{pwd}</div>
                            <div style="font-size: 12px; color: #64748b; margin-top: 12px; letter-spacing: 0.3px;">ONE-TIME PASSWORD</div>
                        </div>
                    </div>

                    <!-- Simple Info -->
                    <div style="margin-bottom: 28px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                            <span style="width: 4px; height: 4px; background: #3b82f6; border-radius: 50%;"></span>
                            <span style="font-size: 14px; color: #334155;">Code expires in 10 minutes</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="width: 4px; height: 4px; background: #3b82f6; border-radius: 50%;"></span>
                            <span style="font-size: 14px; color: #334155;">Valid for account verification</span>
                        </div>
                    </div>

                    <!-- Security Message -->
                    <div style="background: #fff7ed; border-radius: 12px; padding: 16px; margin-bottom: 8px;">
                        <p style="font-size: 13px; color: #9a3412; margin: 0; line-height: 1.5;">
                            <span style="font-weight: 600;">Never share this code</span> — MEDI AI will never ask for it.
                        </p>
                    </div>

                    <!-- Divider -->
                    <div style="height: 1px; background: #e2e8f0; margin: 24px 0 20px 0;"></div>
                </div>

                <!-- Simple Footer -->
                <div style="padding: 20px 32px 28px 32px; background: #f8fafc; border-top: 1px solid #e2e8f0;">
                    <p style="font-size: 12px; color: #64748b; margin: 0 0 4px 0;">© 2024 MEDI AI. All rights reserved.</p>
                    <p style="font-size: 11px; color: #94a3b8; margin: 0;">This is an automated message, please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Attach both versions
        # msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Send email
        server.send_message(msg)
        print("✅ Email sent successfully!")

        # Close connection
        server.quit()
        return HttpResponse("<script>window.location='/otp'</script>")
    else:
        return HttpResponse("<script>alert('Email not found');window.location='/forgotpassword'</script>")


def otp(request):
    return render(request,"otp.html")
def otpbuttonclick(request):
    otp  = request.POST["textfield"]
    if otp == str(request.session['otp']):
        return HttpResponse("<script>window.location='/forgotpswdpswed'</script>")
    else:
        return HttpResponse("<script>alert('incorrect otp');window.location='/otp'</script>")

def forgotpswdpswed(request):
    return render(request,"forgotpswdpswed.html")
def forgotpswdpswedbuttonclick(request):
    np = request.POST["password"]
    User.objects.filter(username=request.session['email']).update(password=make_password(np))
    return HttpResponse("<script>alert('password has been changed');window.location='/' </script>")


######## flutter forgot

def forgotemail(request):
    import random
    import smtplib
    email = request.POST['email']
    print(email)
    data = User.objects.filter(username=email)
    print(data)
    if data.exists():
        otp = str(random.randint(000000, 999999))
        print(otp)
        # *✨ Python Email Codeimport smtplib*

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        try:
            sender_email = "get.mediai.health@gmail.com"
            receiver_email = email  # change to actual recipient
            app_password = "mizv brbx yldj wcuw"
            # Setup SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            # Create the email
            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = "🔑 Forgot Password "

            # Plain text (backup)
            # text = f"""
            # Hello,

            # Your password for Smart Donation Website is: {pwd}

            # Please keep it safe and do not share it with anyone.
            # """

            # HTML (attractive)
            html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Password Reset OTP</title>
                </head>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">
                            🔐 MEDI AI
                        </h1>
                    </div>

                    <div style="background-color: #f9f9f9; padding: 40px 30px; border-radius: 0 0 10px 10px; 
                                border: 1px solid #eaeaea;">

                        <h2 style="color: #2d3748; margin-top: 0;">Password Reset Request</h2>

                        <p style="color: #4a5568; font-size: 16px;">
                            Hello,
                        </p>

                        <p style="color: #4a5568; font-size: 16px;">
                            You requested to reset your password. Use the OTP below to proceed:
                        </p>

                        <div style="background: white; border-radius: 8px; padding: 20px; 
                                    text-align: center; margin: 30px 0; border: 2px dashed #cbd5e0;">
                            <div style="font-size: 32px; font-weight: bold; letter-spacing: 10px; 
                                        color: #2c7be5; margin: 10px 0;">
                                {otp}
                            </div>
                            <div style="font-size: 14px; color: #718096; margin-top: 10px;">
                                (Valid for 10 minutes)
                            </div>
                        </div>

                        <p style="color: #4a5568; font-size: 16px;">
                            Enter this code on the password reset page to complete the process.
                        </p>

                        <div style="background-color: #fef3c7; border-left: 4px solid #d97706; 
                                    padding: 15px; margin: 25px 0; border-radius: 4px;">
                            <p style="color: #92400e; margin: 0; font-size: 14px;">
                                ⚠️ <strong>Security tip:</strong> Never share this OTP with anyone. 
                                Our team will never ask for your password or OTP.
                            </p>
                        </div>

                        <p style="color: #718096; font-size: 14px;">
                            If you didn't request this password reset, please ignore this email or 
                            contact our support team if you have concerns.
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="text-align: center; color: #a0aec0; font-size: 12px;">
                            This is an automated email from MEDI AI System.<br>
                            © {datetime.now().year} MEDI AI. All rights reserved.
                        </p>

                    </div>
                </body>
                </html>
                """

            # Attach both versions
            # msg.attach(MIMEText(text, "plain"))
            msg.attach(MIMEText(html, "html"))

            # Send email
            server.send_message(msg)
            print("✅ Email sent successfully!", otp)

            # Close connection
            server.quit()

        except Exception as e:
            print("❌ Error loading email credentials:", e)
            return JsonResponse({'status': "ok", 'otpp': otp})

        return JsonResponse({'status': 'ok', 'otpp': otp})
    return JsonResponse({'status': "not found"})


def forgotpass(request):
    email = request.POST['email']
    npass = request.POST['password']
    cpass = request.POST['confirmpassword']
    print(email, npass, cpass)
    if npass == cpass:
        User.objects.filter(username=email).update(password=make_password(npass))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'})


def hospital_send_feedback(request):
    hid=request.POST['hid']
    feed=request.POST['feed']
    data=v_feedback.objects.filter(HOSPITAL_id=hid)
    if data.exists():
        print("Previous feedback exists. Making updates in previous feedback.")
        data=data[0]
        data.feedback=feed
        data.date=datetime.now().date()
        data.save()
    else:
        print("Sending first feedback.")
        obj=v_feedback()
        obj.date=datetime.now().date()
        obj.feedback=feed
        obj.HOSPITAL_id=hid
        obj.save()
    return JsonResponse({'status': 'ok'})


@login_required
@never_cache
def adm_edit_hospital(request):
    data=hospital.objects.all()
    return render(request, "admin/edit_hospital.html", {"data":data})


@login_required
@never_cache
def adm_delete_hospital(request, id):
    hospital.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Hospital deleted');window.location='/adm_edit_hospital';</script>")

