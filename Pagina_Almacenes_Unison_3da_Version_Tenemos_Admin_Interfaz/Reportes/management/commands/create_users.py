from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create user-related database tables using raw SQL'

    def handle(self, *args, **kwargs):
        sql_statements = """
        CREATE TABLE Usuarios (
            User_Id INT PRIMARY KEY NOT NULL,
            Name VARCHAR(255),
            lastname VARCHAR(255),
            floor_id VARCHAR(255)
        );

        CREATE TABLE Cuenta (
            User_Id INT PRIMARY KEY NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            rol VARCHAR(255),
            is_active BOOLEAN,
            is_staff BOOLEAN,
            is_superuser BOOLEAN,
            FOREIGN KEY (User_Id) REFERENCES Usuarios(User_Id)
        );

        CREATE TABLE Login (
            User_Id INT NOT NULL,
            day DATE NOT NULL,
            hour TIME NOT NULL,
            PRIMARY KEY (User_Id, day, hour),
            FOREIGN KEY (User_Id) REFERENCES Usuarios(User_Id)
        );
        """

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_statements)
                self.stdout.write(self.style.SUCCESS('Successfully created user-related tables'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user-related tables: {e}'))
