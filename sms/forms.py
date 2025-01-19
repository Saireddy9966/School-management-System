from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory, formset_factory
from .models import *
import datetime


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password","confirm_password"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different username.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            if commit:
                user.save()
        return user
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name", "email", "gender", "phone_number", "location"]
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Staff.objects.filter(name=name).exists():
            raise forms.ValidationError("Staff with this name already exists.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Staff.objects.filter(email=email).exists():
            raise forms.ValidationError("Staff with this email already exists.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Staff.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Staff with this phone number already exists.")
        return phone_number
    
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ["name", "email", "gender", "phone_number", "location", 'class_assigned', 'section_assigned']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Faculty.objects.filter(name=name).exists():
            raise forms.ValidationError("Staff with this name already exists.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Faculty.objects.filter(email=email).exists():
            raise forms.ValidationError("Staff with this email already exists.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Faculty.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Staff with this phone number already exists.")
        return phone_number
    

    def clean(self):
        cleaned_data = super().clean()
        class_assigned = cleaned_data.get("class_assigned")
        section_assigned = cleaned_data.get("section_assigned")

        if Faculty.objects.filter(class_assigned=class_assigned, section_assigned=section_assigned).exists():
            raise forms.ValidationError("This class and section combination is already assigned to another faculty.")

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["name", "email", "roll_number", "class_name", "section_linked", "location"]
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Students.objects.filter(name=name).exists():
            raise forms.ValidationError("Name already exists.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Students.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
    
    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Students.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("Roll number already exists.")
        return roll_number
    
class ParentsForm(forms.ModelForm):
    class Meta:
        model = Parents
        fields = ["parent_name", "children", "contact_number", "location"]
    
    def clean_parent_name(self):
        parent_name = self.cleaned_data.get('parent_name')
        if Parents.objects.filter(parent_name=parent_name).exists():
            raise forms.ValidationError("Parent name already exists.")
        return parent_name
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if Parents.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact_number
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = StudentAdmission
        fields = '__all__'

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'class_linked']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subjectname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjectname'].required = True  # Ensure the field is required
        self.fields['subjectname'].error_messages = {
            'required': 'Subject name is required.'
        }

SubjectFormSet = formset_factory(SubjectForm, extra=1)            

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['file']


class DepartmentForm(forms.ModelForm):
    faculty = forms.ModelMultipleChoiceField(
        queryset=Faculty.objects.all(),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Department
        fields = ['name', 'faculty']
    
class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['session_name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'id': 'start_date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'id': 'end_date'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date.year > 9999:
            raise forms.ValidationError("Year must have 4 digits or fewer.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date.year > 9999:
            raise forms.ValidationError("Year must have 4 digits or fewer.")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if start_date and end_date are valid
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")
        return cleaned_data

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = [ 'leave_type','reason','start_date', 'end_date']

class BusFeesForm(forms.ModelForm):
    class Meta:
        model = BusFees
        fields = [ 'location','amount']

class TuitionFeesForm(forms.ModelForm):
    class Meta:
        model = TuitionFees
        fields = [ 'class_linked','amount']        

class MessFeesForm(forms.ModelForm):
    class Meta:
        model = MessFees
        fields = [ 'amount']

class StaffLeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        fields = ['month', 'staff_leaves']

class FacultyLeaveForm(forms.ModelForm):
    class Meta:
        model = FacultyLeave
        fields = ['month', 'faculty_leaves']

class StaffSalaryForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('', 'Select Month'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    current_year = datetime.datetime.now().year
    YEAR_CHOICES = [('', 'Select Year')] + [(year, year) for year in range(current_year - 1, current_year + 1)]

    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Select Month")
    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Select Year")
    class Meta:
        model = StaffSalary
        fields = ['staff', 'file', 'month', 'year']

class FacultySalaryForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('', 'Select Month'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    current_year = datetime.datetime.now().year
    YEAR_CHOICES = [('', 'Select Year')] + [(year, year) for year in range(current_year - 1, current_year + 1)]

    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Select Month")
    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Select Year")
    class Meta:
        model = FacultySalary
        fields = ['faculty', 'file', 'month', 'year']

class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ['route_name', 'bus_number', 'driver_name', 'driver_number']

class FacultyAttendanceForm(forms.ModelForm):
    class Meta:
        model = FacultyAttendance
        fields = ['file']

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendance
        fields = ['file']

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ['file']        


class StudentTimetableForm(forms.ModelForm):
    class Meta:
        model = StudentTimetable  
        fields = ['file']       

class FacultyTimetableForm(forms.ModelForm):
    class Meta:
        model = FacultyTimetable
        fields = ['faculty', 'file']

class StaffTimetableForm(forms.ModelForm):
    class Meta:
        model = StaffTimetable
        fields = ['staff', 'file']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks 
        fields = ['file'] 


