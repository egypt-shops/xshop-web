from django.shortcuts import render


def manager(request):
    return render(request, "dashboard/manager.html")


def cashier(request):
    return render(request, "dashboard/cashier.html")


def data_entry(request):
    return render(request, "dashboard/data_entry.html")
