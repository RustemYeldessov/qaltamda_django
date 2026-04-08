from django.shortcuts import render
from django.views import View
from django.contrib import messages


class IndexView(View):
    def get(self, request):
        if request.session.pop('just_logged_out', False):
            messages.success(request, "You are logged in")
        return render(request, 'index.html')