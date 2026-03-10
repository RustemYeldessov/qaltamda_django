from django.contrib import messages
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from tengecash.core.mixins import SafeDeleteMixin
from .forms import CategoryForm
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/index.html'
    context_object_name = 'categories'
    paginate_by = 15

    # Скрываем данные о категориях от других пользователей
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('id', 'name')

class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/create.html'
    success_url = reverse_lazy('categories:index')
    success_message = _('Category created successfully')

    # Автоматически подставляем юзера как автора
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Category
    template_name = 'categories/update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('categories:index')
    success_message = _('Category updated successfully')

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to perform this action")
        )
        return redirect("categories:index")

class CategoryDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    SafeDeleteMixin,
    DeleteView
):
    model = Category
    template_name = 'categories/delete.html'
    success_url = reverse_lazy('categories:index')
    success_message = _('Category deleted successfully')

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to perform this action")
        )
        return redirect("categories:index")


@login_required
def category_toggle_favorite(request, pk):
    # Ищем категорию, принадлежащую именно этому юзеру
    category = get_object_or_404(Category, pk=pk, user=request.user)
    # Меняем значение на противоположное
    category.is_favorite = not category.is_favorite
    category.save()
    # Возвращаемся обратно на страницу списка
    return redirect('categories:index')