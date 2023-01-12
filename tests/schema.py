from datetime import datetime

from typing import List

from ninja import Field, Schema


class ProjectOut(Schema):
    id: int
    name: str
    slug: str


class ProjectIn(Schema):
    name: str


class SectionOut(Schema):
    id: int
    section_hierachy: List[str]
    full_section_hierachy: str


class TestCaseIn(Schema):
    case_id: str
    title: str
    is_automation: bool
    section_id: int
    expected_result: str
    preconditions: str
    type: str


class TestCasePatch(Schema):
    # None to make it possible to update a single field
    case_id: str = None
    title: str = None
    is_automation: bool = None
    section_id: int = None
    exected_result: str = None
    preconditions: str = None
    type: str = None


class TestCaseOut(Schema):
    id: int
    case_id: str
    title: str
    is_automation: bool
    section: SectionOut
    expected_result: str
    preconditions: str
    type: str = Field(None, alias="get_type_display")
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
