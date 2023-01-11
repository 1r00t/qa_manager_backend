from django.db import models


class Section(models.Model):
    parent = models.ForeignKey(
        "self",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "name"), name="unique section for parent"
            )
        ]

    def __str__(self) -> str:
        return self.name


class TestCase(models.Model):
    case_id = models.CharField(max_length=8, unique=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.case_id


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

    def __str__(self) -> str:
        return self.title


class TestRunCase(models.Model):
    # TODO: unique together test_run test_case
    UNTESTED = "U"
    PASSED = "P"
    FAILED = "F"
    SKIPPED = "S"
    RETEST = "R"
    STATUS_CHOICES = [
        (UNTESTED, "Untested"),
        (PASSED, "Passed"),
        (FAILED, "Failed"),
        (SKIPPED, "Skipped"),
        (RETEST, "Retest"),
    ]
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=UNTESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("test_run", "test_case"), name="unique testcase for run"
            )
        ]

    def __str__(self) -> str:
        return f"Run #{self.test_run.pk} - Case: {self.test_case.case_id}"
