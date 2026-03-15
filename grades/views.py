from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Grade
from .forms import GradeForm


def grade_list(request):
    subject_filter = request.GET.get('subject', '')
    grades = Grade.objects.select_related('subject').all()
    if subject_filter:
        grades = grades.filter(subject_id=subject_filter)

    avg = None
    if grades.exists():
        avg = round(sum(g.percentage() for g in grades) / grades.count(), 1)

    from courses.models import Subject
    subjects = Subject.objects.all()

    return render(request, 'grades/grade_list.html', {
        'grades': grades,
        'avg': avg,
        'subjects': subjects,
        'subject_filter': subject_filter,
    })


def grade_detail(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    return render(request, 'grades/grade_detail.html', {'grade': grade})


def grade_add(request):
    form = GradeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grade saved.')
        return redirect('grades:grade_list')
    return render(request, 'grades/grade_form.html', {'form': form, 'action': 'Add'})


def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=grade)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grade updated.')
        return redirect('grades:grade_detail', pk=pk)
    return render(request, 'grades/grade_form.html', {'form': form, 'action': 'Edit', 'grade': grade})


def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted.')
        return redirect('grades:grade_list')
    return render(request, 'grades/grade_confirm_delete.html', {'grade': grade})
