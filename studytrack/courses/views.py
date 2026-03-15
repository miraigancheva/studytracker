from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from exams.models import Exam
from grades.models import Grade
from .models import Subject, StudyGroup
from .forms import SubjectForm, StudyGroupForm
from django.utils import timezone


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def home(request):
    subjects = Subject.objects.all()
    upcoming = Exam.objects.filter(
        date__gte=timezone.now().date(),
        status='upcoming'
    ).select_related('subject').order_by('date')[:4]
    recent_grades = Grade.objects.select_related('subject').order_by('-date')[:4]
    return render(request, 'home.html', {
        'subjects': subjects,
        'upcoming': upcoming,
        'recent_grades': recent_grades,
    })


def subject_list(request):
    semester = request.GET.get('semester', '')
    subjects = Subject.objects.all()
    if semester:
        subjects = subjects.filter(semester=semester)
    semesters = Subject.objects.values_list('semester', flat=True).distinct()
    return render(request, 'courses/subject_list.html', {
        'subjects': subjects,
        'semesters': semesters,
        'selected_semester': semester,
    })


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'courses/subject_detail.html', {'subject': subject})


def subject_add(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = form.save()
        messages.success(request, f'{subject.name} was added.')
        return redirect('courses:subject_list')
    return render(request, 'courses/subject_form.html', {'form': form, 'action': 'Add'})


def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{subject.name} updated.')
        return redirect('courses:subject_detail', pk=pk)
    return render(request, 'courses/subject_form.html', {'form': form, 'action': 'Edit', 'subject': subject})


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted.')
        return redirect('courses:subject_list')
    return render(request, 'courses/subject_confirm_delete.html', {'subject': subject})


def group_list(request):
    groups = StudyGroup.objects.prefetch_related('subjects').all()
    return render(request, 'courses/group_list.html', {'groups': groups})


def group_add(request):
    form = StudyGroupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        group = form.save()
        messages.success(request, f'Group "{group.name}" created.')
        return redirect('courses:group_list')
    return render(request, 'courses/group_form.html', {'form': form, 'action': 'Create'})


def group_edit(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    form = StudyGroupForm(request.POST or None, instance=group)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Group "{group.name}" updated.')
        return redirect('courses:group_list')
    return render(request, 'courses/group_form.html', {'form': form, 'action': 'Edit', 'group': group})


def group_delete(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted.')
    return redirect('courses:group_list')
