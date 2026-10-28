import io
import uuid
import qrcode
from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone

class CertificateApplication(models.Model):
    CERT_TYPES = [
        ('BIRTH', 'Birth Registration Certificate'),
        ('RESIDENCY', 'Local Residency Recommendation'),
        ('RELATION', 'Relationship Verification Certificate'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('APPROVED', 'Approved & Issued'),
        ('REJECTED', 'Rejected'),
    ]

    # Application details
    tracking_id = models.CharField(max_length=16, unique=True, editable=False)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    certificate_type = models.CharField(max_length=20, choices=CERT_TYPES)
    supporting_doc = models.FileField(upload_to='applicant_docs/')

    # Officer review fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    officer_remarks = models.TextField(blank=True, null=True)

    # Issued certificate security details
    certificate_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate a clean tracking ID like GOV-A1B2C3D4
        if not self.tracking_id:
            self.tracking_id = f"GOV-{uuid.uuid4().hex[:8].upper()}"

        # When an officer marks it APPROVED, automatically generate the verification QR code
        if self.status == 'APPROVED' and not self.qr_code:
            self.issued_at = timezone.now()
            
            # The QR code points directly to the verification page
            verify_url = f"http://127.0.0.1:8000/verify/{self.certificate_uuid}/"
            qr = qrcode.make(verify_url)
            
            buffer = io.BytesIO()
            qr.save(buffer, format='PNG')
            file_name = f"qr_{self.tracking_id}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} - {self.full_name} ({self.status})"