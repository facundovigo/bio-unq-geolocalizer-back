from subprocess import *
from datetime import datetime
import os, sys
import contextlib
from pathlib import Path


class AlignAndTree:
    def __init__(self, folder_name, logger):
        self.__logger = logger
        self.__folder_name = folder_name
        self.__module = "AlignAndTree"

    def align_fasta(self, input_path, threads):
        output = f"{input_path}.aligned"
        command_stdout = Popen(
            ["clustalo", f"{threads}", "-i", input_path, "-o", output], stdout=PIPE
        ).communicate()[0]

        return output

    def tree_from_align(self, input_path, bootstrap, finder):
        with self.__cd(self.__folder_name):

            if finder[0:2] == "-m":
                command_stdout = Popen(
                    ["iqtree", "-s", input_path, f"{finder[0:2]}", f"{finder[3:]}"],
                    stdout=PIPE,
                ).communicate()[0]
            else:
                command_stdout = Popen(
                    ["iqtree", "-s", input_path, "-bb", f"{bootstrap}"], stdout=PIPE
                ).communicate()[0]

        return f"{input_path}.treefile"

    @contextlib.contextmanager
    def __cd(self, path):
        CWD = os.getcwd()

        os.chdir(path)
        try:
            yield
        except:
            print("Exception caught: ", sys.exc_info()[0])
        finally:
            os.chdir(CWD)
