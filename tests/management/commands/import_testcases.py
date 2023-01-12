from pathlib import Path
from typing import Any, Optional

import csv

# case_id
# title
# is_automation
# section
# expected_result
# preconditions
# test_type
# created_at
# updated_at

# 'ID', 'Title', 'Automation Type', 'Automation required?', 'Created By', 'Created On', 'Estimate', 'Expected Result', 'Forecast', 'Goals', 'Mission', 'PR link', 'Preconditions', 'Priority', 'References', 'Section', 'Section Depth', 'Section Description', 'Section Hierarchy', 'Steps', 'Steps (Additional Info)', 'Steps (Expected Result)', 'Steps (References)', 'Steps (Shared step ID)', 'Steps (Step)', 'Suite', 'Suite ID', 'Template', 'Ticket URL', 'Ticket link', 'Type', 'Updated By', 'Updated On'

from django.core.management.base import BaseCommand, CommandError, CommandParser
from tests.models import TestCase, Section
import os.path


class Command(BaseCommand):
    help = "import csv testcases"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_file", nargs="+", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        csv_filepath = options["csv_file"][0]
        if not os.path.isfile(csv_filepath):
            raise CommandError(f"could not find file {csv_filepath}")

        with open(csv_filepath) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                # create sections
                db_sections = []
                section_hierachy = [
                    section.strip()
                    for section in row["Section Hierarchy"].strip().split(">")
                ]
                for i, section in enumerate(section_hierachy):
                    parent = None if i == 0 else db_sections[i - 1]

                    new_section, created = Section.objects.get_or_create(
                        name=section, parent=parent
                    )
                    db_sections.append(new_section)

                # create testcases
                new_test_dict = {
                    "case_id": row["ID"],
                    "title": row["Title"],
                    "is_automation": True
                    if row["Automation required?"] == "Yes"
                    else False,
                    "section_id": db_sections[-1].id,
                    "expected_result": row["Expected Result"],
                    "preconditions": row["Preconditions"],
                    "type": TestCase.TestType.SMOKE
                    if row["Type"].startswith("Smoke")
                    else TestCase.TestType.FUNCTIONAL,
                }
                new_testcase, create = TestCase.objects.get_or_create(**new_test_dict)
        return
