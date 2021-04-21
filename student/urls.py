from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import GeneratePdf

urlpatterns = [
    path('resume/', views.resume, name='resume'),
    path('resume_update/', views.resume_update, name='resume_update'),
    path('company/',views.company,name='company'),
    path('pdf/', GeneratePdf.as_view()),
    path('logout_student/', views.logout_student, name='logout_student'),

]+ static('resume/media/', document_root=settings.MEDIA_ROOT)