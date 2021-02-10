import json
import argparse

from cell_readers import cell_readers


def read_ipynb(ipynb_dict: dict)-> str:
    """
    Reads a whole notebook and output it in a human readable format
    :param ipynb_dict:
    :return: the human readable string
    """
    outstr = []
    try:
        cells = ipynb_dict["cells"]
    except KeyError:
        raise ValueError("Not an ipython notebook")
    for cell in cells:
        outstr.append(cell_readers[cell["cell_type"]](cell))
    return ("\n\n" + "-" * 80 + "\n\n").join(outstr)


def main():
    agp = argparse.ArgumentParser()
    agp.add_argument("file", type=argparse.FileType("r"))
    args = agp.parse_args()
    print(read_ipynb(json.load(args.file)))


if __name__ == "__main__":
    main()