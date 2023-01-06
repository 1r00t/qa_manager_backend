from datetime import datetime

from typing import List

from ninja import Field, Schema


class TestCaseIn(Schema):
    case_id: str
    section: str
    section_hierachy: str
    title: str


class TestCasePatch(Schema):
    case_id: str = None
    section: str = None
    section_hierachy: str = None
    title: str = None


class TestCaseOut(Schema):
    id: int
    case_id: str
    section: str
    section_hierachy: str
    title: str
    created_at: datetime
    updated_at: datetime


class TestRunCaseOut(Schema):
    id: int
    case_id: str = Field(None, alias="test_case.case_id")
    section: str = Field(None, alias="test_case.section")
    section_hierachy: str = Field(None, alias="test_case.section_hierachy")
    title: str = Field(None, alias="test_case.title")
    status: str
    created_at: datetime
    updated_at: datetime


class TestRunIn(Schema):
    title: str
    description: str
    environment: str


class TestRunOut(Schema):
    id: int
    title: str
    description: str
    environment: str
    testruncase_set: List[TestRunCaseOut]
    created_at: datetime
    updated_at: datetime
