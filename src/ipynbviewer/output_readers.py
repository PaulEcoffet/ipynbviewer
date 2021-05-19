"""
Module for converting outputs from cells into str
"""

import pprint

from .data_readers import data_readers, IncompatibleDataReaderException


def stream_output(output: dict):
    """
    Transform a stream output into a human readable str
    :param output:
    :return:
    """
    return "".join(output["text"])

def display_error_output(output: dict):
    """
    Transform a error output into a human readable str
    :param output: dict containing the error output
    :return str: a human readable string for the terminal
    """

    txtoutput = ""
    txtoutput += f"{output['ename']} : {output['evalue']}\n"
    txtoutput += "".join(output["traceback"])
    return txtoutput

def display_data_output(output: dict):
    """
    Transform a display_data output in a human readable str

    :param output:
    :return:
    """
    parser = None
    parser_type = None
    txtoutput = None
    for type_ in output["data"].keys():
        if type_ in data_readers:
            parser = data_readers[type_]
            parser_type = type_
            try:
                txtoutput = parser(output["data"][parser_type])
            except IncompatibleDataReaderException:
                # Parser encountered an issue and thinks it's better to try another reader
                pass
            else:
                break
    if parser is None:
        return "no support for " + str(output["data"].keys())
    else:
        return txtoutput


def output_reader(outputs: list) -> str:
    """
    Reads the list of outputs and return the string associated with it
    :param outputs:
    :return: str
    """
    outstr = []
    for output in outputs:
        try:
            outstr.append(output_readers[output["output_type"]](output))
        except KeyError:
            outstr.append(pprint.pformat(output))
    return "\n".join(outstr)


output_readers = {
    "stream": stream_output,
    "error": display_error_output,
    "display_data": display_data_output,
    "execute_result": display_data_output
}
"""`dict[str, function]` of all the functions that read an output and return a human readable string."""
