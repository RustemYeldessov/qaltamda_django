from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from qaltamda.core.mixins import SafeDeleteMixin # Самодельный миксин для безопасного удаления
from .forms import SectionForm
from .models import Section


class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "sections/index.html"
    context_object_name = "sections"
    paginate_by = 15

    # Скрываем данные о категориях от других пользователей
    def get_queryset(self):
        return Section.objects.filter(user=self.request.user).order_by('id', 'name')

class SectionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Section
    template_name = "sections/create.html"
    form_class = SectionForm
    success_url = reverse_lazy("sections:index")
    success_message = _("Section created successfully")

    # Автоматически подставляем юзера как автора
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SectionUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Section
    template_name = "sections/update.html"
    form_class = SectionForm
    success_url = reverse_lazy("sections:index")
    success_message = _("Section updated successfully")

    def test_func(self):
        section = self.get_object()
        return self.request.user == section.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to perform this action")
        )
        return redirect("sections:index")

class SectionDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    SafeDeleteMixin, # Иморт самодельного миксина для безопасного удаления
    DeleteView
):
    model = Section
    template_name = "sections/delete.html"
    success_url = reverse_lazy("sections:index")
    success_message = _("Sections deleted successfully")

    def test_func(self):
        section = self.get_object()
        return self.request.user == section.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to perform this action")
        )
        return redirect("sections:index")