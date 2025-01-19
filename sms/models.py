from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentAdmission(models.Model):
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField()
    address = models.TextField()
    class_of_admission = models.CharField(max_length=10)
    previous_school = models.CharField(max_length=30)
    parent_name = models.CharField(max_length=30)
    parent_contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name if self.name else 'Unnamed Class'
    
class Section(models.Model):
    name = models.CharField(max_length=50)
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    def __str__(self):
        return self.name if self.name else 'Unnamed Section'

class Subject(models.Model):
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    subjectname = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.subjectname if self.subjectname else 'Unnamed Subject'

class Exam(models.Model):
    EXAM_TYPES = [
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
        ('Annual', 'Annual'),
        ('Unit Test', 'Unit Test'),
    ]
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    unit_test_number = models.PositiveSmallIntegerField(null=True, blank=True)
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField(upload_to='exam_timetable/') 

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ManyToManyField('Faculty', related_name='departments')
    def __str__(self):
        return self.name

class AcademicSession(models.Model):
    session_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    LEAVE_TYPE_CHOICES = (
        ('Casual Leave', 'Casual Leave'),
        ('Sick Leave', 'Sick Leave'),
        ('Maternity Leave', 'Maternity Leave'),
        ('Paternity Leave', 'Paternity Leave'),
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    status_changed = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = LeaveRequest.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.status_changed = timezone.now()
                self.notified = False
        super().save(*args, **kwargs)

    def get_user_type(self):
        if hasattr(self.user, 'staff'):
            return 'Staff', self.user.staff.name
        elif hasattr(self.user, 'faculty'):
            return 'Faculty', self.user.faculty.name
    def __str__(self):
        user_type, user_name = self.get_user_type()
        return f"Leave request by {user_name} ({user_type})"

class BusRoute(models.Model):
    route_name = models.CharField(max_length=25)
    bus_number = models.CharField(max_length=10)
    driver_name = models.CharField(max_length=25)
    driver_number = models.CharField(max_length=10)

class PickupLocation(models.Model):
    bus_route = models.ForeignKey(BusRoute, related_name='pickup_locations', on_delete=models.SET_NULL, null=True, default=None)
    location = models.CharField(max_length=100)
    time = models.TimeField()

class DropoffLocation(models.Model):
    bus_route = models.ForeignKey(BusRoute, related_name='dropoff_locations', on_delete=models.SET_NULL, null=True, default=None)
    location = models.CharField(max_length=100)
    time = models.TimeField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, default=None)
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    location = models.CharField(max_length=25, null=True, default=None)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, default=None)
    faculty_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    location = models.CharField(max_length=25, null=True, default=None)
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_assigned = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('class_assigned', 'section_assigned')

    def __str__(self):
        return self.name

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, default=None)
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    roll_number = models.CharField(max_length=10, unique=True)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    location = models.CharField(max_length=25, null=True, default=None)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Parents(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, default=None)
    parent_id = models.AutoField(primary_key=True)
    parent_name = models.CharField(max_length=25)
    children = models.ManyToManyField(Students)
    contact_number = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

class BusFees(models.Model):
    location = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class TuitionFees(models.Model):
    class_linked = models.OneToOneField(Class, on_delete=models.SET_NULL, null=True, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class MessFees(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Demand Draft', 'Demand Draft'),
        ('Cheque', 'Cheque'),
    )
    FEES_CHOICES = (
        ('Bus Fees', 'Bus Fees'),
        ('Mess Fees', 'Mess Fees'),
        ('Tuition Fees', 'Tuition Fees'),
    )
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True, default=None)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, default=None)
    fees_type = models.CharField(max_length=20, choices=FEES_CHOICES, null=True, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    receipt_number = models.CharField(max_length=20)
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StaffLeave(models.Model):
    month = models.CharField(max_length=20)
    staff_leaves = models.PositiveIntegerField(default=0)

class FacultyLeave(models.Model):
    month = models.CharField(max_length=20)
    faculty_leaves = models.PositiveIntegerField()

class StaffSalary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='staff_payslips/')
    month = models.CharField(max_length=20)
    year = models.IntegerField()

class FacultySalary(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='faculty_payslips/')
    month = models.CharField(max_length=20)
    year = models.IntegerField()

class FacultyAttendance(models.Model):
    file = models.FileField(upload_to='faculty_attendance/')
    date = models.DateField(auto_now_add=True)

class StaffAttendance(models.Model):
    file = models.FileField(upload_to='staff_attendance/')
    date = models.DateField(auto_now_add=True)

class StudentAttendance(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_assigned = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField(upload_to='student_attendance/')
    date = models.DateField(auto_now_add=True)

class StudentTimetable(models.Model):
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField(upload_to='student_timetable/')

class FacultyTimetable(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField(upload_to='faculty_timetable/')

class StaffTimetable(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, default=None)
    file = models.FileField(upload_to='staff_timetable/')  


class Marks(models.Model):
    class_linked = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, default=None)
    section_linked = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, default=None)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, default=None)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True,default=None)
    EXAM_TYPES = [
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
        ('Annual', 'Annual'),
        ('Unit Test', 'Unit Test'),
    ]
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    unit_test_number = models.PositiveSmallIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='student_marks/') 

