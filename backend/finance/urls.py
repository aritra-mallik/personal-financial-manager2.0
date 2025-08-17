from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_income/', views.add_income, name='add_income'),
    path('category_manager/', views.category_manager, name='category_manager'),
    path('expense_alerts/', views.expense_alerts, name='expense_alerts'),
    path('expense_log/', views.expense_log, name='expense_log'),
    path('income_history/', views.income_history, name='income_history'),
    path('payment_analysis/', views.payment_analysis, name='payment_analysis'),
    path('recurring_expense/', views.recurring_expense, name='recurring_expense'),
    path('recurring_income/', views.recurring_income, name='recurring_income'),
    path('trends/', views.trends, name='trends'),
]
