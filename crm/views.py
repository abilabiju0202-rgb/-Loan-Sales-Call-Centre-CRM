from .models import Bank, LoanScheme
from .forms import BankForm, LoanSchemeForm
import csv
import io

from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.utils import timezone
from datetime import timedelta
from .models import CallRecord, DailyTarget, FollowUp
from .forms import CallRecordForm, FollowUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import User, CustomerLead
from .forms import (
    EmployeeCreateForm,
    EmployeeUpdateForm,
    CustomerLeadForm,
    LeadAssignmentForm
)
from .forms import LoanApplicationForm, CustomerDocumentForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum

from .models import (
    User,
    CustomerLead,
    CallRecord,
    FollowUp,
    LoanApplication,
    CustomerDocument,
)
from .forms import DocumentVerificationForm
from .forms import LoanApplicationStatusForm


def is_admin(user):
    return user.is_superuser or user.role == 'admin'


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'crm/login.html')


@login_required
def dashboard(request):

    if is_admin(request.user):

        context = {
            'total_leads': CustomerLead.objects.count(),
            'total_staff': User.objects.filter(
    role='staff',
    is_active=True,
    is_superuser=False
).count(),
            'total_calls': CallRecord.objects.count(),
            'total_applications': LoanApplication.objects.count(),
            'interested_leads': CustomerLead.objects.filter(
                status='interested'
            ).count(),
            'recent_leads': CustomerLead.objects.order_by(
                '-created_at'
            )[:5],
        }

        return render(
            request,
            'crm/admin_dashboard.html',
            context
        )

    else:

        assigned_leads = CustomerLead.objects.filter(
            assigned_to=request.user
        )

        context = {
            'total_leads': assigned_leads.count(),
            'total_calls': CallRecord.objects.filter(
                employee=request.user
            ).count(),
            'interested_leads': assigned_leads.filter(
                status='interested'
            ).count(),
            'recent_leads': assigned_leads.order_by(
                '-created_at'
            )[:5],
        }

        return render(
            request,
            'crm/staff_dashboard.html',
            context
        )


@login_required
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('dashboard')

@login_required
def employee_list(request):

    if not is_admin(request.user):
        return redirect('dashboard')

    employees = User.objects.filter(
        role='staff',
        is_superuser=False
    ).order_by('-date_joined')

    return render(
        request,
        'crm/employee_list.html',
        {'employees': employees}
    )

@login_required
def employee_add(request):

    if not is_admin(request.user):
        return redirect('dashboard')

    form = EmployeeCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Employee added successfully!')
        return redirect('employee_list')

    return render(
        request,
        'crm/employee_form.html',
        {'form': form, 'title': 'Add Employee'}
    )

@login_required
def employee_edit(request, employee_id):

    if not is_admin(request.user):
        return redirect('dashboard')

    employee = get_object_or_404(
        User,
        id=employee_id,
        role='staff',
        is_superuser=False
    )

    form = EmployeeUpdateForm(
        request.POST or None,
        instance=employee
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Employee updated successfully!')
        return redirect('employee_list')

    return render(
        request,
        'crm/employee_form.html',
        {'form': form, 'title': 'Edit Employee'}
    )

@login_required
def employee_toggle_status(request, employee_id):

    if not is_admin(request.user):
        return redirect('dashboard')

    if request.method == 'POST':

        employee = get_object_or_404(
            User,
            id=employee_id,
            role='staff',
            is_superuser=False
        )

        employee.is_active = not employee.is_active
        employee.save(update_fields=['is_active'])

        messages.success(
            request,
            'Employee status updated successfully!'
        )

    return redirect('employee_list')

@login_required
def lead_list(request):

    if is_admin(request.user):
        leads = CustomerLead.objects.select_related(
            'assigned_to'
        ).all()
    else:
        leads = CustomerLead.objects.filter(
            assigned_to=request.user
        )

    search = request.GET.get('search', '').strip()

    if search:
        leads = leads.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search)
        )

    leads = leads.order_by('-created_at')

    return render(
        request,
        'crm/lead_list.html',
        {'leads': leads, 'search': search}
    )

