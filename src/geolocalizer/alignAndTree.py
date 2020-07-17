from subprocess import *
from datetime import datetime
import os, sys
import contextlib
from pathlib import Path


class AlignAndTree:
    def generate_file_extension(self):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        output = f"{timestamp}_clustalo_aligned"
        return output

    def align_fasta(self, input_path):
        ext = self.generate_file_extension()
        output = f"{input_path}{ext}"
        command_stdout = Popen(
            ["clustalo", "-i", input_path, "-o", output], stdout=PIPE
        ).communicate()[0]
        return output

    def tree_from_align(self, input_path, bootstrap="1000", merge=True):
        with self.__cd("tmp/"):
            if merge:
                command_stdout = Popen(
                    ["iqtree", "-s", input_path, "-m", "MFP+MERGE", "-bb", bootstrap],
                    stdout=PIPE,
                ).communicate()[0]
            else:
                command_stdout = Popen(
                    ["iqtree", "-s", input_path, "-bb", bootstrap], stdout=PIPE
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
