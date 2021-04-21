from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.template.loader import get_template
from django.views.decorators.cache import never_cache
from student.models import User
from student.models import Resume
from django.http import HttpResponse
from django.views.generic import View
from tnp_admin.models import StudentsEligible, Company, StudentPlaced
from .utils import render_to_pdf


@never_cache
def resume(request):
    if not request.session.get('student_login'):
        return HttpResponseRedirect("/login/")
    else:
        if request.method == 'POST':
            user = request.session['username']
            hn = request.POST['hn'].strip()
            number = request.POST['id_no'].strip()
            lastname = request.POST['lastname'].strip()
            firstname = request.POST['firstname'].strip()
            middlename = request.POST['middlename'].strip()
            branch = request.POST['branch']
            gender = request.POST['gender']
            date = request.POST['dob']
            languages = request.POST['languages']
            address = request.POST['address']
            phone = request.POST['phoneInput']
            objective = request.POST['objective']

            if request.POST.get('diploma') is None:
                sem1 = request.POST['sem1'].strip()
                sem1f = request.FILES.get('sem1f')
                sem2 = request.POST['sem2'].strip()
                sem2f = request.FILES.get('sem2f')

                hsc_marks = request.POST['hsc'].strip()
                hscf = request.FILES.get('hscf')
                hsc_institute = request.POST['hsc_inst']
                hsc_year = request.POST['hsc_year'].strip()
            else:
                diploma = request.POST['diplo'].strip()
                diploma_inst = request.POST['diploi']
                diploma_year = request.POST['diploy'].strip()
                diplomaf = request.FILES.get('diplof')

            sem3 = request.POST['sem3'].strip()
            sem3f = request.FILES.get('sem3f')
            sem4 = request.POST['sem4'].strip()
            sem4f = request.FILES.get('sem4f')
            sem5 = request.POST['sem5'].strip()
            sem5f = request.FILES.get('sem5f')
            sem6 = request.POST['sem6'].strip()
            sem6f = request.FILES.get('sem6f')
            sem7 = request.POST['sem7'].strip()
            sem7f = request.FILES.get('sem7f')
            sem8 = request.POST['sem8'].strip()
            sem8f = request.FILES.get('sem8f')
            aggregate = request.POST['aggregate'].strip()
            ssc_marks = request.POST['ssc'].strip()
            sscf = request.FILES.get('sscf')
            ssc_institute = request.POST['ssc_inst']
            ssc_year = request.POST['ssc_year']
            be_proj = request.POST['be_proj']
            te_proj = request.POST['te_proj']
            tech_prof = request.POST['tech_prof']
            awards = request.POST['awards']
            hobbies = request.POST['hobbies']

            name = hn + " " + lastname + " " + firstname + " " + middlename
            passname = lastname + " " + firstname + " " + middlename

            myround = lambda x: float(int(x)) if int(x) == x else float(int(x) + 1)

            MAX_UPLOAD_SIZE = 1048576

            if float(aggregate) < 7.00:
                spercs = 7.1 * float(aggregate) + 12
                sperc = myround(spercs)
            else:
                spercs = 7.4 * float(aggregate) + 12
                sperc = myround(spercs)

            error = []

            if number.isnumeric() == False:
                error.append("Invalid ID Number.")

            if phone.isnumeric() == False:
                error.append("Invalid Contact Number (10 digits start with 9/8/7).")

            if len(phone) < 10:
                error.append("Invalid Contact Number (10 digits start with 9/8/7).")

            if (sem1 != "" and sem1f is None) or (sem1 == "" and sem1f is not None):
                error.append("Sem 1 Marks or File missing.")

            if (sem2 != "" and sem2f is None) or (sem2 == "" and sem2f is not None):
                error.append("Sem 2 Marks or File missing.")

            if (sem3 != "" and sem3f is None) or (sem3 == "" and sem3f is not None):
                error.append("Sem 3 Marks or File missing.")

            if (sem4 != "" and sem4f is None) or (sem4 == "" and sem4f is not None):
                error.append("Sem 4 Marks or File missing.")

            if (sem5 != "" and sem5f is None) or (sem5 == "" and sem5f is not None):
                error.append("Sem 5 Marks or File missing.")

            if (sem6 != "" and sem6f is None) or (sem6 == "" and sem6f is not None):
                error.append("Sem 6 Marks or File missing.")

            if (sem7 != "" and sem7f is None) or (sem7 == "" and sem7f is not None):
                error.append("Sem 7 Marks or File missing.")

            if (sem8 != "" and sem8f is None) or (sem8 == "" and sem8f is not None):
                error.append("Sem 8 Marks or File missing.")

            if sem3 != "":
                if any(c.isalpha() for c in sem3) == True or float(sem3) > 10:
                    error.append("Invalid Sem 3 marks.")

            if sem4 != "":
                if any(c.isalpha() for c in sem4) == True or float(sem4) > 10:
                    error.append("Invalid Sem 4 marks.")

            if sem5 != "":
                if any(c.isalpha() for c in sem5) == True or float(sem5) > 10:
                    error.append("Invalid Sem 5 marks.")

            if sem6 != "":
                if any(c.isalpha() for c in sem6) == True or float(sem6) > 10:
                    error.append("Invalid Sem 6 marks.")

            if sem7 != "":
                if any(c.isalpha() for c in sem7) == True or float(sem7) > 10:
                    error.append("Invalid Sem 7 marks.")

            if sem8 != "":
                if any(c.isalpha() for c in sem8) == True or float(sem8) > 10:
                    error.append("Invalid Sem 8 marks.")

            if any(c.isalpha() for c in aggregate) == True or float(aggregate) > 10:
                error.append("Invalid Aggregate marks.")

            if request.POST.get('diploma') is None:
                diploma_check = "no"
                if sem1 == "" or sem1f is None:
                    error.append("Sem 1 marks are mandatory.")
                if sem2 == "" or sem2f is None:
                    error.append("Sem 2 marks are mandatory.")
                if sem1 != "":
                    if any(c.isalpha() for c in sem1) == True or float(sem1) > 10:
                        error.append("Invalid Sem 1 marks.")
                if sem2 != "":
                    if any(c.isalpha() for c in sem2) == True or float(sem2) > 10:
                        error.append("Invalid Sem 2 marks.")
                if hsc_marks == "":
                    error.append("HSC marks are mandatory.")
                if any(c.isalpha() for c in hsc_marks) == True or float(hsc_marks) > 100:
                        error.append("Invalid HSC marks.")
                if hscf is None:
                    error.append("HSC marksheet is mandatory.")
                if hsc_institute == "":
                    error.append("HSC institute is mandatory.")
                if hsc_year.isnumeric() == False:
                    error.append("HSC Passing year is invalid.")
                if hscf is not None:
                    if hscf.size > MAX_UPLOAD_SIZE:
                        error.append("HSC file upload size less than 1.0 MB")

            else:
                diploma_check = "yes"
                if diploma == "":
                    error.append("Diploma marks are mandatory.")
                if any(c.isalpha() for c in diploma) == True or float(diploma) > 100:
                    error.append("Invalid Diploma marks.")
                if diplomaf is None:
                    error.append("Diploma marksheet is mandatory.")
                if diploma_inst == "":
                    error.append("Diploma institute is mandatory.")
                if diploma_year.isnumeric() == False:
                    error.append("Diploma Passing year is invalid.")
                if diplomaf is not None:
                    if (not diplomaf.name.endswith('.png', '.jpg', '.jpeg')) or diplomaf.size > MAX_UPLOAD_SIZE:
                        error.append("Diploma file upload size less than 1.0 MB")

            if ssc_marks == "":
                error.append("SSC marks are mandatory.")
            if any(c.isalpha() for c in ssc_marks) == True or float(ssc_marks) > 100:
                error.append("Invalid SSC marks.")
            if sscf is None:
                error.append("SSC marksheet is mandatory.")
            if ssc_institute == "":
                error.append("SSC institute is mandatory.")
            if ssc_year.isnumeric() == False:
                error.append("SSC Passing year is invalid.")

            if sem1f is not None:
                if sem1f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 1 file upload size less than 1.0 MB")

            if sem2f is not None:
                if sem2f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 2 file upload size less than 1.0 MB")

            if sem3f is not None:
                if sem3f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 3 file upload size less than 1.0 MB")

            if sem4f is not None:
                if sem4f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 4 file upload size less than 1.0 MB")

            if sem5f is not None:
                if sem5f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 5 file upload size less than 1.0 MB")

            if sem6f is not None:
                if sem6f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 6 file upload size less than 1.0 MB")

            if sem7f is not None:
                if sem7f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 7 file upload size less than 1.0 MB")

            if sem8f is not None:
                if sem8f.size > MAX_UPLOAD_SIZE:
                    error.append("Sem 8 file upload size less than 1.0 MB")

            if sscf is not None:
                if sscf.size > MAX_UPLOAD_SIZE:
                    error.append("SSC file upload size less than 1.0 MB")

            if sem3 == '':
                sem3 = None
            if sem4 == '':
                sem4 = None
            if sem5 == '':
                sem5 = None
            if sem6 == '':
                sem6 = None
            if sem7 == '':
                sem7 = None
            if sem8 == '':
                sem8 = None

            if len(error) > 0:
                if request.POST.get('diploma') is None:
                    msg = {
                        "lastname": lastname,
                        "firstname": firstname,
                        "middlename": middlename,
                        "branch": branch,
                        "gender": gender,
                        "date": date,
                        "languages": languages,
                        "address": address,
                        "phone": phone,
                        "objective": objective,
                        "sem1": sem1,
                        "sem1f": sem1f,
                        "sem2": sem2,
                        "sem2f": sem2f,
                        "sem3": sem3,
                        "sem3f": sem3f,
                        "sem4": sem4,
                        "sem4f": sem4f,
                        "sem5": sem5,
                        "sem5f": sem5f,
                        "sem6": sem6,
                        "sem6f": sem6f,
                        "sem7": sem7,
                        "sem7f": sem7f,
                        "sem8": sem8,
                        "sem8f": sem8f,
                        "aggregate": aggregate,
                        "ssc_marks": ssc_marks,
                        "sscf": sscf,
                        "ssc_institute": ssc_institute,
                        "ssc_year": ssc_year,
                        "hsc_marks": hsc_marks,
                        "hscf": hscf,
                        "hsc_institute": hsc_institute,
                        "hsc_year": hsc_year,
                        "be_proj": be_proj,
                        "te_proj": te_proj,
                        "tech_prof": tech_prof,
                        "awards": awards,
                        "hobbies": hobbies,
                        "error": error,
                        "diploma_check": diploma_check,
                        "number": number,
                    }
                else:
                    msg = {
                        "lastname": lastname,
                        "firstname": firstname,
                        "middlename": middlename,
                        "branch": branch,
                        "gender": gender,
                        "date": date,
                        "languages": languages,
                        "address": address,
                        "phone": phone,
                        "objective": objective,
                        "diploma": diploma,
                        "diploma_inst": diploma_inst,
                        "diploma_year": diploma_year,
                        "diplomaf": diplomaf,
                        "sem3": sem3,
                        "sem3f": sem3f,
                        "sem4": sem4,
                        "sem4f": sem4f,
                        "sem5": sem5,
                        "sem5f": sem5f,
                        "sem6": sem6,
                        "sem6f": sem6f,
                        "sem7": sem7,
                        "sem7f": sem7f,
                        "sem8": sem8,
                        "sem8f": sem8f,
                        "aggregate": aggregate,
                        "ssc_marks": ssc_marks,
                        "sscf": sscf,
                        "ssc_institute": ssc_institute,
                        "ssc_year": ssc_year,
                        "be_proj": be_proj,
                        "te_proj": te_proj,
                        "tech_prof": tech_prof,
                        "awards": awards,
                        "hobbies": hobbies,
                        "error": error,
                        "diploma_check": diploma_check,
                        "number": number,
                    }
                return render(request, 'resume_detail.html', msg)
            else:
                if request.POST.get('diploma') is None:
                    resumeUpload = Resume(user=user, name=name, branch=branch, gender=gender, date=date,
                                          languages=languages,
                                          address=address,
                                          phone=phone, objective=objective, sem1=sem1, sem1f=sem1f, sem2=sem2, sem2f=sem2f,
                                          diploma=None, diploma_inst=None, diploma_year=None,
                                          diplomaf=None, sem3=sem3, sem3f=sem3f, sem4=sem4, sem4f=sem4f,
                                          sem5=sem5, sem5f=sem5f,
                                          sem6=sem6, sem6f=sem6f, sem7=sem7, sem7f=sem7f, sem8=sem8, sem8f=sem8f,
                                          agg=aggregate,
                                          ssc_marks=ssc_marks, sscf=sscf,
                                          ssc_institute=ssc_institute, ssc_year=ssc_year, hsc_marks=hsc_marks, hscf=hscf,
                                          hsc_institute=hsc_institute, hsc_year=hsc_year, be_proj=be_proj, te_proj=te_proj,
                                          tech_prof=tech_prof, awards=awards, hobbies=hobbies, sperc=sperc, lock=True, number=number)
                else:
                    resumeUpload = Resume(user=user, name=name, branch=branch, gender=gender, date=date,
                                          languages=languages,
                                          address=address,
                                          phone=phone, objective=objective, sem1=None, sem1f=None, sem2=None, sem2f=None,
                                          diploma=diploma, diploma_inst=diploma_inst, diploma_year=diploma_year,
                                          diplomaf=diplomaf, sem3=sem3, sem3f=sem3f, sem4=sem4, sem4f=sem4f,
                                          sem5=sem5, sem5f=sem5f,
                                          sem6=sem6, sem6f=sem6f, sem7=sem7, sem7f=sem7f, sem8=sem8, sem8f=sem8f,
                                          agg=aggregate,
                                          ssc_marks=ssc_marks, sscf=sscf,
                                          ssc_institute=ssc_institute, ssc_year=ssc_year, hsc_marks=None, hscf=None,
                                          hsc_institute=None, hsc_year=None, be_proj=be_proj, te_proj=te_proj,
                                          tech_prof=tech_prof, awards=awards, hobbies=hobbies, sperc=sperc, lock=True, number=number)
                resumeUpload.save()
                pageObj = Resume.objects.filter(user=user)

                return render(request, 'resume_update.html',
                              {'resumes': pageObj, 'success': "Updated Successfully", 'name': passname, 'hn': hn})
        else:
            user_session = request.session['username']
            pageObj = Resume.objects.filter(user=user_session)
            if pageObj.exists():
                nedit = pageObj[0].name
                name = nedit.split(" ", 1)
                return render(request, 'resume_update.html', {'resumes': pageObj, 'name': name[1], 'hn': name[0]})
            else:
                return render(request, 'resume_detail.html',{'start':"start"})


