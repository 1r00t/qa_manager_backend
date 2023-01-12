from ninja import NinjaAPI
from tests.api import project_router, section_router, testcase_router, testrun_router

api = NinjaAPI(
    title="QA Manager API",
    version="0.0.2",
    description="Manage testcases and testruns",
)

api.add_router("/projects/", project_router, tags=["Projects"])
api.add_router("/sections/", section_router, tags=["Sections"])
api.add_router("/testcases/", testcase_router, tags=["Testcases"])
api.add_router("/testruns/", testrun_router, tags=["Testruns"])
