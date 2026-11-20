
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    CustomerLead,
    Bank,
    LoanScheme,
    LoanApplication,
    CustomerDocument,
    CallRecord,
    FollowUp,
)
from .models import CustomerDocument


class EmployeeCreateForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
        ]

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.role = 'staff'

        if commit:
            employee.save()

        return employee


class EmployeeUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active',
        ]


class CustomerLeadForm(forms.ModelForm):

    class Meta:
        model = CustomerLead
        fields = [
            'name',
            'phone',
            'email',
            'address',
            'status',
            'remarks',
        ]

        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


class LeadAssignmentForm(forms.ModelForm):

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        empty_label="Unassigned"
    )

    class Meta:
        model = CustomerLead
        fields = ['assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = User.objects.filter(
            role='staff',
            is_active=True,
            is_superuser=False
        )

from .models import CallRecord, FollowUp


class CallRecordForm(forms.ModelForm):

    class Meta:
        model = CallRecord
        fields = [
            'call_status',
            'remarks',
        ]

        widgets = {
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter customer response or call remarks'
            })
        }


class FollowUpForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        fields = [
            'followup_date',
            'remarks',
        ]

        widgets = {
            'followup_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter follow-up details'
            })
        }
class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'contact_person', 'phone', 'email']


class LoanSchemeForm(forms.ModelForm):
    class Meta:
        model = LoanScheme
        fields = [
            'bank',
            'scheme_name',
            'interest_rate',
            'description'
        ]
class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['lead', 'bank', 'scheme', 'loan_amount', 'status']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and not (user.is_superuser or user.role == 'admin'):
            self.fields['lead'].queryset = CustomerLead.objects.filter(
                assigned_to=user
            )
            self.fields['status'].choices = [
                ('pending', 'Pending'),
                ('document_verification', 'Document Verification'),
            ]

    def clean(self):
        cleaned_data = super().clean()

        bank = cleaned_data.get('bank')
        scheme = cleaned_data.get('scheme')

        if scheme and bank and scheme.bank_id != bank.id:
            self.add_error(
                'scheme',
                'Please select a loan scheme belonging to the selected bank.'
            )

        return cleaned_data


class CustomerDocumentForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['document_type', 'file']

        widgets = {
            'document_type': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'file': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }
class DocumentVerificationForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['verification_status', 'verification_remarks']

        widgets = {
            'verification_status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'verification_remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter verification remarks'
                }
            ),
        }
class LoanApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'status',
            'status_remarks',
            'disbursed_date',
            'closed_date'
        ]

        widgets = {
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'status_remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter application status remarks'
                }
            ),

            'disbursed_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),

            'closed_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        disbursed_date = cleaned_data.get('disbursed_date')
        closed_date = cleaned_data.get('closed_date')

        if status == 'disbursed' and not disbursed_date:
            self.add_error(
                'disbursed_date',
                'Please enter the disbursement date.'
            )

        if status == 'closed' and not closed_date:
            self.add_error(
                'closed_date',
                'Please enter the closure date.'
            )

        return cleaned_data