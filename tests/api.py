from typing import List

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Q, Value, IntegerField

from ninja import Router
from ninja.pagination import paginate
from ninja.errors import ValidationError

from .models import TestCase, TestRun, TestResult, Project, Section
from .schema import *

project_router = Router()
section_router = Router()
testcase_router = Router()
testrun_router = Router()


"""
Project
"""
# project list
@project_router.get("", response=List[ProjectOut])
def project_list(request):
    return Project.objects.all()


# project detail
@project_router.get("{project_id}/", response=ProjectOut)
def project_detail(request, project_id: int):
    return get_object_or_404(Project, id=project_id)


# project create
@project_router.post("", response=ProjectOut)
def project_create(request, data: ProjectIn):
    try:
        project = Project.objects.create(name=data.name)
    except IntegrityError:
        raise ValidationError(["A project with that name does already exist!"])
    return project


# project update
@project_router.patch("{project_id}/", response=ProjectOut)
def project_update(request, project_id: int, data: ProjectIn):
    project = get_object_or_404(Project, id=project_id)
    project.name = data.name
    try:
        project.save()
    except IntegrityError:
        raise ValidationError(["A project with that name does already exist!"])
    return project


# project delete
@project_router.delete("{project_id}/")
def project_delete(request, project_id: int):
    get_object_or_404(Project, id=project_id).delete()
    return {"success": True}


"""
Section
"""
# section list
@section_router.get("", response=List[SectionOut])
def section_list(request):
    return Section.objects.all()


# section tree
@section_router.get("tree/", response=List[SectionTreeOut])
def section_tree(request):
    return Section.objects.filter(parent=None)


# section detail
@section_router.get("{section_id}/", response=SectionOut)
def section_detail(request, section_id: int):
    return get_object_or_404(Section, id=section_id)


# section create
@section_router.post("", response=SectionOut)
def section_create(request, data: SectionIn):
    try:
        section = Section.objects.create(**data.dict())
    except IntegrityError:
        raise ValidationError(
            ["A Section with that name already exists in that parent!"]
        )
    return section


# section update
@section_router.patch("{section_id}/", response=SectionOut)
def section_update(request, section_id: int, data: SectionPatch):
    section = get_object_or_404(Section, id=section_id)
    for attr, value in data.dict().items():
        if value:
            setattr(section, attr, value)
    try:
        section.save()
    except IntegrityError:
        raise ValidationError(
            ["A Section with that name already exists in that parent!"]
        )
    return section


# section delete
@section_router.delete("{section_id}/")
def section_delete(request, section_id: int):
    get_object_or_404(Section, id=section_id).delete()
    return {"success": True}


"""
Testcases
"""
# testcase list
@testcase_router.get("", response=List[TestCaseOut])
@paginate()
def testcases_list(request):
    return TestCase.objects.all()


@testcase_router.post("by_id/", response=List[TestCaseOut])
@paginate()
def testcases_by_id(request, testcase_ids: List[int]):
    return TestCase.objects.filter(id__in=testcase_ids)


@testcase_router.post("search/", response=List[TestCaseOut])
def testcases_search(request, query: str):
    # TODO: when using postgres use this search! Or even better, look at django search docs
    # testcases = TestCase.objects.filter(title__unaccent__lower__trigram_similar=query)
    testcases = TestCase.objects.filter(
        Q(title__icontains=query) | Q(section__name__icontains=query)
    )
    return testcases


# testcase detail
@testcase_router.get("{case_id}/", response=TestCaseOut)
def testcase_detail(request, case_id: int):
    return get_object_or_404(TestCase, id=case_id)


@testcase_router.get("section/{section_id}/", response=List[TestCaseOut])
def testcases_by_section(request, section_id: int):
    section = get_object_or_404(Section, id=section_id)
    testcases = []
    for testcases_queryset in section.all_child_testcases:
        for testcase in testcases_queryset:
            testcases.append(testcase)
    return testcases


# testcase create
@testcase_router.post("", response=TestCaseOut)
def testcase_create(request, data: TestCaseIn):
    try:
        testcase = TestCase.objects.create(**data.dict())
    except IntegrityError:
        raise ValidationError(["A testcase with that ID does already exist!"])
    return testcase


# testcase update
@testcase_router.patch("{case_id}/", response=TestCaseOut)
def testcase_update(request, case_id: int, data: TestCasePatch):
    testcase = get_object_or_404(TestCase, id=case_id)
    for attr, value in data.dict().items():
        if value:
            setattr(testcase, attr, value)
    try:
        testcase.save()
    except IntegrityError:
        raise ValidationError(["A testcase with that ID does already exist!"])
    return testcase


# testcase delete
@testcase_router.delete("{case_id}/")
def testcase_delete(request, case_id: int):
    get_object_or_404(TestCase, id=case_id).delete()
    return {"success": True}


"""
Testruns
"""
# testrun list
@testrun_router.get("", response=List[TestRunOut])
def testrun_list(request):
    testruns = TestRun.objects.all()
    return testruns


# testrun detail
@testrun_router.get("{run_id}/", response=TestRunOut)
def testrun_detail(request, run_id: int):
    return get_object_or_404(TestRun, id=run_id)


# testruns by project
@testrun_router.get("project/{project_slug}/", response=List[TestRunOut])
def testrun_by_project(request, project_slug: str):
    return get_object_or_404(Project, slug=project_slug).testruns


# testrun create
@testrun_router.post("", response=TestRunOut)
def testrun_create(request, data: TestRunIn):
    testrun = TestRun.objects.create(**data.dict())
    return testrun


# testrun add testresults
@testrun_router.patch("{run_id}/add-cases/", response=TestRunOut)
def testrun_add_cases(request, run_id: int, case_id_list: List[int]):
    testrun = get_object_or_404(TestRun, id=run_id)
    testcases = TestCase.objects.in_bulk(case_id_list)
    testresults = [
        TestResult(test_run_id=run_id, test_case_id=value.id)
        for value in testcases.values()
    ]
    TestResult.objects.bulk_create(testresults)
    return testrun


# testrun remove testresults
@testrun_router.patch("{run_id}/remove-cases/", response=List[int])
def testrun_remove_cases(request, run_id: int, case_id_list: List[int]):
    testresults = TestResult.objects.filter(
        test_run_id=run_id, test_case_id__in=case_id_list
    )
    removed_ids = list(testresults.values_list("id", flat=True))
    testresults.delete()
    return removed_ids


# testrun delete
@testrun_router.delete("{run_id}/")
def testrun_delete(request, run_id: int):
    get_object_or_404(TestRun, id=run_id).delete()
    return {"success": True}
