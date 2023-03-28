import click
from prettytable import PrettyTable


class MVTPrinter:
    """Print the given info as a beautiful table"""

    def print(self, fields: list or tuple, rows: list or tuple):
        """
        Print the given info as a beautiful table
        :param: fields: list with the name of the fields to be printed in the table
        :param: rows: list with the values of every row in the table
        """
        table = PrettyTable()
        table.field_names = fields
        for row in rows:
            # Check if the lenght of the given rows and the given columns are the same
            if len(row) != len(fields):
                continue
            table.add_row(row)

        click.echo(table)
