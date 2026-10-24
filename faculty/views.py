from datetime import datetime

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.utils import timezone

from .models import Admin, Faculty, Attendance, Salary, Schedule

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        admin = Admin.objects.filter(Username=username).first()

        if admin and check_password(password, admin.Password):
            request.session["admin_id"] = admin.AdminID
            return redirect("dashboard")

        faculty = Faculty.objects.filter(FacultyID=username).first()

        if faculty and check_password(password, faculty.Password):
            request.session["faculty_id"] = faculty.FacultyID
            return redirect("faculty_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def faculty_login(request):
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")

        faculty = Faculty.objects.filter(FacultyID=faculty_id).first()

        if faculty and check_password(password, faculty.Password):
            request.session["faculty_id"] = faculty.FacultyID
            return redirect("faculty_dashboard")

        return render(
            request,
            "faculty_login.html",
            {
                "error": "Invalid Faculty ID or password"
            }
        )

    return render(request, "faculty_login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


def admin_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmpassword")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")

        if password != confirm_password:
            return render(
                request,
                "admin_register.html",
                {
                    "error": "Passwords do not match"
                }
            )

        if Admin.objects.filter(Username=username).exists():
            return render(
                request,
                "admin_register.html",
                {
                    "error": "Username already exists"
                }
            )

        Admin.objects.create(
            Username=username,
            Password=make_password(password),
            FullName=fullname,
            Email=email,
            ContactNumber=contact
        )

        messages.success(
            request,
            "Admin registered successfully."
        )

        return redirect("login")

    return render(request, "admin_register.html")


def dashboard(request):
    if "admin_id" not in request.session:
        return redirect("login")

    today = timezone.localdate()

    total_faculty = Faculty.objects.count()

    present_today = Attendance.objects.filter(
        Date=today,
        Status="Present"
    ).values(
        "FacultyID"
    ).distinct().count()

    absent_today = Attendance.objects.filter(
        Date=today,
        Status="Absent"
    ).values(
        "FacultyID"
    ).distinct().count()

    today_lectures = Schedule.objects.filter(
        Date=today
    ).count()

    unpaid_salary = Salary.objects.filter(
        PaymentDate__isnull=True
    ).count()

    attendance_total = present_today + absent_today

    if attendance_total > 0:
        attendance_percentage = round(
            (present_today / attendance_total) * 100
        )
    else:
        attendance_percentage = 0

    today_schedules = Schedule.objects.select_related(
        "FacultyID"
    ).filter(
        Date=today
    ).order_by(
        "StartTime"
    )

    recent_attendance = Attendance.objects.select_related(
        "FacultyID"
    ).order_by(
        "-Date",
        "-AttendanceID"
    )[:5]

    context = {
        "today": today,
        "total_faculty": total_faculty,
        "present_today": present_today,
        "absent_today": absent_today,
        "today_lectures": today_lectures,
        "unpaid_salary": unpaid_salary,
        "attendance_percentage": attendance_percentage,
        "today_schedules": today_schedules,
        "recent_attendance": recent_attendance
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


def manage_faculty(request):
    if "admin_id" not in request.session:
        return redirect("login")

    faculties = Faculty.objects.all()

    return render(
        request,
        "manage_faculty.html",
        {
            "faculties": faculties
        }
    )


def add_faculty(request):
    if "admin_id" not in request.session:
        return redirect("login")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        qualification = request.POST.get("qualification")
        designation = request.POST.get("designation")
        joining_date = request.POST.get("joining_date")
        experience = request.POST.get("experience")
        status = request.POST.get("status")
        password = request.POST.get("password")

        last_faculty = Faculty.objects.order_by(
            "-FacultyID"
        ).first()

        if last_faculty:
            number = int(
                last_faculty.FacultyID.replace(
                    "FAC",
                    ""
                )
            ) + 1
        else:
            number = 1

        faculty_id = f"FAC{number:03d}"

        Faculty.objects.create(
            FacultyID=faculty_id,
            FirstName=first_name,
            LastName=last_name,
            Gender=gender,
            DOB=dob,
            Email=email,
            ContactNumber=contact_number,
            Address=address,
            Qualification=qualification,
            Designation=designation,
            JoiningDate=joining_date,
            Experience=experience,
            Status=status,
            Password=make_password(password)
        )

        messages.success(
            request,
            "Faculty added successfully."
        )

        return redirect("manage_faculty")

    return render(
        request,
        "add_faculty.html"
    )


def update_faculty(request, faculty_id):
    if "admin_id" not in request.session:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    if request.method == "POST":
        faculty.FirstName = request.POST.get("first_name")
        faculty.LastName = request.POST.get("last_name")
        faculty.Gender = request.POST.get("gender")
        faculty.DOB = request.POST.get("dob")
        faculty.Email = request.POST.get("email")
        faculty.ContactNumber = request.POST.get("contact_number")
        faculty.Address = request.POST.get("address")
        faculty.Qualification = request.POST.get("qualification")
        faculty.Designation = request.POST.get("designation")
        faculty.JoiningDate = request.POST.get("joining_date")
        faculty.Experience = request.POST.get("experience")
        faculty.Status = request.POST.get("status")

        faculty.save()

        messages.success(
            request,
            "Faculty updated successfully."
        )

        return redirect("manage_faculty")

    return render(
        request,
        "update_faculty.html",
        {
            "faculty": faculty
        }
    )


def delete_faculty(request, faculty_id):
    if "admin_id" not in request.session:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    faculty.delete()

    messages.success(
        request,
        "Faculty deleted successfully."
    )

    return redirect("manage_faculty")


def view_faculty(request, faculty_id):
    if "admin_id" not in request.session:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    return render(
        request,
        "view_faculty.html",
        {
            "faculty": faculty
        }
    )


def attendance(request):
    if "admin_id" not in request.session:
        return redirect("login")

    faculties = Faculty.objects.all().order_by(
        "FacultyID"
    )

    if request.method == "POST":
        faculty_id = request.POST.get("faculty")
        date = request.POST.get("date")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        status = request.POST.get("status")
        remarks = request.POST.get("remarks")

        faculty = get_object_or_404(
            Faculty,
            FacultyID=faculty_id
        )

        Attendance.objects.create(
            FacultyID=faculty,
            Date=date,
            CheckInTime=check_in if check_in else None,
            CheckOutTime=check_out if check_out else None,
            Status=status,
            Remarks=remarks
        )

        messages.success(
            request,
            "Attendance marked successfully."
        )

        return redirect(
            "/attendance/?tab=view"
        )

    attendance_records = Attendance.objects.select_related(
        "FacultyID"
    ).order_by(
        "-Date",
        "FacultyID"
    )

    active_tab = request.GET.get(
        "tab",
        "mark"
    )

    return render(
        request,
        "attendance.html",
        {
            "faculties": faculties,
            "attendance_records": attendance_records,
            "active_tab": active_tab
        }
    )


def view_attendance(request):
    if "admin_id" not in request.session:
        return redirect("login")

    return redirect("/attendance/?tab=view")


def delete_attendance(request, attendance_id):
    if "admin_id" not in request.session:
        return redirect("login")

    attendance_record = get_object_or_404(
        Attendance,
        AttendanceID=attendance_id
    )

    attendance_record.delete()

    messages.success(
        request,
        "Attendance record deleted successfully."
    )

    return redirect("/attendance/?tab=view")


def salary(request):
    if "admin_id" not in request.session:
        return redirect("login")

    faculties = Faculty.objects.all().order_by(
        "FacultyID"
    )

    if request.method == "POST":
        faculty_id = request.POST.get("faculty")
        hourly_rate = request.POST.get("hourly_rate")
        deduction = request.POST.get("deduction") or "0"
        payment_date = request.POST.get("payment_date")
        month = request.POST.get("month")
        year = request.POST.get("year")
        salary_id = request.POST.get("salary_id")

        if (
            not faculty_id
            or not month
            or not year
            or not hourly_rate
        ):
            messages.error(
                request,
                "Please fill all required salary details."
            )

            return redirect("salary")

        faculty = get_object_or_404(
            Faculty,
            FacultyID=faculty_id
        )

        attendance_records = Attendance.objects.filter(
            FacultyID=faculty,
            Date__month=int(month),
            Date__year=int(year),
            Status="Present"
        )

        total_minutes = 0

        for record in attendance_records:
            if record.CheckInTime and record.CheckOutTime:
                check_in = (
                    record.CheckInTime.hour * 60
                    + record.CheckInTime.minute
                )

                check_out = (
                    record.CheckOutTime.hour * 60
                    + record.CheckOutTime.minute
                )

                minutes = check_out - check_in

                if minutes > 0:
                    total_minutes += minutes

        total_hours = total_minutes / 60

        net_salary = (
            float(total_hours)
            * float(hourly_rate)
        ) - float(deduction)

        if net_salary < 0:
            net_salary = 0

        if salary_id:
            salary_record = get_object_or_404(
                Salary,
                SalaryID=salary_id
            )

            salary_record.FacultyID = faculty
            salary_record.HourlyRate = hourly_rate
            salary_record.TotalHours = total_hours
            salary_record.Deduction = deduction
            salary_record.NetSalary = net_salary
            salary_record.PaymentDate = (
                payment_date
                if payment_date
                else None
            )
            salary_record.Month = month
            salary_record.Year = year

            salary_record.save()

            messages.success(
                request,
                "Salary updated successfully."
            )

        else:
            Salary.objects.create(
                FacultyID=faculty,
                HourlyRate=hourly_rate,
                TotalHours=total_hours,
                Deduction=deduction,
                NetSalary=net_salary,
                PaymentDate=(
                    payment_date
                    if payment_date
                    else None
                ),
                Month=month,
                Year=year
            )

            messages.success(
                request,
                "Salary calculated and added successfully."
            )

        return redirect("salary")

    salaries = Salary.objects.select_related(
        "FacultyID"
    ).order_by(
        "-Year",
        "-Month",
        "FacultyID"
    )

    selected_salary = None

    faculty_id = request.GET.get("faculty")
    month = request.GET.get("month")
    year = request.GET.get("year")

    if faculty_id and month and year:
        selected_salary = Salary.objects.filter(
            FacultyID=faculty_id,
            Month=month,
            Year=year
        ).first()

    return render(
        request,
        "salary.html",
        {
            "faculties": faculties,
            "salaries": salaries,
            "selected_salary": selected_salary
        }
    )


def get_total_hours(request):
    if "admin_id" not in request.session:
        return JsonResponse(
            {
                "hours": 0
            }
        )

    faculty_id = request.GET.get("faculty")
    month = request.GET.get("month")
    year = request.GET.get("year")

    if not faculty_id or not month or not year:
        return JsonResponse(
            {
                "hours": 0
            }
        )

    attendance_records = Attendance.objects.filter(
        FacultyID_id=faculty_id,
        Date__month=int(month),
        Date__year=int(year),
        Status="Present"
    )

    total_minutes = 0

    for record in attendance_records:
        if record.CheckInTime and record.CheckOutTime:
            check_in = (
                record.CheckInTime.hour * 60
                + record.CheckInTime.minute
            )

            check_out = (
                record.CheckOutTime.hour * 60
                + record.CheckOutTime.minute
            )

            minutes = check_out - check_in

            if minutes > 0:
                total_minutes += minutes

    total_hours = total_minutes / 60

    return JsonResponse(
        {
            "hours": round(
                total_hours,
                2
            )
        }
    )


def add_salary(request):
    if "admin_id" not in request.session:
        return redirect("login")

    faculties = Faculty.objects.all().order_by(
        "FacultyID"
    )

    if request.method == "POST":
        faculty_id = request.POST.get("faculty")
        hourly_rate = request.POST.get("hourly_rate")
        deduction = request.POST.get("deduction") or "0"
        payment_date = request.POST.get("payment_date")
        month = request.POST.get("month")
        year = request.POST.get("year")

        faculty = get_object_or_404(
            Faculty,
            FacultyID=faculty_id
        )

        attendance_records = Attendance.objects.filter(
            FacultyID=faculty,
            Date__month=int(month),
            Date__year=int(year),
            Status="Present"
        )

        total_minutes = 0

        for record in attendance_records:
            if record.CheckInTime and record.CheckOutTime:
                check_in = (
                    record.CheckInTime.hour * 60
                    + record.CheckInTime.minute
                )

                check_out = (
                    record.CheckOutTime.hour * 60
                    + record.CheckOutTime.minute
                )

                minutes = check_out - check_in

                if minutes > 0:
                    total_minutes += minutes

        total_hours = total_minutes / 60

        net_salary = (
            float(total_hours)
            * float(hourly_rate)
        ) - float(deduction)

        if net_salary < 0:
            net_salary = 0

        Salary.objects.create(
            FacultyID=faculty,
            HourlyRate=hourly_rate,
            TotalHours=total_hours,
            Deduction=deduction,
            NetSalary=net_salary,
            PaymentDate=(
                payment_date
                if payment_date
                else None
            ),
            Month=month,
            Year=year
        )

        messages.success(
            request,
            "Salary calculated and added successfully."
        )

        return redirect("salary")

    return render(
        request,
        "add_salary.html",
        {
            "faculties": faculties
        }
    )


def view_salary(request):
    if "admin_id" not in request.session:
        return redirect("login")

    salary_records = Salary.objects.select_related(
        "FacultyID"
    ).order_by(
        "-Year",
        "-Month",
        "FacultyID"
    )

    return render(
        request,
        "view_salary.html",
        {
            "salary_records": salary_records
        }
    )


def update_salary(request, salary_id):
    if "admin_id" not in request.session:
        return redirect("login")

    salary_record = get_object_or_404(
        Salary,
        SalaryID=salary_id
    )

    faculties = Faculty.objects.all().order_by(
        "FacultyID"
    )

    if request.method == "POST":
        faculty_id = request.POST.get("faculty")
        hourly_rate = request.POST.get("hourly_rate")
        deduction = request.POST.get("deduction") or "0"
        payment_date = request.POST.get("payment_date")
        month = request.POST.get("month")
        year = request.POST.get("year")

        faculty = get_object_or_404(
            Faculty,
            FacultyID=faculty_id
        )

        attendance_records = Attendance.objects.filter(
            FacultyID=faculty,
            Date__month=int(month),
            Date__year=int(year),
            Status="Present"
        )

        total_minutes = 0

        for record in attendance_records:
            if record.CheckInTime and record.CheckOutTime:
                check_in = (
                    record.CheckInTime.hour * 60
                    + record.CheckInTime.minute
                )

                check_out = (
                    record.CheckOutTime.hour * 60
                    + record.CheckOutTime.minute
                )

                minutes = check_out - check_in

                if minutes > 0:
                    total_minutes += minutes

        total_hours = total_minutes / 60

        net_salary = (
            float(total_hours)
            * float(hourly_rate)
        ) - float(deduction)

        if net_salary < 0:
            net_salary = 0

        salary_record.FacultyID = faculty
        salary_record.HourlyRate = hourly_rate
        salary_record.TotalHours = total_hours
        salary_record.Deduction = deduction
        salary_record.NetSalary = net_salary
        salary_record.PaymentDate = (
            payment_date
            if payment_date
            else None
        )
        salary_record.Month = month
        salary_record.Year = year

        salary_record.save()

        messages.success(
            request,
            "Salary updated successfully."
        )

        return redirect("salary")

    return render(
        request,
        "update_salary.html",
        {
            "salary_record": salary_record,
            "faculties": faculties
        }
    )


def delete_salary(request, salary_id):
    if "admin_id" not in request.session:
        return redirect("login")

    salary_record = get_object_or_404(
        Salary,
        SalaryID=salary_id
    )

    salary_record.delete()

    messages.success(
        request,
        "Salary deleted successfully."
    )

    return redirect("view_salary")


def schedule(request):
    if "admin_id" not in request.session:
        return redirect("login")

    faculties = Faculty.objects.all().order_by(
        "FacultyID"
    )

    if request.method == "POST":
        schedule_id = request.POST.get("schedule_id")
        faculty_id = request.POST.get("faculty")
        subject = request.POST.get("subject")
        standard = request.POST.get("standard")
        date = request.POST.get("date")
        start_time = request.POST.get("starttime")
        end_time = request.POST.get("endtime")
        room_number = request.POST.get("roomnumber")

        if (
            not faculty_id
            or not subject
            or not standard
            or not date
            or not start_time
            or not end_time
            or not room_number
        ):
            messages.error(
                request,
                "Please fill all schedule details."
            )

            return redirect("schedule")

        try:
            schedule_date = datetime.strptime(
                date,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            messages.error(
                request,
                "Please select a valid date."
            )

            return redirect("schedule")

        day = schedule_date.strftime("%A")

        if start_time >= end_time:
            messages.error(
                request,
                "End Time must be later than Start Time."
            )

            return redirect("schedule")

        faculty = get_object_or_404(
            Faculty,
            FacultyID=faculty_id
        )

        if schedule_id:
            schedule_record = get_object_or_404(
                Schedule,
                ScheduleID=schedule_id
            )

            schedule_record.FacultyID = faculty
            schedule_record.Subject = subject
            schedule_record.Standard = standard
            schedule_record.Date = schedule_date
            schedule_record.Day = day
            schedule_record.StartTime = start_time
            schedule_record.EndTime = end_time
            schedule_record.RoomNumber = room_number

            schedule_record.save()

            messages.success(
                request,
                "Schedule updated successfully."
            )

        else:
            Schedule.objects.create(
                FacultyID=faculty,
                Subject=subject,
                Standard=standard,
                Date=schedule_date,
                Day=day,
                StartTime=start_time,
                EndTime=end_time,
                RoomNumber=room_number
            )

            messages.success(
                request,
                "Schedule created successfully."
            )

        return redirect("schedule")

    schedules = Schedule.objects.select_related(
        "FacultyID"
    ).all().order_by(
        "Date",
        "StartTime"
    )

    edit_schedule = None

    edit_id = request.GET.get("edit")

    if edit_id:
        edit_schedule = get_object_or_404(
            Schedule,
            ScheduleID=edit_id
        )

    return render(
        request,
        "schedule.html",
        {
            "faculties": faculties,
            "schedules": schedules,
            "edit_schedule": edit_schedule
        }
    )


def delete_schedule(request, schedule_id):
    if "admin_id" not in request.session:
        return redirect("login")

    schedule_record = get_object_or_404(
        Schedule,
        ScheduleID=schedule_id
    )

    schedule_record.delete()

    messages.success(
        request,
        "Schedule deleted successfully."
    )

    return redirect("schedule")

def _save_faculty_profile_photo(request, faculty):
    uploaded_photo = request.FILES.get("profile_photo")

    if not uploaded_photo:
        messages.error(request, "Select a photo to upload.")
    elif uploaded_photo.size > 5 * 1024 * 1024:
        messages.error(request, "Photo must be 5 MB or smaller.")
    else:
        try:
            validated_photo = forms.ImageField().clean(uploaded_photo)
        except forms.ValidationError:
            messages.error(request, "Choose a valid image file.")
        else:
            faculty.ProfilePhoto = validated_photo
            faculty.save(update_fields=["ProfilePhoto"])
            messages.success(request, "Profile photo updated successfully.")


def faculty_dashboard(request):
    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    if request.method == "POST":
        _save_faculty_profile_photo(request, faculty)
        return redirect("faculty_dashboard")

    today = timezone.localdate()

    today_schedules = Schedule.objects.filter(
        FacultyID=faculty,
        Date=today
    ).order_by(
        "StartTime"
    )

    attendance_records = Attendance.objects.filter(
        FacultyID=faculty
    )

    present_days = attendance_records.filter(
        Status="Present"
    ).count()

    absent_days = attendance_records.filter(
        Status="Absent"
    ).count()

    total_days = present_days + absent_days

    if total_days > 0:
        attendance_percentage = round(
            (present_days / total_days) * 100
        )
    else:
        attendance_percentage = 0

    current_month = today.month
    current_year = today.year

    current_salary = Salary.objects.filter(
        FacultyID=faculty,
        Month=current_month,
        Year=current_year
    ).order_by("-SalaryID").first()

    return render(
        request,
        "faculty_dashboard.html",
        {
            "faculty": faculty,
            "today": today,
            "today_schedules": today_schedules,
            "present_days": present_days,
            "absent_days": absent_days,
            "total_days": total_days,
            "attendance_percentage": attendance_percentage,
            "current_salary": current_salary
        }
    )

def faculty_profile(request):
    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    if request.method == "POST":
        _save_faculty_profile_photo(request, faculty)
        return redirect("faculty_profile")

    return render(
        request,
        "faculty_profile.html",
        {"faculty": faculty}
    )

def faculty_schedule(request):
    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    schedules = Schedule.objects.filter(
        FacultyID=faculty
    ).order_by(
        "Date",
        "StartTime"
    )

    return render(
        request,
        "faculty_schedule.html",
        {
            "faculty": faculty,
            "schedules": schedules
        }
    )
def faculty_attendance(request):
    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    attendance_records = Attendance.objects.filter(
        FacultyID=faculty
    ).order_by(
        "-Date"
    )

    present_days = attendance_records.filter(
        Status="Present"
    ).count()

    absent_days = attendance_records.filter(
        Status="Absent"
    ).count()

    total_days = attendance_records.count()

    if total_days > 0:
        attendance_percentage = round(
            (present_days / total_days) * 100
        )
    else:
        attendance_percentage = 0

    return render(
        request,
        "faculty_attendance.html",
        {
            "faculty": faculty,
            "attendance_records": attendance_records,
            "present_days": present_days,
            "absent_days": absent_days,
            "total_days": total_days,
            "attendance_percentage": attendance_percentage
        }
    )

def faculty_salary(request):
    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("login")

    faculty = get_object_or_404(
        Faculty,
        FacultyID=faculty_id
    )

    salary_records = Salary.objects.filter(
        FacultyID=faculty
    ).order_by(
        "-Year",
        "-Month"
    )

    return render(
        request,
        "faculty_salary.html",
        {
            "faculty": faculty,
            "salary_records": salary_records
        }
    )