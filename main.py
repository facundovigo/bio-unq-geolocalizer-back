from src.geolocalizer.logger import Logger
from src.geolocalizer.parser import Parser
from src.geolocalizer.geo_services import GeoServices
from src.geolocalizer.align_and_tree import AlignAndTree
from src.geolocalizer.canvas import Canvas
import sys, getopt


if __name__ == "__main__":
    email = ""
    if not email:
        raise Exception("Set Entrez email")

    logger = Logger("tmp/logfile.txt")
    if (sys.argv[1].__str__ == "h") | (len(sys.argv) != 2):
        print("case of use:   test.py file_align")
    else:
        try:
            logger.log("Parser", "Parsing input file...")
            parsed_fasta = Parser(logger).parse(
                f"src/files/{sys.argv[1]}", write_output=True
            )
            logger.log("Parser", "Done")

            logger.log('GeoServices', "Geolocalizing sequences...")
            geo_seqs = GeoServices(email, logger).geolocalize_seqs(parsed_fasta["seqs"])
            logger.log('GeoServices', "Done")


            align_and_tree = AlignAndTree(logger)
            logger.log('AlignAndTree', "Aligning fasta file...")
            output_path = align_and_tree.align_fasta(parsed_fasta["output_path"])
            logger.log('AlignAndTree', "Done")

            logger.log('AlignAndTree', "Generating phylogenetic tree...")
            tree_path = align_and_tree.tree_from_align(output_path)
            logger.log('AlignAndTree', "Done")

            logger.log("Canvas", "Creating map...")
            Canvas(geo_seqs, tree_path, logger).create_map_and_save_to(
                "tmp/mapa_prueba.html"
            )
            logger.log("Canvas", "Done")
        except getopt.GetoptError:
            print("test.py file_align table_accessions")
