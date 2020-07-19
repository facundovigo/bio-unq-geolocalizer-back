from src.geolocalizer.parser import Parser
from src.geolocalizer.geo_services import GeoServices
from src.geolocalizer.alignAndTree import AlignAndTree
from src.geolocalizer.canvas import Canvas
import sys, getopt


if __name__ == "__main__":
    
    email = f'rizziromanalejandro@gmail.com'
    if (sys.argv[1].__str__ == "h") or (len(sys.argv) != 3):
        print('case of use:   test.py file_align table_accessions')
    else:
        try:
            parsed_fasta = Parser().parse(
                "tests/sequences/geolocalized_seqs.fasta", write_output=True
            )
           
            geo_services = GeoServices(email)
            geo_seqs = geo_services.geolocalize_seqs(parsed_fasta["seqs"])
            align_and_tree = AlignAndTree()
            output_path = align_and_tree.align_fasta(parsed_fasta["output_path"])
            tree_path = align_and_tree.tree_from_align(output_path)
        except getopt.GetoptError:
            print('test.py file_align table_accessions')