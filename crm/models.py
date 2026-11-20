
from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. User and Employee Management
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='staff'
    )
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. Customer Lead Management
class CustomerLead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('follow_up', 'Follow Up'),
        ('document_pending', 'Document Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )

    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 3. Call Records
class CallRecord(models.Model):
    CALL_STATUS = [
        ('answered', 'Answered'),
        ('not_answered', 'Not Answered'),
        ('busy', 'Busy'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
    ]

    lead = models.ForeignKey(
        CustomerLead,
        on_delete=models.CASCADE,
        related_name='calls'
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    call_status = models.CharField(
        max_length=30,
        choices=CALL_STATUS
    )

    remarks = models.TextField(blank=True)
    call_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.name} - {self.call_status}"


# 4. Follow-up Management
class FollowUp(models.Model):
    lead = models.ForeignKey(
        CustomerLead,
        on_delete=models.CASCADE,
        related_name='followups'
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    followup_date = models.DateTimeField()
    remarks = models.TextField(blank=True)

    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lead.name} - {self.followup_date}"


# 5. Bank Management
class Bank(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


# 6. Loan Scheme Management
class LoanScheme(models.Model):
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='schemes'
    )

    scheme_name = models.CharField(max_length=150)
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.scheme_name


# 7. Loan Application Management
class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('document_verification', 'Document Verification'),
        ('submitted', 'Submitted to Bank'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),
    ]


    lead = models.ForeignKey(
        CustomerLead,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        null=True
    )

    scheme = models.ForeignKey(
        LoanScheme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )
    status_remarks = models.TextField(blank=True)
    disbursed_date = models.DateField(
        null=True,
        blank=True
    )

    closed_date = models.DateField(
        null=True,
        blank=True
    )

    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.name} - {self.loan_amount}"


# 8. Customer Document Management
class CustomerDocument(models.Model):
    DOCUMENT_TYPES = [
        ('identity', 'Identity Proof'),
        ('address', 'Address Proof'),
        ('income', 'Income Proof'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    ]

    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )
    file = models.FileField(upload_to='customer_documents/')
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    verification_remarks = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.lead.name} - {self.document_type}"
# 9. Daily Call Target Management
class DailyTarget(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='daily_targets'
    )

    target_date = models.DateField()
    call_target = models.PositiveIntegerField(default=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'target_date'],
                name='unique_employee_daily_target'
            )
        ]

    def __str__(self):
        return f"{self.employee.username} - {self.target_date}"
