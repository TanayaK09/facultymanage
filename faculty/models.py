from django.db import models


class Admin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=255)
    FullName = models.CharField(max_length=100)
    Email = models.EmailField()
    ContactNumber = models.CharField(max_length=15)
    LastLogin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.Username

class Faculty(models.Model):
    FacultyID = models.CharField(max_length=10, primary_key=True)
    Password = models.CharField(max_length=255, blank=True)
    ProfilePhoto = models.ImageField(upload_to="faculty_photos/", blank=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Gender = models.CharField(max_length=20)
    DOB = models.DateField()
    Email = models.EmailField()
    ContactNumber = models.CharField(max_length=10)
    Address = models.TextField()
    Qualification = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    JoiningDate = models.DateField()
    Experience = models.DecimalField(max_digits=4, decimal_places=1)
    Status = models.CharField(max_length=20)

class Attendance(models.Model):
    AttendanceID = models.CharField(max_length=10, primary_key=True)
    FacultyID = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    Date = models.DateField()
    CheckInTime = models.TimeField(null=True, blank=True)
    CheckOutTime = models.TimeField(null=True, blank=True)
    Status = models.CharField(max_length=20)
    Remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.AttendanceID:
            last_attendance = Attendance.objects.order_by("-AttendanceID").first()

            if last_attendance:
                number = int(last_attendance.AttendanceID.replace("ATT", "")) + 1
            else:
                number = 1

            self.AttendanceID = f"ATT{number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.AttendanceID} - {self.FacultyID} - {self.Date}"

class Salary(models.Model):

    SalaryID = models.AutoField(primary_key=True)

    FacultyID = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="salary_records"
    )

    HourlyRate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    TotalHours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    Deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    NetSalary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    PaymentDate = models.DateField(
        null=True,
        blank=True
    )

    Month = models.IntegerField()

    Year = models.IntegerField()

    def __str__(self):
        return f"{self.FacultyID} - {self.Month}/{self.Year}"

class Schedule(models.Model):
    ScheduleID = models.AutoField(primary_key=True)
    FacultyID = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="schedule_records"
    )
    Subject = models.CharField(max_length=100)
    Date = models.DateField()
    Day = models.CharField(max_length=20)
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    RoomNumber = models.CharField(max_length=20)
    Standard = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return f"{self.Subject} - {self.Date} - {self.Day}"