@login_required
def lead_add(request):

    if not is_admin(request.user):
        return redirect('dashboard')

    form = CustomerLeadForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer lead added successfully!')
        return redirect('lead_list')

    return render(
        request,
        'crm/lead_form.html',
        {'form': form, 'title': 'Add Customer Lead'}
    )

@login_required
def lead_edit(request, lead_id):

    if not is_admin(request.user):
        return redirect('dashboard')

    lead = get_object_or_404(CustomerLead, id=lead_id)

    form = CustomerLeadForm(
        request.POST or None,
        instance=lead
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Lead updated successfully!')
        return redirect('lead_list')

    return render(
        request,
        'crm/lead_form.html',
        {'form': form, 'title': 'Edit Customer Lead'}
    )

@login_required
def lead_delete(request, lead_id):

    if not is_admin(request.user):
        return redirect('dashboard')

    lead = get_object_or_404(CustomerLead, id=lead_id)

    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Lead deleted successfully!')
        return redirect('lead_list')

    return redirect('lead_list')

@login_required
def lead_assign(request, lead_id):

    if not is_admin(request.user):
        return redirect('dashboard')

    lead = get_object_or_404(CustomerLead, id=lead_id)

    form = LeadAssignmentForm(
        request.POST or None,
        instance=lead
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            'Lead assigned successfully!'
        )
        return redirect('lead_list')

    return render(
        request,
        'crm/lead_assign.html',
        {
            'form': form,
            'lead': lead
        }
    )

@login_required
def call_centre(request):

    if is_admin(request.user):
        leads = CustomerLead.objects.select_related(
            'assigned_to'
        ).all()
    else:
        leads = CustomerLead.objects.filter(
            assigned_to=request.user
        )

    return render(
        request,
        'crm/call_centre.html',
        {'leads': leads}
    )

@login_required
def record_call(request, lead_id):

    lead = get_object_or_404(CustomerLead, id=lead_id)

    if not is_admin(request.user):
        if lead.assigned_to_id != request.user.id:
            return redirect('call_centre')

    if request.method == 'POST':
        form = CallRecordForm(request.POST)

        if form.is_valid():

            call = form.save(commit=False)
            call.lead = lead
            call.employee = request.user
            call.save()

            # Update lead status based on call outcome
            if call.call_status == 'interested':
                lead.status = 'interested'

            elif call.call_status == 'not_interested':
                lead.status = 'not_interested'

            elif call.call_status in ['not_answered', 'busy']:
                lead.status = 'follow_up'

            lead.save()

            messages.success(
                request,
                'Call record saved successfully!'
            )

            return redirect('call_centre')

    else:
        form = CallRecordForm()

    return render(
        request,
        'crm/record_call.html',
        {'form': form, 'lead': lead}
    )

@login_required
def call_performance(request):

    today = timezone.localdate()

    target, created = DailyTarget.objects.get_or_create(
        employee=request.user,
        target_date=today,
        defaults={'call_target': 100}
    )

    completed_calls = CallRecord.objects.filter(
        employee=request.user,
        call_date__date=today
    ).count()

    percentage = min(
        round((completed_calls / target.call_target) * 100)
        if target.call_target else 0,
        100
    )

    context = {
        'target': target,
        'completed_calls': completed_calls,
        'remaining_calls': max(
            target.call_target - completed_calls, 0
        ),
        'percentage': percentage,
    }

    return render(
        request,
        'crm/call_performance.html',
        context
    )

@login_required
def followup_list(request):

    if is_admin(request.user):
        followups = FollowUp.objects.select_related(
            'lead', 'employee'
        ).all()
    else:
        followups = FollowUp.objects.filter(
            employee=request.user
        ).select_related('lead', 'employee')

    followups = followups.order_by(
        'completed', 'followup_date'
    )

    return render(
        request,
        'crm/followup_list.html',
        {'followups': followups}
    )


@login_required
def followup_add(request, lead_id):

    lead = get_object_or_404(CustomerLead, id=lead_id)

    if not is_admin(request.user):
        if lead.assigned_to_id != request.user.id:
            return redirect('call_centre')

    if request.method == 'POST':
        form = FollowUpForm(request.POST)

        if form.is_valid():

            followup = form.save(commit=False)
            followup.lead = lead
            followup.employee = request.user
            followup.save()

            lead.status = 'follow_up'
            lead.save(update_fields=['status'])

            messages.success(
                request,
                'Follow-up scheduled successfully!'
            )

            return redirect('followup_list')

    else:
        form = FollowUpForm()

    return render(
        request,
        'crm/followup_form.html',
        {'form': form, 'lead': lead}
    )


@login_required
def followup_complete(request, followup_id):

    if request.method == 'POST':

        followup = get_object_or_404(
            FollowUp,
            id=followup_id
        )

        if (
            is_admin(request.user)
            or followup.employee_id == request.user.id
        ):
            followup.completed = True
            followup.save(update_fields=['completed'])

            messages.success(
                request,
                'Follow-up marked as completed!'
            )

    return redirect('followup_list')

@login_required
def bulk_lead_upload(request):

    if not is_admin(request.user):
        return redirect('dashboard')

    imported_count = 0
    errors = []

    if request.method == 'POST':

        uploaded_file = request.FILES.get('csv_file')

        if not uploaded_file:
            errors.append("Please select a CSV file.")

        elif not uploaded_file.name.lower().endswith('.csv'):
            errors.append("Only CSV files are allowed.")

        elif uploaded_file.size > 5 * 1024 * 1024:
            errors.append("File size must not exceed 5 MB.")

        else:
            try:
                decoded_file = uploaded_file.read().decode('utf-8-sig')

                reader = csv.DictReader(io.StringIO(decoded_file))

                if not reader.fieldnames:
                    errors.append("The CSV file is empty.")

                else:
                    reader.fieldnames = [
                        field.strip().lower()
                        for field in reader.fieldnames
                        if field
                    ]

                    required_columns = {'name', 'phone'}

                    if not required_columns.issubset(set(reader.fieldnames)):
                        errors.append(
                            "CSV must contain at least name and phone columns."
                        )

                    else:
                        valid_statuses = dict(
                            CustomerLead.STATUS_CHOICES
                        )

                        status_labels = {
                            label.lower(): key
                            for key, label in CustomerLead.STATUS_CHOICES
                        }

                        leads_to_create = []

                        for row_number, row in enumerate(reader, start=2):

                            name = (row.get('name') or '').strip()
                            phone = (row.get('phone') or '').strip()
                            email = (row.get('email') or '').strip()
                            address = (row.get('address') or '').strip()
                            status = (row.get('status') or 'new').strip().lower()
                            remarks = (row.get('remarks') or '').strip()

                            row_errors = []

                            if not name:
                                row_errors.append("Customer name is required.")

                            if not phone:
                                row_errors.append("Phone number is required.")

                            elif len(phone) > 15:
                                row_errors.append(
                                    "Phone number cannot exceed 15 characters."
                                )

                            if email:
                                try:
                                    validate_email(email)
                                except ValidationError:
                                    row_errors.append("Invalid email address.")

                            if status in status_labels:
                                status = status_labels[status]

                            if status not in valid_statuses:
                                row_errors.append("Invalid customer status.")

                            if row_errors:
                                errors.append(
                                    f"Row {row_number}: " + " ".join(row_errors)
                                )
                                continue

                            leads_to_create.append(
                                CustomerLead(
                                    name=name,
                                    phone=phone,
                                    email=email,
                                    address=address,
                                    status=status,
                                    remarks=remarks,
                                    assigned_to=None
                                )
                            )

                        if leads_to_create:
                            CustomerLead.objects.bulk_create(
                                leads_to_create
                            )

                            imported_count = len(leads_to_create)

            except UnicodeDecodeError:
                errors.append(
                    "Unable to read the file. Please save it as UTF-8 CSV."
                )

            except csv.Error:
                errors.append("The CSV file contains invalid formatting.")

    return render(
        request,
        'crm/bulk_lead_upload.html',
        {
            'imported_count': imported_count,
            'errors': errors
        }
    )

@login_required
def download_sample_csv(request):

    if not is_admin(request.user):
        return redirect('dashboard')

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="customer_leads_sample.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'name',
        'phone',
        'email',
        'address',
        'status',
        'remarks'
    ])

    writer.writerow([
        'Rahul Thomas',
        '9876501234',
        'rahul@example.com',
        'Kochi, Kerala',
        'new',
        'Personal loan enquiry'
    ])

    writer.writerow([
        'Anjali Mary',
        '9876501235',
        'anjali@example.com',
        'Thrissur, Kerala',
        'interested',
        'Interested in home loan'
    ])

    writer.writerow([
        'John Mathew',
        '9876501236',
        'john@example.com',
        'Ernakulam, Kerala',
        'follow_up',
        'Needs another call'
    ])

    return response

