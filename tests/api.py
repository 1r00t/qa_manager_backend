from typing import List

from django.shortcuts import get_object_or_404

from ninja import Router

from .models import TestCase, TestRun, TestRunCase
from .schema import *

router = Router()


"""
Testcases
"""
# list all testcases
@router.get("/cases", response=List[TestCaseOut])
def testcases_list(request):
    return TestCase.objects.all()


# create new testcase
@router.post("/cases", response=TestCaseOut)
def testcase_create(request, data: TestCaseIn):
    testcase = TestCase.objects.create(
        case_id=data.case_id,
        section=data.section,
        section_hierachy=data.section_hierachy,
        title=data.title,
    )
    return testcase


# update testcase
@router.patch("/cases/{case_id}", response=TestCaseOut)
def testcase_update(request, case_id: int, payload: TestCasePatch):
    testcase = get_object_or_404(TestCase, id=case_id)
    for attr, value in payload.dict().items():
        if value:
            setattr(testcase, attr, value)
    testcase.save()
    return testcase


# delete testcase
@router.delete("/cases/{case_id}")
def testcase_delete(request, case_id: int):
    testcase = get_object_or_404(TestCase, id=case_id)
    testcase.delete()
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
