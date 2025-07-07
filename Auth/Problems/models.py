from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    Input = models.TextField(null=True, blank=True)
    constraints = models.TextField()
    Output = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=20)
    ai_review = models.TextField(null=True, blank=True)  # 🔹 AI review field added

    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return f'TestCase for {self.problem.title}'
