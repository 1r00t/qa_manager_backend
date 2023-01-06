from django.db import models


class TestCase(models.Model):
    case_id = models.CharField(max_length=8)
    section = models.CharField(max_length=255)
    section_hierachy = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)


class TestRunCase(models.Model):
    UNTESTED = "U"
    PASSED = "P"
    FAILED = "F"
    SKIPPED = "S"
    RETEST = "R"
    STATUS_CHOICES = [
        (UNTESTED, "untested"),
        (PASSED, "passed"),
        (FAILED, "failed"),
        (SKIPPED, "skipped"),
        (RETEST, "retest"),
    ]
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=UNTESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
