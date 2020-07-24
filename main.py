from src.geolocalizer.logger import Logger
from src.geolocalizer.parser import Parser
from src.geolocalizer.geo_services import GeoServices
from src.geolocalizer.align_and_tree import AlignAndTree
from src.geolocalizer.canvas import Canvas
import sys, getopt, json, argparse


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--fasta", help="FASTA file path")
    argument_parser.add_argument(
        "--config", help="JSON config file path", default="config.json"
    )
    argument_parser.add_argument(
        "--map-output", help="Output path for map", default="tmp/map.html"
    )
    args = argument_parser.parse_args()

    with open(args.config) as config:
        parsed_config = json.load(config)

    email = parsed_config.get("email")
    if not email:
        print("Set Entrez email in the config.json")
        exit(2)
    logger = Logger("tmp/logfile.txt")

    logger.log("Parser", "Parsing input file...")
    parsed_fasta = Parser(logger).parse(args.fasta, write_output=True)
    logger.log("Parser", "Done")

    logger.log("GeoServices", "Geolocalizing sequences...")
    geo_seqs = GeoServices(email, logger).geolocalize_seqs(parsed_fasta["seqs"])
    logger.log("GeoServices", "Done")

    align_and_tree = AlignAndTree(logger)
    logger.log("AlignAndTree", "Aligning fasta file...")
    output_path = align_and_tree.align_fasta(
        parsed_fasta["output_path"], parsed_config.get("clustal").get("threads")
    )
    logger.log("AlignAndTree", "Done")

    logger.log("AlignAndTree", "Generating phylogenetic tree...")
    tree_path = align_and_tree.tree_from_align(
        output_path,
        parsed_config.get("iqtree").get("bootstrap"),
        parsed_config.get("iqtree").get("model_finder"),
    )

    logger.log("AlignAndTree", "Done")

    logger.log("Canvas", "Creating map...")
    Canvas(geo_seqs, tree_path, logger).create_map_and_save_to(args.map_output)
    logger.log("Canvas", "Done")
