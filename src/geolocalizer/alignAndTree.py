from subprocess import *
from datetime import datetime


class AlignAndTree:
    def generate_ouput_name(self, input_path, final_text="align"):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        output = f"{timestamp}_{input_path}_{final_text}"
        return output

    def align_fasta(self, input_path):
        output = self.generate_ouput_name(input_path)
        command_stdout = Popen(
            ["clustalo", "-i", input_path, "-o", output], stdout=PIPE
        ).communicate()[0]
        return output

    def tree_from_align(self, input_path, bootstrap='1000', merge=True):
        output = self.generate_ouput_name(input_path, "tree")
        if merge:
            command_stdout = Popen(["iqtree", "-s", input_path, '-m', 'MFP+MERGE', '-bb', bootstrap], stdout=PIPE).communicate()[0]
        else:
            command_stdout = Popen(["iqtree", "-s", input_path, '-bb', bootstrap], stdout=PIPE).communicate()[0]
        return output[:18]


tree = AlignAndTree()
temp = tree.align_fasta("pruebaFasta_iqtree")
print(temp)
print(tree.tree_from_align(temp))

