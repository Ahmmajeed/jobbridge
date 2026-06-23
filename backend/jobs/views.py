from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application

def job_list(request):
    title = request.GET.get('title', '').strip()
    company = request.GET.get('company', '').strip()
    location = request.GET.get('location', '').strip()

    jobs = Job.objects.all()
    if title:
        jobs = jobs.filter(title__icontains=title)
    if company:
        jobs = jobs.filter(company__icontains=company)
    if location:
        jobs = jobs.filter(location__icontains=location)

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    return render(request, 'jobs/jobs.html', {
        'page_obj': page_obj,
        'title': title,
        'company': company,
        'location': location,
        'querystring': query_params.urlencode(),
    })

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    saved = request.user.is_authenticated and request.user in job.saved_by.all()
    return render(request, 'jobs/job_detail.html', {'job': job, 'saved': saved})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '').strip()
        Application.objects.create(
            user=request.user,
            job=job,
            cover_letter=cover_letter,
            status=Application.STATUS_PENDING,
        )
        if request.user.email:
            send_mail(
                'Application Submitted',
                f'Hi {request.user.username}, your application for {job.title} has been submitted.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
        return redirect('accounts:dashboard')
    return render(request, 'jobs/apply.html', {'job': job})

@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        if request.user in job.saved_by.all():
            job.saved_by.remove(request.user)
        else:
            job.saved_by.add(request.user)
    return redirect('jobs:job_detail', job_id=job.id)

@login_required
def employer_dashboard(request):
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    recent_applicants = Application.objects.select_related('user', 'job').order_by('-applied_at')[:5]

    return render(request, 'jobs/employer.html', {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'recent_applicants': recent_applicants,
    })