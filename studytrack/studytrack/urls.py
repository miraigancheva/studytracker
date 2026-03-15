from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('grades/', include('grades.urls', namespace='grades')),
]

handler404 = 'courses.views.page_not_found'
