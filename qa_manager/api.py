from ninja import NinjaAPI
from tests.api import router as tests_router

api = NinjaAPI(
    title="QA Manager API",
    version="0.0.1",
    description="Manage testcases and testruns",
)

api.add_router("/tests/", tests_router, tags=["tests"])
