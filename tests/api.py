from typing import List
from django.db import IntegrityError

from django.shortcuts import get_object_or_404

from ninja import Router
from ninja.pagination import paginate
from ninja.errors import ValidationError

from .models import TestCase, TestRun, TestRunCase, Project
from .schema import *

router = Router()


"""
Project
"""
# project list
@router.get("/projects", response=List[ProjectOut])
def project_list(request):
    return Project.objects.all()


# project detail
@router.get("/projects/{project_id}", response=ProjectOut)
def project_detail(request, project_id: int):
    return get_object_or_404(Project, id=project_id)


# project create
@router.post("/projects", response=ProjectOut)
def project_create(request, data: ProjectIn):
    try:
        project = Project.objects.create(name=data.name)
    except IntegrityError:
        raise ValidationError(["A project with that name does already exist!"])
    return project


# project update
@router.patch("/projects/{project_id}", response=ProjectOut)
def project_update(request, project_id: int, payload: ProjectIn):
    project = get_object_or_404(Project, id=project_id)
    project.name = payload.name
    try:
        project.save()
    except IntegrityError:
        raise ValidationError(["A project with that name does already exist!"])
    return project


# project delete
@router.delete("/projects/{project_id}")
def project_delete(request, project_id: int):
    get_object_or_404(Project, id=project_id).delete()
    return {"success": True}


"""
Testcases
"""
# list all testcases
@router.get("/cases", response=List[TestCaseOut])
@paginate
def testcases_list(request):
    return TestCase.objects.all()


# testcase detail
@router.get("/cases/{case_id}", response=TestCaseOut)
def testcase_detail(request, case_id: int):
    return get_object_or_404(TestCase, id=case_id)


# create new testcase
@router.post("/cases", response=TestCaseOut)
def testcase_create(request, data: TestCaseIn):
    try:
        testcase = TestCase.objects.create(
            case_id=data.case_id,
            title=data.title,
            is_automation=data.is_automation,
            section_id=data.section_id,
            expected_result=data.expected_result,
            preconditions=data.preconditions,
            type=data.type,
        )
    except IntegrityError:
        raise ValidationError(["A testcase with that ID does already exist!"])
    return testcase


# update testcase
@router.patch("/cases/{case_id}", response=TestCaseOut)
def testcase_update(request, case_id: int, payload: TestCasePatch):
    testcase = get_object_or_404(TestCase, id=case_id)
    for attr, value in payload.dict().items():
        if value:
            setattr(testcase, attr, value)
    try:
        testcase.save()
    except IntegrityError:
        raise ValidationError(["A testcase with that ID does already exist!"])
    return testcase


# delete testcase
@router.delete("/cases/{case_id}")
def testcase_delete(request, case_id: int):
    get_object_or_404(TestCase, id=case_id).delete()
    return {"success": True}


"""
Testruns
"""
# list all testruns
@router.get("/runs", response=List[TestRunOut])
def testrun_list(request):
    testruns = TestRun.objects.all()
    return testruns


# create new testrun
@router.post("/runs", response=TestRunOut)
def testrun_create(request, data: TestRunIn):
    testrun = TestRun.objects.create(
        title=data.title, description=data.description, environment=data.environment
    )
    return testrun


# add TestRunCase to testrun
@router.patch("/runs/{run_id}", response=TestRunOut)
def testrun_add_cases(request, run_id: int, case_id_list: List[int]):
    testrun = get_object_or_404(TestRun, id=run_id)
    testcases = TestCase.objects.in_bulk(case_id_list)
    testruncases = [
        TestRunCase(test_run_id=run_id, test_case_id=value.id)
        for value in testcases.values()
    ]
    TestRunCase.objects.bulk_create(testruncases)
    return testrun


# delete testrun
@router.delete("/runs/{run_id}")
def testrun_delete(request, run_id: int):
    testrun = get_object_or_404(TestRun, id=run_id)
    testrun.delete()
    return {"success": True}
