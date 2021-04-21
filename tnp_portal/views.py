import time
from datetime import date, datetime, timedelta
from secrets import token_urlsafe
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from tnp_admin.models import Admin
from student.models import User
from tnp_admin.models import StudentPlaced, resetPassword


@never_cache
def login(request):
    if request.method == 'POST':
        user = request.POST['uname']
        password = request.POST['psw']

        admin = Admin.objects.filter(username=user, password=password)
        student = User.objects.filter(username=user, password=password)
        if student:
            request.session['student_login'] = True
            request.session['username'] = user
            return HttpResponseRedirect("/student/resume/")
        elif admin:
            request.session['admin_login'] = True
            request.session['admin_username'] = user
            return HttpResponseRedirect("/tnp_admin/")
        else:
            msg = {
                'error': "Invalid Id or Password"
            }
            return render(request, 'login.html', msg)

    elif 'admin_login' in request.session:
        return HttpResponseRedirect("/tnp_admin/")

    elif 'student_login' in request.session:
        return HttpResponseRedirect("/student/resume/")

    else:
        return render(request, 'login.html')


def placement(request):
    placed = StudentPlaced.objects.all()
    it = 0
    extc = 0
    etrx = 0
    comps = 0
    for place in placed:
        if place.branch == "Information Technology":
            it = it + 1
        elif place.branch == "Electronics & Telecommunication":
            extc = extc + 1
        elif place.branch == "Electronics":
            etrx = etrx + 1
        else:
            comps = comps + 1
    return render(request, 'placement_highlight.html', {'it': it, 'extc': extc, 'etrx': etrx, 'comps': comps})


@never_cache
def forgotPassword(request):
    if request.method == "POST":
        username = request.POST['uname']
        student = User.objects.filter(username=username)
        admin = Admin.objects.filter(username=username)
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
        getTime = time.strftime("%H:%M:%S", t)
        today = date.today()
        if student.exists():
            token = token_urlsafe(16)

            saveToken = resetPassword(username=username, token=token, time=current_time, getTime=getTime, date=today)
            saveToken.save()

            sendSupport = User.objects.get(username=username)
            email = EmailMessage('Account Recovery',
                                 '<p>We received an account recovery request for ' + sendSupport.username + '.</p><br><p>If you initiated this request, <a href="placementportal.pythonanywhere.com/recover?token=' + token + '">reset your password here.</a></p><br><p>If you did not initiate this account recovery request, just ignore this email. We’ll keep your account safe</p>',
                                 'tnpportal7@gmail.com', [sendSupport.username])
            email.content_subtype = "html"
            email.send()
            return render(request, 'forgot_password.html',
                          {'mailSent': "If you are an active user, a mail has been sent to your email Id."})
        elif admin.exists():
            token = token_urlsafe(16)

            saveToken = resetPassword(username=username, token=token, time=current_time, getTime=getTime, date=today)
            saveToken.save()

            sendAdmin = Admin.objects.get(username=username)
            email = EmailMessage('Account Recovery',
                                 '<p>We received an account recovery request for ' + sendAdmin.username + '.</p><br><p>If you initiated this request, <a href="placementportal.pythonanywhere.com/recover?token=' + token + '">reset your password here.</a></p><br><p>If you did not initiate this account recovery request, just ignore this email. We’ll keep your account safe</p>',
                                 'tnpportal7@gmail.com', [sendAdmin.username])
            email.content_subtype = "html"
            email.send()
            return render(request, 'forgot_password.html',
                          {'mailSent': "If you are an active user, a mail has been sent to your email Id."})
        else:
            return render(request, 'forgot_password.html',
                          {'mailSent': "If you are an active user, a mail has been sent to your email Id."})
    else:
        return render(request, 'forgot_password.html')


@never_cache
def recover(request):
    if request.GET.get('token'):
        token = request.GET.get('token')

        if resetPassword.objects.filter(token=token).exists():
            reset = resetPassword.objects.get(token=token)
            t = time.localtime()
            y = time.strftime("%H:%M:%S", t)
            x = reset.getTime

            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(y, FMT) - datetime.strptime(x, FMT)
            today = date.today()
            strToday = str(today)

            newdate1 = time.strptime(strToday, "%Y-%m-%d")
            newdate2 = time.strptime(reset.date, "%Y-%m-%d")
            print(tdelta.seconds)

            if tdelta.seconds < 1800 and newdate1 == newdate2:
                request.session['tokens'] = token
                return render(request, 'recover.html')
            else:
                reset.delete()
                return render(request, 'cannot_recover.html')
        else:
            return render(request, 'cannot_recover.html')
    elif request.method == "POST":

        session_token = request.session['tokens']
        user = resetPassword.objects.filter(token=session_token)

        if user.exists():
            passw = request.POST['passw']

            del request.session['tokens']
            request.session.modified = True

            user = resetPassword.objects.get(token=session_token)
            username = user.username

            user.delete()

            student = User.objects.filter(username=username)
            admin = Admin.objects.filter(username=username)

            if admin.exists():
                getAdmin = Admin.objects.get(username=username)
                getAdmin.password = passw
                getAdmin.save()
                return HttpResponseRedirect("/login/")

            if student.exists():
                getUser = User.objects.get(username=username)
                getUser.password = passw
                getUser.save()
                return HttpResponseRedirect("/login/")
        else:
            return render(request, 'cannot_recover.html')
    else:
        return HttpResponseRedirect("/error/")


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)