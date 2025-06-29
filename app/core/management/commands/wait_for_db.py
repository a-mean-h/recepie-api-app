"""
Django command to wait for database to be available
"""
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    """
    Django command to wait for database
    """
    def handle(self, *args, **kwargs):
        """Entry point for command"""
        self.stdout.write("Waiting for database ...🙄🙄🙄")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available! 🎉🎉🎉"))
