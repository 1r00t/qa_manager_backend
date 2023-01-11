from typing import List
from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="sections"
    )
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
                fields=("parent_id", "name"), name="unique section for parent"
            )
        ]

    @property
    def section_hierachy(self) -> List[str]:
        if self.parent:
            yield from self.parent.section_hierachy
        yield self.name

    @property
    def full_section_hierachy(self) -> str:
        return f"/{'/'.join(self.section_hierachy)}"

    def __str__(self) -> str:
        return self.full_section_hierachy


class TestCase(models.Model):
    case_id = models.CharField(max_length=8, unique=True)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, default=None
    )
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
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="testruns"
    )
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