@never_cache
def resume_update(request):
    if not request.session.get('student_login'):
        return HttpResponseRedirect("/login/")
    else:
        if request.method == 'POST':

            users = request.session['username']
            pageObj = Resume.objects.get(user=users)

            if pageObj.lock == True:
                studentResume = Resume.objects.filter(user=users)
                nedit = studentResume[0].name
                name = nedit.split(" ", 1)
                return render(request, 'resume_update.html', {'resumes': studentResume, 'lockerror': "Your Resume is locked, Please contact Admin.", 'name': name[1], 'hn': name[0]})
            else:
                hn = request.POST['hn']
                nam = request.POST['name']
                name = hn + " " + nam
                branch = request.POST['branch']
                gender = request.POST['gender']
                date = request.POST['dob']
                languages = request.POST['languages']
                address = request.POST['address']
                phone = request.POST['phoneInput']
                objective = request.POST['objective']

                aggregate = request.POST['aggregate'].strip()
                ssc_marks = request.POST['ssc'].strip()
                sscf = request.FILES.get('sscf')
                ssc_institute = request.POST['ssc_inst']
                ssc_year = request.POST['ssc_year'].strip()
                be_proj = request.POST['be_proj']
                te_proj = request.POST['te_proj']
                tech_prof = request.POST['tech_prof']
                awards = request.POST['awards']
                hobbies = request.POST['hobbies']

                myround = lambda x: float(int(x)) if int(x) == x else float(int(x) + 1)

                if float(aggregate) < 7.00:
                    spercs = 7.1 * float(aggregate) + 12
                    sperc = myround(spercs)
                else:
                    spercs = 7.4 * float(aggregate) + 12
                    sperc = myround(spercs)

                error = []

                sem3 = request.POST['sem3'].strip()
                sem3f = request.FILES.get('sem3f')
                pageObj.sem3 = sem3
                sem4 = request.POST['sem4'].strip()
                sem4f = request.FILES.get('sem4f')
                pageObj.sem4 = sem4
                sem5 = request.POST['sem5'].strip()
                sem5f = request.FILES.get('sem5f')
                pageObj.sem5 = sem5
                sem6 = request.POST['sem6'].strip()
                sem6f = request.FILES.get('sem6f')
                pageObj.sem6 = sem6
                sem7 = request.POST['sem7'].strip()
                sem7f = request.FILES.get('sem7f')
                pageObj.sem7 = sem7
                sem8 = request.POST['sem8'].strip()
                sem8f = request.FILES.get('sem8f')
                pageObj.sem8 = sem8

                if sem3 == '':
                    pageObj.sem3 = None
                if sem4 == '':
                    pageObj.sem4 = None
                if sem5 == '':
                    pageObj.sem5 = None
                if sem6 == '':
                    pageObj.sem6 = None
                if sem7 == '':
                    pageObj.sem7 = None
                if sem8 == '':
                    pageObj.sem8 = None

                MAX_UPLOAD_SIZE = 1048576

                if sem3f is not None:
                    if sem3f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 3 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem3f = sem3f

                if sem4f is not None:
                    if sem4f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 4 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem4f = sem4f

                if sem5f is not None:
                    if sem5f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 5 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem5f = sem5f

                if sem6f is not None:
                    if sem6f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 6 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem6f = sem6f

                if sem7f is not None:
                    if sem7f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 7 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem7f = sem7f

                if sem8f is not None:
                    if sem8f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 8 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem8f = sem8f

                if phone.isnumeric() == False:
                    error.append("Invalid Contact Number (10 digits start with 9/8/7).")

                if len(phone) < 10:
                    error.append("Invalid Contact Number (10 digits start with 9/8/7).")

                print("checkhere")
                print(pageObj.sem5f)

                if (sem3 == "" and sem3f is not None) or (sem3 == "" and bool(pageObj.sem3f) == True):
                    error.append("Sem 3 Marks missing.")
                if (sem4 == "" and sem4f is not None) or (sem4 == "" and bool(pageObj.sem4f) == True):
                    error.append("Sem 4 Marks missing.")
                if (sem5 == "" and sem5f is not None) or (sem5 == "" and bool(pageObj.sem5f) == True):
                    error.append("Sem 5 Marks missing.")
                if (sem6 == "" and sem6f is not None) or (sem6 == "" and bool(pageObj.sem6f) == True):
                    error.append("Sem 6 Marks missing.")
                if (sem7 == "" and sem7f is not None) or (sem7 == "" and bool(pageObj.sem7f) == True):
                    error.append("Sem 7 Marks missing.")
                if (sem8 == "" and sem8f is not None) or (sem8 == "" and bool(pageObj.sem8f) == True):
                    error.append("Sem 8 Marks missing.")

                if sem3 != "" and bool(pageObj.sem3f) == False and sem3f == None:
                    error.append("Sem 3 File missing.")
                if sem4 != "" and bool(pageObj.sem4f) == False and sem4f == None:
                    error.append("Sem 4 File missing.")
                if sem5 != "" and bool(pageObj.sem5f) == False and sem5f == None:
                    error.append("Sem 5 File missing.")
                if sem6 != "" and bool(pageObj.sem6f) == False and sem6f == None:
                    error.append("Sem 6 File missing.")
                if sem7 != "" and bool(pageObj.sem7f) == False and sem7f == None:
                    error.append("Sem 7 File missing.")
                if sem8 != "" and bool(pageObj.sem8f) == False and sem8f == None:
                    error.append("Sem 8 File missing.")

                if sem3f is not None:
                    if sem3f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 3 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem3f = sem3f

                if sem4f is not None:
                    if sem4f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 4 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem4f = sem4f

                if sem5f is not None:
                    if sem5f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 5 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem5f = sem5f

                if sem6f is not None:
                    if sem6f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 6 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem6f = sem6f

                if sem7f is not None:
                    if sem7f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 7 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem7f = sem7f

                if sem8f is not None:
                    if sem8f.size > MAX_UPLOAD_SIZE:
                        error.append("Sem 8 file upload size less than 1.0 MB")
                    else:
                        pageObj.sem8f = sem8f

                if sem3 != "":
                    if any(c.isalpha() for c in sem3) == True or float(sem3) > 10:
                        error.append("Invalid Sem 3 marks.")

                if sem4 != "":
                    if any(c.isalpha() for c in sem4) == True or float(sem4) > 10:
                        error.append("Invalid Sem 4 marks.")

                if sem5 != "":
                    if any(c.isalpha() for c in sem5) == True or float(sem5) > 10:
                        error.append("Invalid Sem 5 marks.")

                if sem6 != "":
                    if any(c.isalpha() for c in sem6) == True or float(sem6) > 10:
                        error.append("Invalid Sem 6 marks.")

                if sem7 != "":
                    if any(c.isalpha() for c in sem7) == True or float(sem7) > 10:
                        error.append("Invalid Sem 7 marks.")

                if sem8 != "":
                    if any(c.isalpha() for c in sem8) == True or float(sem8) > 10:
                        error.append("Invalid Sem 8 marks.")

                if any(c.isalpha() for c in aggregate) == True or float(aggregate) > 10:
                    error.append("Invalid Aggregate marks.")

                if any(c.isalpha() for c in ssc_marks) == True or float(ssc_marks) > 100:
                    error.append("Invalid SSC marks.")

                if sscf is not None:
                    if sscf.size > MAX_UPLOAD_SIZE:
                        error.append("SSC file upload size less than 1.0 MB")

                pageObj.user = users
                pageObj.name = name
                pageObj.branch = branch
                pageObj.gender = gender
                pageObj.date = date
                pageObj.languages = languages
                pageObj.address = address
                pageObj.phone = phone
                pageObj.objective = objective
                pageObj.agg = aggregate
                pageObj.ssc_marks = ssc_marks
                pageObj.ssc_institute = ssc_institute
                pageObj.ssc_year = ssc_year
                pageObj.be_proj = be_proj
                pageObj.te_proj = te_proj
                pageObj.tech_prof = tech_prof
                pageObj.awards = awards
                pageObj.hobbies = hobbies
                pageObj.sperc = sperc

                if pageObj.diploma == None:
                    sem1 = request.POST['sem1'].strip()
                    sem1f = request.FILES.get('sem1f')
                    sem2 = request.POST['sem2'].strip()
                    sem2f = request.FILES.get('sem2f')
                    hsc = request.POST['hsc'].strip()
                    hscf = request.FILES.get('hscf')
                    hsc_inst = request.POST['hsc_inst']
                    hsc_year = request.POST['hsc_year'].strip()

                    if sem1f is not None:
                        if sem1f.size > MAX_UPLOAD_SIZE:
                            error.append("Sem 1 file upload size less than 1.0 MB")
                        else:
                            pageObj.sem1f = sem1f

                    if sem2f is not None:
                        if sem2f.size > MAX_UPLOAD_SIZE:
                            error.append("Sem 2 file upload size less than 1.0 MB")
                        else:
                            pageObj.sem2f = sem2f

                    if hscf is not None:
                        if hscf.size > MAX_UPLOAD_SIZE:
                            error.append("HSC file upload size less than 1.0 MB")
                        else:
                            pageObj.hscf = hscf

                    pageObj.sem1 = sem1
                    pageObj.sem2 = sem2
                    pageObj.hsc_marks = hsc
                    pageObj.hsc_institute = hsc_inst
                    pageObj.hsc_year = hsc_year

                    if sem1 == "":
                        error.append("Sem 1 marks are mandatory.")
                    if sem2 == "":
                        error.append("Sem 2 marks are mandatory.")
                    if sem1 != "":
                        if any(c.isalpha() for c in sem1) == True or float(sem1) > 10:
                            error.append("Invalid Sem 1 marks.")
                    if sem2 != "":
                        if any(c.isalpha() for c in sem2) == True or float(sem2) > 10:
                            error.append("Invalid Sem 2 marks.")
                    if hsc == "":
                        error.append("HSC marks are mandatory.")
                    if any(c.isalpha() for c in hsc) == True or float(hsc) > 100:
                        error.append("Invalid HSC marks.")
                    if hsc_inst == "":
                        error.append("HSC institute is mandatory.")
                    if hsc_year.isnumeric() == False:
                        error.append("HSC Passing year is invalid.")

                else:
                    diplo = request.POST['diplo'].strip()
                    diplomaf = request.FILES.get('diplomaf')
                    diploma_inst = request.POST['diploi']
                    diploma_year = request.POST['diploy'].strip()
                    pageObj.diploma = diplo
                    pageObj.diploma_inst = diploma_inst
                    pageObj.diploma_year = diploma_year

                    if diplo == "":
                        error.append("Diploma marks are mandatory.")
                    if any(c.isalpha() for c in diplo) == True or float(diplo) > 100:
                        error.append("Invalid Diploma marks.")
                    if diploma_inst == "":
                        error.append("Diploma institute is mandatory.")
                    if diploma_year.isnumeric() == False:
                        error.append("Diploma Passing year is invalid.")

                    if diplomaf is not None:
                        if (not diplomaf.name.endswith('.png', '.jpg', '.jpeg')) or diplomaf.size > MAX_UPLOAD_SIZE:
                            error.append("Diploma file upload size less than 1.0 MB")
                        else:
                            pageObj.diplomaf = diplomaf

                if len(error) > 0:
                    studentResume = Resume.objects.filter(user=users)
                    nedit = studentResume[0].name
                    name = nedit.split(" ", 1)
                    msg = {
                        'error': error,
                        'resumes': studentResume,
                        'name': name[1],
                        'hn': name[0]
                    }
                    return render(request, 'resume_update.html', msg)
                else:
                    pageObj.lock = True
                    pageObj.save()
                    StudentPlaced.objects.filter(stud_user=users).update(stud_name=name, branch=branch)
                    StudentsEligible.objects.filter(stud_user=users).update(stud_name=name, branch=branch)
                    studentResume = Resume.objects.filter(user=users)

                    nedit = studentResume[0].name
                    name = nedit.split(" ", 1)

                    msg = {
                        "success": "Updated Successfully",
                        "resumes": studentResume,
                        "name": name[1],
                        "hn": name[0],
                    }
                    return render(request, 'resume_update.html',msg)
        else:
            users = request.session['username']
            studentResume = Resume.objects.filter(user=users)
            nedit = studentResume[0].name
            name = nedit.split(" ", 1)
            return render(request, 'resume_update.html', {'resumes': studentResume, 'name': name[1], 'hn': name[0]})