# Bank Management
@login_required
def bank_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')

    banks = Bank.objects.all().order_by('name')

    return render(request, 'crm/bank_list.html', {
        'banks': banks
    })


@login_required
def bank_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')

    if request.method == 'POST':
        form = BankForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Bank added successfully.')
            return redirect('bank_list')
    else:
        form = BankForm()

    return render(request, 'crm/bank_form.html', {
        'form': form,
        'title': 'Add Bank'
    })


@login_required
def bank_edit(request, bank_id):
    if not is_admin(request.user):
        return redirect('dashboard')

    bank = get_object_or_404(Bank, id=bank_id)

    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)

        if form.is_valid():
            form.save()
            messages.success(request, 'Bank updated successfully.')
            return redirect('bank_list')
    else:
        form = BankForm(instance=bank)

    return render(request, 'crm/bank_form.html', {
        'form': form,
        'title': 'Edit Bank'
    })


# Loan Scheme Management
@login_required
def scheme_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')

    schemes = LoanScheme.objects.select_related('bank').all().order_by('scheme_name')

    return render(request, 'crm/scheme_list.html', {
        'schemes': schemes
    })


@login_required
def scheme_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoanSchemeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Loan scheme added successfully.')
            return redirect('scheme_list')
    else:
        form = LoanSchemeForm()

    return render(request, 'crm/scheme_form.html', {
        'form': form,
        'title': 'Add Loan Scheme'
    })


