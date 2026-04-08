from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from qaltamda.core.mixins import SafeDeleteMixin
from .forms import ExpenseForm
from .models import Expense
from .filters import ExpenseFilter

User = get_user_model()


class ExpenseListView(LoginRequiredMixin, FilterView):
    model = Expense
    template_name = "expenses/index.html"
    context_object_name = "expenses"
    filterset_class = ExpenseFilter
    paginate_by = 20

    def get_queryset(self):
        # 1. Берем базовый набор данных (траты текущего пользователя)
        queryset = Expense.objects.filter(user=self.request.user).order_by('-date')

        # 2. Получаем текст из строки поиска
        query = self.request.GET.get('search')

        # 3. Если текст есть — фильтруем
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |  # Поиск в описании
                Q(category__name__icontains=query)  # Поиск по названию категории
            )

        return queryset

    # Этот метод сохраняет фильтр трат на время действия сессии
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        session_key = f'expense_filter_{self.request.user.id}'

        if kwargs.get('data'):
            self.request.session[session_key] = kwargs['data'].dict()
        else:
            saved_filter = self.request.session.get(session_key)
            if saved_filter:
                kwargs['data'] = saved_filter

        if self.request.GET.get('reset'):
            if session_key in self.request.session:
                del self.request.session[session_key]
            kwargs['data'] = {}

        return kwargs

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = "expenses/show.html"
    context_object_name = "expense"

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Expense
    template_name = "expenses/create.html"
    form_class = ExpenseForm
    success_url = reverse_lazy("expenses:index")
    success_message = _("Expense created successfully")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Этот метод позволяет узнать о текущем пользователе,
    # чтобы отфильтровать список категорий
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExpenseUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Expense
    template_name = "expenses/update.html"
    form_class = ExpenseForm
    success_url = reverse_lazy("expenses:index")
    success_message = _("Expense updated successfully")

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Yot have no permission to perform this action")
        )
        return redirect("expenses:index")

class ExpenseDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    SafeDeleteMixin,
    DeleteView
):
    model = Expense
    template_name = "expenses/delete.html"
    success_url = reverse_lazy("expenses:index")
    success_message = _("Expense deleted successfully")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user

    def handle_no_permission(self):
        messages.error(self.request, _("You have no permission to perform this action"))
        return redirect("users:login")