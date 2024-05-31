from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create material-related database tables using raw SQL'

    def handle(self, *args, **kwargs):
        sql_statements = """
        CREATE TABLE Piso (
            floor_id VARCHAR(255) PRIMARY KEY,
            departament_name VARCHAR(255),
            building VARCHAR(255),
            floor VARCHAR(255)
        );

        CREATE TABLE Producto (
            Product_id INT PRIMARY KEY NOT NULL,
            Name VARCHAR(255),
            unit_place VARCHAR(255),
            category VARCHAR(255),
            description VARCHAR(255),
            origins VARCHAR(255),
            sold_in_pack BOOLEAN,
            quantity VARCHAR(255)
        );

        CREATE TABLE Existencia (
            Product_id INT PRIMARY KEY NOT NULL,
            units INT,
            umbal INT,
            FOREIGN KEY (Product_id) REFERENCES Producto(Product_id)
        );

        CREATE TABLE Paquete_producto (
            Producto_id INT PRIMARY KEY NOT NULL,
            Pack_price INT,
            units INT,
            FOREIGN KEY (Producto_id) REFERENCES Producto(Product_id)
        );
        """

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_statements)
                self.stdout.write(self.style.SUCCESS('Successfully created material-related tables'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating material-related tables: {e}'))
