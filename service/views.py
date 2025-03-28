from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import EnrollRiderForm, RiderLoginForm, BookServiceForm, ServiceBookingRecord,AssignMechanicForm,UpdateStatusForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .invoice_tools import (
    format_euros,
    estimate_service_duration,
    calculate_service_cost,
    generate_invoice_number
)




def enroll_new_rider(request):
    if request.method == 'POST':
        form = EnrollRiderForm(request.POST)
        if form.is_valid():
            new_rider = form.save()
            login(request, new_rider)
            return redirect('my_dashboard')
    else:
        form = EnrollRiderForm()
    return render(request, 'signup_page.html', {'form': form})

def welcome_rider(request):
    if request.method == 'POST':
        form = RiderLoginForm(request.POST)
        if form.is_valid():
            rider_username = form.cleaned_data['username']
            rider_password = form.cleaned_data['password']
            legit_rider = authenticate(request, username=rider_username, password=rider_password)

            if legit_rider:
                login(request, legit_rider)
                if legit_rider.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('my_dashboard')
            else:
                form.add_error(None, "Invalid login details, try again.")
    else:
        form = RiderLoginForm()
    return render(request, 'login_page.html', {'form': form})


@login_required
def my_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def rider_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def arrange_bike_service(request):
    if request.method == 'POST':
        form = BookServiceForm(request.POST)
        if form.is_valid():
            booking_record = form.save(commit=False)
            booking_record.booked_by = request.user
            booking_record.save()
            return redirect('my_booking_list')
    else:
        form = BookServiceForm()
    return render(request, 'book_service_page.html', {'form': form})

@login_required
def my_booking_list(request):
    my_services = ServiceBookingRecord.objects.filter(booked_by=request.user)
    return render(request, 'my_bookings.html', {'services': my_services})

@login_required
def edit_my_booking(request, booking_id):
    booking = get_object_or_404(ServiceBookingRecord, id=booking_id, booked_by=request.user)
    if request.method == 'POST':
        form = BookServiceForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('my_booking_list')
    else:
        form = BookServiceForm(instance=booking)
    return render(request, 'edit_service_page.html', {'form': form})

@login_required
def cancel_my_booking(request, booking_id):
    booking = get_object_or_404(ServiceBookingRecord, id=booking_id, booked_by=request.user)
    booking.delete()
    return redirect('my_booking_list')

@staff_member_required
def list_unassigned_bookings(request):
    waiting_services = ServiceBookingRecord.objects.filter(mechanic_assigned__isnull=True, service_status='Pending')
    return render(request, 'unassigned_services_page.html', {'waiting_services': waiting_services})

@staff_member_required
def assign_mechanic(request, booking_id):
    service = get_object_or_404(ServiceBookingRecord, id=booking_id)
    if request.method == 'POST':
        form = AssignMechanicForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            service.service_status = 'In Progress'
            service.save()
            return redirect('list_unassigned_bookings')
    else:
        form = AssignMechanicForm(instance=service)
    return render(request, 'assign_mechanic_page.html', {'form': form, 'booking': service})

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_home_page.html')

@staff_member_required
def see_all_bookings(request):
    all_services = ServiceBookingRecord.objects.all().order_by('-service_date')
    return render(request, 'all_bookings_admin.html', {'all_services': all_services})

@staff_member_required
def update_service_status(request, booking_id):
    booking = get_object_or_404(ServiceBookingRecord, id=booking_id)
    
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('see_all_bookings')
    else:
        form = UpdateStatusForm(instance=booking)
    
    return render(request, 'update_status_page.html', {'form': form, 'booking': booking})


@login_required
def view_invoice(request, booking_id):
    booking = get_object_or_404(ServiceBookingRecord, id=booking_id, booked_by=request.user)

    if booking.service_status != 'Completed':
        return HttpResponse("Invoice available only after completion.", status=403)

    template_path = 'invoice_template.html'

    selected_service_type = "general"

    context = {
        'booking': booking,
        'invoice_id': generate_invoice_number(),
        'formatted_amount': format_euros(calculate_service_cost(selected_service_type)),
        'estimated_time': estimate_service_duration(selected_service_type),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{booking_id}.pdf'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating invoice', status=500)

    return response

