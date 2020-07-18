from src.geolocalizer.parser import Parser
from src.geolocalizer.geo_services import GeoServices
from src.geolocalizer.alignAndTree import AlignAndTree
from src.geolocalizer.canvas import Canvas
import sys, getopt



if __name__ == "__main__":

    if (sys.argv[1].__str__ == "h") | (len(sys.argv) != 3):
        print('case of use:   test.py file_align table_accessions')
    else:
        try:
            parsed_fasta = Parser().parse(
                f'src/files/{sys.argv[1]}', write_output=True
            )
            geo_services = GeoServices()
            countries = geo_services.get_countries_from_xls(
                f'src/files/{sys.argv[2]}'
            )
            geo_seqs = geo_services.get_location_for_idseq(parsed_fasta["seqs"], countries)
            align_and_tree = AlignAndTree()
            output_path = align_and_tree.align_fasta(parsed_fasta["output_path"])
            tree_path = align_and_tree.tree_from_align(output_path)
            Canvas(geo_seqs, tree_path).create_map_and_save_to("tmp/mapa_prueba.html")
        except getopt.GetoptError:
            print('test.py file_align table_accessions')