from django.db import models

# Create your models here.
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities'),
        ('Transportation', 'Transportation'),
        ('Others', 'Others'),
    ]
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.category})"

class Income(models.Model):
    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Freelancing', 'Freelancing'),
        ('Investments', 'Investments'),
        ('Other', 'Other'),
    ]
    source = models.CharField(max_length=100)  
    amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.source} - {self.amount} ({self.category})"

class RecurringIncome(models.Model):
    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Freelancing', 'Freelancing'),
        ('Investments', 'Investments'),
        ('Other', 'Other'),
    ]
    source = models.CharField(max_length=100)
    amount = models.FloatField()
    frequency = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Salary')

    def __str__(self):
        return f"{self.source} - {self.amount} ({self.frequency})"
    
class RecurringExpense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities'),
        ('Subscriptions', 'Subscriptions'),
        ('Others', 'Others'),
    ]
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    frequency = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Food')

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.frequency})"

class IncomeHistory(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.amount} ({self.date})"

class ExpenseLog(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.date})"

class ExpenseAlert(models.Model):
    category = models.CharField(max_length=100)
    message = models.TextField()
    level = models.CharField(max_length=50, choices=[('warning', 'Warning'), ('info', 'Info')])
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - {self.message[:30]}"

