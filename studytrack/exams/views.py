from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Exam
from .forms import ExamForm, ExamStatusForm


def exam_list(request):
    today = timezone.now().date()
    status_filter = request.GET.get('status', '')
    upcoming = Exam.objects.filter(date__gte=today).select_related('subject')
    past = Exam.objects.filter(date__lt=today).select_related('subject')
    if status_filter:
        past = past.filter(status=status_filter)
    return render(request, 'exams/exam_list.html', {
        'upcoming': upcoming,
        'past': past,
        'status_filter': status_filter,
        'status_choices': Exam.STATUS_CHOICES,
    })


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'exams/exam_detail.html', {'exam': exam})


def exam_add(request):
    form = ExamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exam added.')
        return redirect('exams:exam_list')
    return render(request, 'exams/exam_form.html', {'form': form, 'action': 'Add'})


def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    form = ExamForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Exam updated.')
        return redirect('exams:exam_detail', pk=pk)
    return render(request, 'exams/exam_form.html', {'form': form, 'action': 'Edit', 'exam': exam})


def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted.')
        return redirect('exams:exam_list')
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


def exam_update_status(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    form = ExamStatusForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Status updated.')
        return redirect('exams:exam_detail', pk=pk)
    return render(request, 'exams/exam_status_form.html', {'form': form, 'exam': exam})