@login_required
def scheme_edit(request, scheme_id):
    if not is_admin(request.user):
        return redirect('dashboard')

    scheme = get_object_or_404(LoanScheme, id=scheme_id)

    if request.method == 'POST':
        form = LoanSchemeForm(request.POST, instance=scheme)

        if form.is_valid():
            form.save()
            messages.success(request, 'Loan scheme updated successfully.')
            return redirect('scheme_list')
    else:
        form = LoanSchemeForm(instance=scheme)

    return render(request, 'crm/scheme_form.html', {
        'form': form,
        'title': 'Edit Loan Scheme'
    })

# Loan Application Management

@login_required
def application_list(request):

    if is_admin(request.user):
        applications = LoanApplication.objects.select_related(
            'lead', 'bank', 'scheme'
        ).all()
    else:
        applications = LoanApplication.objects.filter(
            lead__assigned_to=request.user
        ).select_related('lead', 'bank', 'scheme')

    applications = applications.order_by('-applied_date')

    return render(
        request,
        'crm/application_list.html',
        {'applications': applications}
    )


@login_required
def application_add(request):

    if request.method == 'POST':
        form = LoanApplicationForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Loan application created successfully!'
            )
            return redirect('application_list')

    else:
        form = LoanApplicationForm(user=request.user)

    return render(
        request,
        'crm/application_form.html',
        {
            'form': form,
            'title': 'Create Loan Application'
        }
    )
@login_required
def document_list(request, application_id):
    application = get_object_or_404(
        LoanApplication,
        id=application_id
    )

    if not is_admin(request.user):
        if application.lead.assigned_to != request.user:
            messages.error(request, "You are not authorized to view these documents.")
            return redirect('application_list')

    documents = application.documents.all().order_by('-uploaded_at')

    return render(request, 'crm/document_list.html', {
        'application': application,
        'documents': documents,
    })


