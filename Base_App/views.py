from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from Base_App.models import (
    Items,
    FoodCategory,
    Feedback,
    BookTable,
    Coupon,
    Offer,
    AboutUs,
)
from datetime import date


# Home Page View
def HomeView(request):
    items = Items.objects.prefetch_related("categories").all()
    categories = FoodCategory.objects.all()
    reviews = Feedback.objects.all()

    return render(
        request,
        "home.html",
        {"items": items, "categories": categories, "reviews": reviews},
    )


# About Us View
def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, "about.html", {"data": data})


# Menu View
def MenuView(request):
    # Use `.prefetch_related()` for Many-to-Many relationship and offers
    items = Items.objects.prefetch_related("categories", "offers").all()
    categories = FoodCategory.objects.all()

    # Apply offer discounts
    for item in items:
        for offer in item.offers.filter(is_active=True):
            if offer.is_valid():
                discount = (item.price * offer.discount_percentage) / 100
                item.discounted_price = item.price - discount
            else:
                item.discounted_price = item.price

    return render(request, "menu.html", {"items": items, "categories": categories})


# Table Booking View
def BookTableView(request):
    if request.method == "POST":
        name = request.POST.get("user_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("user_email")
        total_person = request.POST.get("total_person")
        booking_data = request.POST.get("booking_data")

        if (
            name
            and len(phone_number) == 10
            and email
            and total_person.isdigit()
            and int(total_person) > 0
            and booking_data
        ):
            data = BookTable(
                name=name,
                phone_number=phone_number,
                email=email,
                total_person=int(total_person),
                booking_date=booking_data,
            )
            data.save()
            return redirect("Book_Table")

    return render(request, "Book_Table.html")


# Feedback View
def FeedbackView(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        description = request.POST.get("description")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        if user_name and description and rating:
            feedback = Feedback(
                user_name=user_name,
                description=description,
                rating=rating,
                image=image,
            )
            feedback.save()
            return redirect("feedback")

    return render(request, "feedback.html")


# Apply Coupon View (for AJAX requests)
def ApplyCouponView(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")

        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)

            if coupon.is_valid():
                return JsonResponse(
                    {
                        "success": True,
                        "discount_type": coupon.discount_type,
                        "discount_value": float(coupon.discount_value),
                    }
                )
            else:
                return JsonResponse(
                    {"success": False, "message": "Coupon expired or inactive"}
                )
        except Coupon.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid coupon"})

    return JsonResponse({"success": False, "message": "Invalid request"})
