from django.contrib import admin
from .models import Problem, TestCase

# Optional: Inline test cases while creating a problem
class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]  # Show test case form in problem page

admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase)