@login_required
def document_upload(request, application_id):
    application = get_object_or_404(
        LoanApplication,
        id=application_id
    )

    if not is_admin(request.user):
        if application.lead.assigned_to != request.user:
            messages.error(request, "You are not authorized to upload documents.")
            return redirect('application_list')

    if request.method == 'POST':
        form = CustomerDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()

            messages.success(request, "Document uploaded successfully!")
            return redirect('document_list', application_id=application.id)

    else:
        form = CustomerDocumentForm()

    return render(request, 'crm/document_upload.html', {
        'form': form,
        'application': application,
    })
@login_required
def admin_document_verification(request):
    if not is_admin(request.user):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('staff_dashboard')

    documents = CustomerDocument.objects.select_related(
        'application',
        'application__lead',
        'application__bank'
    ).order_by('-uploaded_at')

    return render(request, 'crm/admin_document_verification.html', {
        'documents': documents
    })
@login_required
def verify_document(request, document_id):
    if not is_admin(request.user):
        messages.error(request, "You are not authorized to verify documents.")
        return redirect('staff_dashboard')

    document = get_object_or_404(CustomerDocument, id=document_id)

    if request.method == 'POST':
        form = DocumentVerificationForm(request.POST, instance=document)

        if form.is_valid():
            form.save()
            messages.success(request, "Document verification status updated successfully!")
            return redirect('admin_document_verification')

    else:
        form = DocumentVerificationForm(instance=document)

    return render(request, 'crm/verify_document.html', {
        'form': form,
        'document': document,
    })
@login_required
def update_application_status(request, application_id):

    if not is_admin(request.user):
        messages.error(
            request,
            "You are not authorized to update application status."
        )
        return redirect('staff_dashboard')

    application = get_object_or_404(
        LoanApplication,
        id=application_id
    )

    if request.method == 'POST':
        form = LoanApplicationStatusForm(
            request.POST,
            instance=application
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Loan application status updated successfully!"
            )

            return redirect('application_list')

    else:
        form = LoanApplicationStatusForm(instance=application)

    return render(
        request,
        'crm/update_application_status.html',
        {
            'form': form,
            'application': application
        }
    )
@login_required
def reports_analytics(request):

    if not is_admin(request.user):
        messages.error(request, "You are not authorized to access reports.")
        return redirect('dashboard')

    today = timezone.localdate()

    # Lead statistics
    total_leads = CustomerLead.objects.count()

    lead_status_report = CustomerLead.objects.values(
        'status'
    ).annotate(
        total=Count('id')
    ).order_by('status')

    # Call statistics
    total_calls = CallRecord.objects.count()

    today_calls = CallRecord.objects.filter(
        call_date__date=today
    ).count()

    # Employee performance
    staff_members = User.objects.filter(
        role='staff',
        is_active=True,
        is_superuser=False
    ).order_by('username')

    employee_performance = []

    for employee in staff_members:
        employee_performance.append({
            'employee': employee,
            'total_calls': CallRecord.objects.filter(
                employee=employee
            ).count(),
            'today_calls': CallRecord.objects.filter(
                employee=employee,
                call_date__date=today
            ).count(),
        })

    # Loan application statistics
    total_applications = LoanApplication.objects.count()

    application_status_report = LoanApplication.objects.values(
        'status'
    ).annotate(
        total=Count('id')
    ).order_by('status')

    total_loan_amount = LoanApplication.objects.aggregate(
        total=Sum('loan_amount')
    )['total'] or 0

    # Disbursement statistics
    disbursed_applications = LoanApplication.objects.filter(
        status='disbursed'
    )

    total_disbursed = disbursed_applications.count()

    total_disbursed_amount = disbursed_applications.aggregate(
        total=Sum('loan_amount')
    )['total'] or 0

    context = {
        'total_leads': total_leads,
        'lead_status_report': lead_status_report,
        'total_calls': total_calls,
        'today_calls': today_calls,
        'employee_performance': employee_performance,
        'total_applications': total_applications,
        'application_status_report': application_status_report,
        'total_loan_amount': total_loan_amount,
        'total_disbursed': total_disbursed,
        'total_disbursed_amount': total_disbursed_amount,
    }

    return render(
        request,
        'crm/reports_analytics.html',
        context
    )