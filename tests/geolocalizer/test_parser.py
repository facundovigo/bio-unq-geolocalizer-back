from src.geolocalizer.parser import Parser
from src.geolocalizer.parser import InvalidFileError
import pytest


class TestParser:
    def test_fails_if_file_is_not_supported(self):
        invalid_file_path = "sequences/invalid_file.txt"

        with pytest.raises(InvalidFileError):
            Parser().parse(invalid_file_path)

    def test_reads_fasta_file(self):
        expected_header = "gi|87137207|gb|DQ362940.1|"
        expected_seq = (
            "ATGTCTTGGAAAGTGGTGATCATTTTTTCATTGTTAATAACACCTCAACA"
            "CGGTCTTAAAGAGAGCTATTTAGAAGAGTCATGTAGCACTATAACTGAAG"
            "GATATCTCAGTGTTCTGAGGACAGGTTGGTATACCAACGTTTTTACA"
            "CTGGAGGTAGGTGATGTAGAGAACCTTACATGTGCTGATGGACCTAGCTT"
            "AATAAAAACAGAATTAGACCTGACCAAAAGTGCACTAAGA"
            "GAGCTCAGAACAGTTTCTGCTGATCAACTGGCAAGAGAGGAGCAAATTGA"
            "GAATCCCAGACAATCTAGATTTGTTCTAGGAGCAATAGCACTCGGTGTTG"
            "CAACAGCAGCTGCAGTTACAGCAGGTGTTGCAATTGCCAAAACCATCCGG"
            "CTTGAAAGTGAAGTAACAGCAATTAAGAATGCCCTCAAAAAGACCAATGA"
            "AGCAGTATCTACATTGGGGAATGGAGTTCGAGTGTTGGCAACTGCAGT"
            "GAGGGAGCTGAAAGATTTTGTGAGCAAGAATCTAACACGTGCAATCAACA"
            "AAAACAAGTGCGACATTGCTGACCTGAAAATGGCCGTTAGCTTCAGTCAA"
            "TTCAACAGAAGGTTTCTAAATGTTGTGCGGCAATTTTCAGACAATGCTGG"
            "AATAACACCAGCAATATCCTTGGACTTAATGACAGATGCTGAACTAGCCA"
            "GAGCTGTTTCCAACATGCCAACATCTGCAGGACAAATAAAACTGATGTTG"
            "GAGAACCGTGCAATGGTAAGAAGAAAGGGGTTCGGAATCCTGATAGGAGT"
            "TTACGGAAGCTCCGTAATTTACATGG"
        )
        seq_path = "tests/sequences/examples.fst"

        parsed_seqs = Parser().parse(seq_path)["seqs"]

        assert expected_header == parsed_seqs[0]["description"]
        assert expected_seq == parsed_seqs[0]["seq"].strip()

    def test_reads_genbank_accession_id(self):
        expected_accession_number = "DQ362940.1"
        expected_gen_info = "87137207"
        seq_path = "tests/sequences/examples.fst"

        parsed_seqs = Parser().parse(seq_path)["seqs"]

        assert expected_gen_info == parsed_seqs[0]["genbank_accession"]
        assert expected_accession_number == parsed_seqs[0]["genbank_gen_info"]

    def test_only_use_max_types_of_seqs(self):
        protein_header = (
            "Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1"
        )
        seq_path = "tests/sequences/mismatch_seqs.fasta"

        parsed_seqs = Parser().parse(seq_path)["seqs"]
        descriptions = map(lambda s: s["description"], parsed_seqs)

        assert protein_header not in descriptions
