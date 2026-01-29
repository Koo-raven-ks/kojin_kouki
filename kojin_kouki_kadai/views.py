from django.shortcuts import render


def index(request):
    return render(request, "kojin_kouki_kadai/index.html")
