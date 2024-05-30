from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create report-related database tables using raw SQL'

    def handle(self, *args, **kwargs):
        sql_statements = """
        CREATE TABLE Pedido (
            order_id INT PRIMARY KEY NOT NULL,
            user_id INT,
            order_date DATE,
            description VARCHAR(255),
            total_amount INT,
            status VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES Usuarios(User_Id)
        );

        CREATE TABLE Detalles_Pedidos (
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT,
            subtotal INT,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES Pedido(order_id),
            FOREIGN KEY (product_id) REFERENCES Producto(Product_id)
        );

        CREATE TABLE Solicitud (
            request_id INT PRIMARY KEY NOT NULL,
            User_id INT,
            request_date DATE,
            description VARCHAR(255),
            total_amount INT,
            status VARCHAR(255),
            FOREIGN KEY (User_id) REFERENCES Usuarios(User_Id)
        );

        CREATE TABLE Detalles_solicitud (
            request_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT,
            subtotal INT,
            PRIMARY KEY (request_id, product_id),
            FOREIGN KEY (request_id) REFERENCES Solicitud(request_id),
            FOREIGN KEY (product_id) REFERENCES Producto(Product_id)
        );
        """

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_statements)
                self.stdout.write(self.style.SUCCESS('Successfully created report-related tables'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating report-related tables: {e}'))
