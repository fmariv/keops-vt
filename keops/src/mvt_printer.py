import click
from prettytable import PrettyTable


class MVTPrinter:
    """Print the given info as a beautiful table"""

    def print(self, fields: list, rows: list):
        """

        """
        table = PrettyTable()
        table.field_names = fields
        for row in rows:
            table.add_row(row)

        click.echo(table)
