from django.db import models


class TestCase(models.Model):
    # TODO: make stuff unique (case_id, ...)
    case_id = models.CharField(max_length=8)
    section = models.CharField(max_length=255)
    section_hierachy = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestRun(models.Model):
    ENV_DEVELOPMENT = "D"
    ENV_STAGING = "S"
    ENV_LIVE = "L"
    ENVIRONMENT_CHOICES = [
        (ENV_DEVELOPMENT, "Development"),
        (ENV_STAGING, "Staging"),
        (ENV_LIVE, "Live"),
    ]
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    environment = models.CharField(
        max_length=1, choices=ENVIRONMENT_CHOICES, default=ENV_DEVELOPMENT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestRunCase(models.Model):
    # TODO: unique together test_run test_case
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
