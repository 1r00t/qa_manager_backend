from datetime import datetime

from typing import List, Union

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


class SectionIn(Schema):
    name: str
    parent_id: Union[int, None]


class SectionPatch(Schema):
    name: str = None
    parent_id: Union[int, None] = None


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
    section: SectionOut = Field(None, alias="test_case.section")
    title: str = Field(None, alias="test_case.title")
    status: str = Field(None, alias="get_status_display")
    created_at: datetime
    updated_at: datetime


class TestRunIn(Schema):
    project_id: int
    title: str
    description: str
    environment: str


class TestRunOut(Schema):
    id: int
    project: ProjectOut
    title: str
    description: str
    environment: str = Field(None, alias="get_environment_display")
    testruncase_set: List[TestRunCaseOut]
    created_at: datetime
    updated_at: datetime