def logout_student(request):
    del request.session['username']
    del request.session['student_login']
    request.session.modified = True
    return HttpResponseRedirect("/login/")


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        user = request.session['username']
        resumes = Resume.objects.get(user=user)
        if resumes.hsc_marks == "":
            hdm = resumes.diploma
            hdi = resumes.diploma_inst
            hdy = resumes.diploma_year
        else:
            hdm = resumes.hsc_marks
            hdi = resumes.hsc_institute
            hdy = resumes.hsc_year
        context = {
            "resume_name": resumes.name,
            "resume_user": resumes.user,
            "resume_branch": resumes.branch,
            "resume_gender": resumes.gender,
            "resume_dob": resumes.date,
            "resume_lang": resumes.languages,
            "resume_addr": resumes.address,
            "resume_phone": resumes.phone,
            "resume_obj": resumes.objective,
            "resume_sem1": resumes.sem1,
            "resume_sem2": resumes.sem2,
            "resume_sem3": resumes.sem3,
            "resume_sem4": resumes.sem4,
            "resume_sem5": resumes.sem5,
            "resume_sem6": resumes.sem6,
            "resume_sem7": resumes.sem7,
            "resume_sem8": resumes.sem8,
            "resume_agg": resumes.agg,
            "resume_sscm": resumes.ssc_marks,
            "resume_ssci": resumes.ssc_institute,
            "resume_sscy": resumes.ssc_year,
            "resume_hdm": hdm,
            "resume_hdi": hdi,
            "resume_hdy": hdy,
            "resume_beproj": resumes.be_proj,
            "resume_teproj": resumes.te_proj,
            "resume_techprof": resumes.tech_prof,
            "resume_awards": resumes.awards,
            "resume_hobbies": resumes.hobbies,
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
        # if pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     filename = "Resume_%s.pdf" % ("12341231")
        #     content = "inline; filename='%s'" % (filename)
        #     download = request.GET.get("download")
        #     if download:
        #         content = "attachment; filename='%s'" % (filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return HttpResponse("Not found")


@never_cache
def company(request):
    if not request.session.get('student_login'):
        return HttpResponseRedirect("/login/")
    else:
        dream = []
        normal = []
        users = request.session['username']
        company = Company.objects.all().order_by('-id')
        comp_list = list(company.values())
        for comp in comp_list:
            if int(comp['ctc']) > 600000:
                if StudentsEligible.objects.filter(stud_user=users, comp_name=comp['comp_name']).exists():
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Eligible", comp['instruction'], comp['campus']]
                elif StudentPlaced.objects.filter(stud_user=users, comp_name=comp['comp_name']).exists():
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Placed", comp['instruction'], comp['campus']]
                else:
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Not Eligible", comp['instruction'], comp['campus']]
                dream.append(temp)
            else:
                if StudentsEligible.objects.filter(stud_user=users, comp_name=comp['comp_name']).exists():
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Eligible", comp['instruction'], comp['campus']]
                elif StudentPlaced.objects.filter(stud_user=users, comp_name=comp['comp_name']).exists():
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Placed", comp['instruction'], comp['campus']]
                else:
                    temp = [comp['comp_name'], comp['comp_profile'], comp['ctc'], comp['eligibility'], comp['bond'], comp['date'], comp['time'], comp['venue'], comp['branch'], "Not Eligible", comp['instruction'], comp['campus']]
                normal.append(temp)

        data = {
            'dream': dream,
            'normal': normal,
        }
        return render(request, 'student_company.html', data)


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
