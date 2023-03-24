import click
from prettytable import PrettyTable


class MVTPrinter:
    """Print the given info as a beautiful table"""

    def print(self, fields: list or tuple, rows: list or tuple):
        """
        Print the given info as a beautiful table
        :param: fields: List with the name of the fields to be printed in the table
        :param: rows: List with the values of every row in the table
        """
        table = PrettyTable()
        table.field_names = fields
        for row in rows:
            table.add_row(row)

        click.echo(table)
