import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from analytics.models import StudentRecord


class Command(BaseCommand):
    help = "Import gaming academic performance data from CSV into StudentRecord table"

    def handle(self, *args, **options):
        # CSV path: <project_root>/data/Gaming_Academic_Performance.csv
        csv_path = os.path.join(settings.BASE_DIR, "data", "Gaming_Academic_Performance.csv")

        if not os.path.exists(csv_path):
            raise CommandError(f"CSV file not found at: {csv_path}")

        self.stdout.write(self.style.NOTICE(f"Importing data from {csv_path}..."))

        created_count = 0

        # Open CSV and read rows
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Create a StudentRecord for each row in the CSV
                StudentRecord.objects.create(
                    student_id=int(row["student_id"]),
                    age=int(row["age"]),
                    gender=row["gender"],
                    gaming_hours=float(row["gaming_hours"]),
                    study_hours=float(row["study_hours"]),
                    sleep_hours=float(row["sleep_hours"]),
                    attendance=float(row["attendance"]),
                    gaming_genre=row["gaming_genre"],
                    social_activity=float(row["social_activity"]),
                    device_usage=float(row["device_usage"]),
                    reaction_time_ms=float(row["reaction_time_ms"]),
                    addiction_score=float(row["addiction_score"]),
                    stress_level=row["stress_level"],
                    grades=float(row["grades"]),
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {created_count} records from CSV"))