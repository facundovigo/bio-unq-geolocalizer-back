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

    def tree_from_align(self, input_path):
        output = self.generate_ouput_name(input_path, "tree")
        command_stdout = Popen(
            ["clustalo", "-i", input_path, f"--guidetree-out={output}"], stdout=PIPE
        ).communicate()[0]
        return output[18:]

    def tree_from_fasta(self, input_path):
        output = self.tree_from_align(self.align_fasta(input_path))
        return output


"""
CASO DE USO

salchicha = AlignAndTree()
print(salchicha.tree_from_fasta('fasta_nombre[Especie]*Ciudad*Pais'))
"""
