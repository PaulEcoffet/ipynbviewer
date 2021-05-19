import pygments
from pygments.lexers import PythonLexer, MarkdownLexer
from pygments.formatters import TerminalFormatter

from .output_readers import output_reader


def code_reader(cell: dict) -> str:
    """
    Return a code cell with its output in a human readable format

    :param cell: The cell dict
    :return: a human readable string of the code cell
    """
    mainstr = f"In[{cell['execution_count']}]: \n"
    instr = pygments.highlight("".join(cell["source"]), PythonLexer(), TerminalFormatter())
    instr = "\t" + "\n\t".join(instr.split("\n"))
    mainstr += instr
    mainstr += "\n\n"
    mainstr += f"Out[{cell['execution_count']}]: \n"
    outstr = output_reader(cell['outputs'])
    outstr = "\t" + "\n\t".join(outstr.split("\n"))
    mainstr += outstr
    return mainstr


def markdown_reader(cell: dict) -> str:
    """
    Return a markdown cell in a human readable format

    :param cell: The cell dict
    :return: a human readable string of the markdown cell
    """
    mainstr = pygments.highlight("".join(cell["source"]), MarkdownLexer(), TerminalFormatter())
    return mainstr


cell_readers = {
    "code": code_reader,
    "markdown": markdown_reader
}
"""`dict[str, function]` of the cell readers"""
