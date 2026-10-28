from django.shortcuts import render, get_object_or_404
from .models import CertificateApplication

def home_view(request):
    if request.method == 'POST':
        app = CertificateApplication.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            certificate_type=request.POST.get('certificate_type'),
            supporting_doc=request.FILES.get('supporting_doc')
        )
        return render(request, 'certificates/success.html', {'tracking_id': app.tracking_id})
    return render(request, 'certificates/apply.html')

def track_view(request):
    application = None
    query = request.GET.get('tracking_id')
    if query:
        application = CertificateApplication.objects.filter(tracking_id=query.strip().upper()).first()
    return render(request, 'certificates/track.html', {'application': application, 'query': query})

def verify_view(request, cert_uuid):
    cert = get_object_or_404(CertificateApplication, certificate_uuid=cert_uuid)
    return render(request, 'certificates/verify.html', {'cert': cert})

def print_certificate(request, cert_uuid):
    cert = get_object_or_404(CertificateApplication, certificate_uuid=cert_uuid, status='APPROVED')
    return render(request, 'certificates/certificate.html', {'cert': cert})