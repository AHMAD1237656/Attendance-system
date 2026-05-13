from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AttendanceForm
from .models import Attendance
from django.db.models import Count
from django.utils import timezone

# ✅ Helper function: check if user is HR Manager
def is_hr(user):
    return user.groups.filter(name='HR_Manager').exists()

# ➡️ Dashboard (only HR Manager)
@login_required
@user_passes_test(is_hr)
def dashboard(request):
    current_month = timezone.now().month
    report = Attendance.objects.filter(date__month=current_month) \
              .values('employee__username') \
              .annotate(total=Count('id'))

    labels = [r['employee__username'] for r in report]
    data = [r['total'] for r in report]

    return render(request, 'dashboard.html', {
        'labels': labels,
        'data': data
    })

# ➡️ Monthly Report (only HR Manager)
@login_required
@user_passes_test(is_hr)
def monthly_report(request):
    current_month = timezone.now().month
    report = Attendance.objects.filter(date__month=current_month) \
              .values('employee__username') \
              .annotate(total=Count('id'))
    return render(request, 'monthly_report.html', {'report': report})

# ➡️ Create (Add Attendance) – Employees + HR Manager
@login_required
def mark_attendance(request):
    if request.user.groups.filter(name='Employee').exists() or is_hr(request.user):
        if request.method == 'POST':
            form = AttendanceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('attendance_list')
        else:
            form = AttendanceForm()
        return render(request, 'mark_attendance.html', {'form': form})
    else:
        return redirect('login')

# ➡️ Read (List Attendance Records) – only HR Manager
@login_required
@user_passes_test(is_hr)
def attendance_list(request):
    records = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'records': records})

# ➡️ Update (Edit Attendance Record) – only HR Manager
@login_required
@user_passes_test(is_hr)
def update_attendance(request, id):
    record = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=record)
    return render(request, 'update_attendance.html', {'form': form})

# ➡️ Delete (Remove Attendance Record) – only HR Manager
@login_required
@user_passes_test(is_hr)
def delete_attendance(request, id):
    record = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        record.delete()
        return redirect('attendance_list')
    return render(request, 'delete_attendance.html', {'record': record})
