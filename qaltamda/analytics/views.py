from django.utils import timezone
from datetime import date
from django.db.models import Sum
from django.shortcuts import render
from qaltamda.expenses.models import Expense
from django.contrib.auth.decorators import login_required


@login_required
def expenses_statistics_view(request):
    today = timezone.now().date()
    user = request.user
    session_key = f'statistics_filter_{request.user.id}'

    if request.GET.get('reset'):
        if session_key in request.session:
            del request.session[session_key]
        from django.shortcuts import redirect
        return redirect('analytics:statistics')

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str and not end_date_str:
        saved_filters = request.session.get(session_key, {})
        start_date_str = saved_filters.get('start_date')
        end_date_str = saved_filters.get('end_date')
    else:
        request.session[session_key] = {
            'start_date': start_date_str,
            'end_date': end_date_str
        }

    try:
        if start_date_str:
            start_date = date.fromisoformat(start_date_str)
        else:
            start_date = today.replace(day=1)

        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
        else:
            end_date = today
    except ValueError:
        start_date = today.replace(day=1)
        end_date = today

    user_expenses = Expense.objects.filter(user=user)
    # 1. Общая статистика (за всё время)
    total_count = user_expenses.count()
    total_sum = user_expenses.aggregate(total=Sum("amount"))['total'] or 0

    # 2. Статистика за сегодня
    count_today = user_expenses.filter(date=today).count()
    sum_today = user_expenses.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0

    # 3. Траты по категориям ЗА ТЕКУЩИЙ МЕСЯЦ
    # Сначала фильтруем, потом группируем
    expenses_by_category = (
        user_expenses.filter(date__gte=start_date, date__lte=end_date)
        .values("category__name")
        .annotate(sum=Sum("amount"))
        .order_by("-sum")
    )

    total_sum_by_period = expenses_by_category.aggregate(total=Sum('sum'))['total'] or 0

    context = {
        'count_today': count_today,
        'sum_today': sum_today,
        'total_count': total_count,
        'total_sum': total_sum,
        'today': today,
        'start_date': start_date,
        'end_date': end_date,
        'expenses_by_category': expenses_by_category,
        'total_sum_by_period': total_sum_by_period,
    }

    return render(request, 'analytics/statistics.html', context)