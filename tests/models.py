from typing import List
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


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
                fields=("parent_id", "name"), name="unique section for parent"
            )
        ]

    @property
    def all_child_testcases(self):
        if self.children:
            for child in self.children.all():
                yield from child.all_child_testcases
        yield self.testcase_set.all()

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
    class TestType(models.TextChoices):
        NONE = "none", _("None")
        SMOKE = "smoke", _("Smoke")
        FUNCTIONAL = "functional", _("Functional")

    case_id = models.CharField(max_length=8, unique=True)
    title = models.CharField(max_length=500)
    is_automation = models.BooleanField(default=False)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, default=None
    )
    expected_result = models.CharField(max_length=500, blank=True)
    preconditions = models.CharField(max_length=500, blank=True)
    test_type = models.CharField(
        choices=TestType.choices,
        default=TestType.NONE,
        name="type",
        max_length=max(len(v) for v in TestType.values),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.case_id


class TestRun(models.Model):
    class Environment(models.TextChoices):
        DEVELOPMENT = "dev", _("Development")
        STAGING = "staging", _("Staging")
        LIVE = "live", _("Live")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="testruns"
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    environment = models.CharField(
        choices=Environment.choices,
        default=Environment.DEVELOPMENT,
        max_length=max(len(v) for v in Environment.values),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class TestResult(models.Model):
    class Status(models.TextChoices):
        UNTESTED = "untested", _("Untested")
        PASSED = "passed", _("Passed")
        FAILED = "failed", _("Failed")
        SKIPPED = "skipped", _("Skipped")
        RETEST = "retest", _("Retest")

    class Priority(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(
        choices=Status.choices,
        default=Status.UNTESTED,
        max_length=max(len(v) for v in Status.values),
    )
    priority = models.CharField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        max_length=max(len(v) for v in Priority.values),
    )
    details = models.CharField(max_length=255, blank=True)
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
