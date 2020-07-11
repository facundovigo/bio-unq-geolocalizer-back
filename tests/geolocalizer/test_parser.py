from src.geolocalizer.parser import Parser
from src.geolocalizer.parser import InvalidFileError
import pytest

class TestParser:
  def test_fails_if_file_is_not_supported(self):
    invalid_file_path = 'tests/sequences/invalid_file.txt'

    with pytest.raises(InvalidFileError):
      Parser().parse(invalid_file_path)

  def test_reads_fasta_file(self):
    expected_header = 'cytochrome c [Homo sapiens]'
    expected_seq = 'MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE'
    seq_path = 'tests/sequences/geolocalized_seqs.fasta'

    parsed_seqs = Parser().parse(seq_path)['seqs']

    assert expected_header == parsed_seqs[0]['description']
    assert expected_seq == parsed_seqs[0]['seq']

  def test_reads_geolocalized_fasta_file(self):
    expected_lat = '-34.706501'
    expected_long = '-58.27853'
    seq_path = 'tests/sequences/geolocalized_seqs.fasta'

    parsed_seqs = Parser().parse(seq_path)['seqs']

    assert expected_lat == parsed_seqs[0]['latitude']
    assert expected_long == parsed_seqs[0]['longitude']

  def test_reads_genbank_accession_id(self):
    expected_genbank_id = 'NP_061820.1'
    seq_path = 'tests/sequences/geolocalized_seqs.fasta'

    parsed_seqs = Parser().parse(seq_path)['seqs']

    assert expected_genbank_id == parsed_seqs[0]['genbank_id']

  def test_only_use_max_types_of_seqs(self):
    protein_header = 'Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1'
    seq_path = 'tests/sequences/mismatch_seqs.fasta'

    parsed_seqs = Parser().parse(seq_path)['seqs']
    descriptions = map(lambda s: s['description'], parsed_seqs)

    assert protein_header not in descriptions





