from unicodedata import category
from django.shortcuts import render, redirect
from .models import Expense, Income, RecurringIncome, RecurringExpense, IncomeHistory, ExpenseLog, ExpenseAlert
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import datetime
import calendar

# Create your views here.
def dashboard(request):
    return render(request, 'finance/dashboard.html')

def add_expense(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = float(request.POST.get('amount'))
        date = request.POST.get('date')
        category = request.POST.get('category')
        Expense.objects.create(name=name, amount=amount, date=date, category=category)
        return redirect('add_expense')

    categories = ['Food', 'Rent', 'Utilities', 'Transportation', 'Others']
    chart_data=[]
    for cat in categories:
        total = Expense.objects.filter(category=cat).aggregate(Sum('amount'))['amount__sum'] or 0
        chart_data.append(total)
        
    context={
        'categories': categories,
        'chart_data': chart_data,
    }
    return render(request, 'finance/add_expense.html', context)

def add_income(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        amount = float(request.POST.get('amount'))
        date = request.POST.get('date')
        category = request.POST.get('category')
        Income.objects.create(source=source, amount=amount, date=date, category=category)
        return redirect('add_income')

    categories = ['Salary', 'Freelancing', 'Investments', 'Other']
    chart_data = []
    for cat in categories:
        total = Income.objects.filter(category=cat).aggregate(Sum('amount'))['amount__sum'] or 0
        chart_data.append(total)

    context = {
        'categories': categories,
        'chart_data': chart_data,
        'today': timezone.now().date(),
    }
    return render(request, 'finance/add_income.html', context)


def category_manager(request):
    return render(request, 'finance/category_manager.html')

def expense_alerts(request):
    alerts = ExpenseAlert.objects.all()
    
    category = {}
    for alert in alerts:
        category[alert.category] = category.get(alert.category, 0) + 1

    context={
        "alerts" : alerts,
        "categories" : list(category.keys()),
        "counts" : list(category.values())
    }
    return render(request, 'finance/expense_alerts.html', context)

def expense_log(request):
    expenses = Expense.objects.all().order_by('-date')
    
    labels = [expense.date.strftime('%Y-%m-%d') for expense in expenses]
    data = [expense.amount for expense in expenses]
    
    context={
        'expenses': expenses,
        'labels': labels,
        'data': data,
    }
    return render(request, 'finance/expense_log.html', context)

def income_history(request):
    incomes = Income.objects.all().order_by('-date')

    labels=[income.date.strftime('%Y-%m-%d') for income in incomes]
    data=[income.amount for income in incomes]

    context={
        'incomes': incomes,
        'labels': labels,
        'data': data,
    }
    return render(request, 'finance/income_history.html', context)

def payment_analysis(request):
    return render(request, 'finance/payment_analysis.html')

def recurring_expense(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = float(request.POST.get('amount'))
        frequency = request.POST.get('frequency')
        category = request.POST.get('category')
        RecurringExpense.objects.create(name=name, amount=amount, frequency=frequency, category=category)
        return redirect('recurring_expense')
    
    expenses = RecurringExpense.objects.all()
    categories = [exp.name for exp in expenses]
    chart_data = [exp.amount for exp in expenses]

    context = {
        'expenses': expenses,
        'categories': categories,
        'chart_data': chart_data,
    }
    return render(request, 'finance/recurring_expense.html', context)

def recurring_income(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        amount = float(request.POST.get('amount'))
        frequency = request.POST.get('frequency')
        category = request.POST.get('category')
        RecurringIncome.objects.create(source=source, amount=amount, frequency=frequency, category=category)
        return redirect('recurring_income')
    incomes = RecurringIncome.objects.all()
    categories=[ inc.source for inc in incomes]
    chart_data = [ inc.amount for inc in incomes]

    context = {
        'incomes': incomes,
        'categories': categories,
        'chart_data': chart_data,
    }
    return render(request, 'finance/recurring_income.html', context)

def trends(request):
    incomes = Income.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount'))
    expenses = Expense.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount'))
    
    income_dict = {income['month']: income['total'] for income in incomes}
    expense_dict = {expense['month']: expense['total'] for expense in expenses}
    
    for r in RecurringIncome.objects.all():
        start = r.start_date.replace(day=1)
        end = datetime.date.today().replace(day=1)
        current = start

        while start <= end:
            income_dict[current] = income_dict.get(current, 0) + r.amount
            # advance one month
            month = current.month + 1 if current.month < 12 else 1
            year = current.year if current.month < 12 else current.year + 1
            current = datetime.date(year, month, 1)
    
    for r in RecurringExpense.objects.all():
        start = r.start_date.replace(day=1)
        end = datetime.date.today().replace(day=1)
        current = start

        while start <= end:
            expense_dict[current] = expense_dict.get(current, 0) + r.amount
            # advance one month
            month = current.month + 1 if current.month < 12 else 1
            year = current.year if current.month < 12 else current.year + 1
            current = datetime.date(year, month, 1)
            
    all_months = sorted(set(income_dict.keys()) | set(expense_dict.keys()))
    labels = [calendar.month_name[m.month] for m in all_months]
    income_data = [float(income_dict.get(m, 0)) for m in all_months]
    expense_data = [float(expense_dict.get(m, 0)) for m in all_months]

    context = {
        'labels': labels,
        'income_data': income_data,
        'expense_data': expense_data,
        'table_data': zip(labels, income_data, expense_data),
    }
    return render(request, 'finance/trends.html', context)

from django.db.models import Sum
from django.db.models.functions import ExtractWeek

def dashboard(request):
    # Total income and expenses
    income_total = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    balance = income_total - expense_total

    # Example: Monthly income & expense trend (Jan–Jun, grouped by month)
    monthly_income = (
        Income.objects.values_list('date__month').annotate(total=Sum('amount')).order_by('date__month')
    )
    monthly_expense = (
        Expense.objects.values_list('date__month').annotate(total=Sum('amount')).order_by('date__month')
    )

    # Convert into dict for easy lookup
    income_dict = {month: total for month, total in monthly_income}
    expense_dict = {month: total for month, total in monthly_expense}

    # Ensure all 12 months are covered (fill missing with 0)
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    income_data = [income_dict.get(i+1, 0) for i in range(12)]
    expense_data = [expense_dict.get(i+1, 0) for i in range(12)]

    # Category-wise expense
    category_expenses = (
        Expense.objects.values('category').annotate(total=Sum('amount')).order_by('-total')
    )
    category_labels = [c['category'] for c in category_expenses]
    category_values = [c['total'] for c in category_expenses]

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "months": months,
        "income_data": income_data,
        "expense_data": expense_data,
        "category_labels": category_labels,
        "category_values": category_values,
    }
    return render(request, "finance/dashboard.html", context)



