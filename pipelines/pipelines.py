import argparse
from calendar import c
import os
import cv2
import numpy as np
import json
from skimage.metrics import structural_similarity as ssim
from graph import *
from methods import *
from filters import *
from crop import *
from usefulData import *

def pipeline_1(method, folderA, folderB, **kwargs):
    iterateThroughImages(folderA, folderB, method, **kwargs)
    updated_colourmap(method, "results.json")
    analyze_results("results.json", method)

def pipeline_2(filename, folderA, folderB, outputA, outputB):
    crop_image(filename, folderA, folderB, outputA, outputB)
    pass

def resize(x_dim, y_dim, folderA, folderB):
    if x_dim is not None and y_dim is not None:
        if not (check_image_dimensions("resizedA", x_dim, y_dim) and check_image_dimensions("resizedB", x_dim, y_dim)):
            print("Resizing images to dimensions:", x_dim, y_dim)
            block_average_png_to_json(folderA, "resizedA", x_dim, y_dim)
            block_average_png_to_json(folderB, "resizedB", x_dim, y_dim)
        else:
            print("Resized images with matching dimensions already exist.")

def filterImage(filter_name, input_folderA, input_folderB, output_folderA, output_folderB):
    filters = {
        "greyscale": greyscale,
        "colour": replaceColour
        # Add other filters here as needed
    }

    if filter_name not in filters:
        raise ValueError(f"Unknown filter: {filter_name}")

    filter_function = filters[filter_name]

    # Ensure output folders exist or create them
    for folder in [output_folderA, output_folderB]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created output folder: {folder}")

    # Apply the filter to all images in both input folders and save to the respective output folders
    for folder, output_folder in [(input_folderA, output_folderA), (input_folderB, output_folderB)]:
        for filename in os.listdir(folder):
            if filename.lower().endswith('.png'):
                input_path = os.path.join(folder, filename)
                output_path = os.path.join(output_folder, filename)

                try:
                    # Apply the filter
                    filter_function(input_path, output_path)
                    print(f"Processed and saved: {output_path}")
                except Exception as e:
                    print(f"Error processing {input_path}: {str(e)}")

def graph(method, json):
    updated_colourmap(method, "results.json")

def iterateThroughImages(folderA, folderB, method, **kwargs):
    # Define comparison techniques
    comparison_techniques = {
        "PSNR": psnr,
        "MAE": mae,
        "NCC": ncc,
        "SSIM": lambda imgA, imgB: ssim(imgA, imgB, **kwargs),
        "Histogram": histogram_intersection,
        "EMD": emd,
        "Absolute": abs_diff,
        "Correlation": correlation,
        "Bhattacharyya": bhattacharyya
    }

    results = {}

    # Load existing results if available
    results_file = "results.json"
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            results = json.load(f)
        
        # Check if any image has data for the specified method
        if any(method in image_results for image_results in results.values()):
            user_input = input(f"Results for method '{method}' already exist. Do you want to continue processing? (yes/no): ").strip().lower()
            if user_input != 'yes':
                print("Skipping processing.")
                return

    for filename in os.listdir(folderA):
        if filename.endswith(".png"):
            print(filename)

            imageA = cv2.imread(os.path.join(folderA, filename))
            imageB = cv2.imread(os.path.join(folderB, filename))
            if imageA is None or imageB is None:
                continue

            function = comparison_techniques[method]
            try:
                result = function(imageA, imageB)
            except Exception as e:
                result = str(e)

            # Ensure the filename entry exists in results
            if filename not in results:
                results[filename] = {}

            # Update the method result for this image
            results[filename][method] = result

    # Save updated results
    with open(results_file, "w") as f:
        json.dump(results, f)

    print("Results saved to results.json")

def check_image_dimensions(folder, x_dim, y_dim):
    # Check if folder exists
    if not os.path.exists(folder):
        return False

    # List all files in the directory
    files = os.listdir(folder)
    if not files:
        return False

    # Read the first PNG image
    first_image_path = os.path.join(folder, files[0])
    if not first_image_path.lower().endswith(".png"):
        return False

    # Get image dimensions
    image = cv2.imread(first_image_path)
    if image is None:
        return False

    # Check if dimensions match
    return image.shape[1] == x_dim and image.shape[0] == y_dim

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line Interface for Pipelines")
    subparsers = parser.add_subparsers(dest="pipeline")

    # Pipeline 1
    pipeline1_parser = subparsers.add_parser("pipeline1", help="Pipeline 1")
    pipeline1_parser.add_argument("method", choices=["PSNR", "MAE", "NCC", "SSIM", "Histogram", "EMD", "Absolute", "Correlation", "Bhattacharyya"], help="Method")
    pipeline1_parser.add_argument("folderA")
    pipeline1_parser.add_argument("folderB")

    resize_parser = subparsers.add_parser("resize", help="Resize")
    resize_parser.add_argument("dimensions", nargs='*', type=int, help="Dimensions (x_dim, y_dim)")
    resize_parser.add_argument("folderA")
    resize_parser.add_argument("folderB")

    # SSIM specific arguments
    pipeline1_parser.add_argument("--gaussian_weights", type=bool, default=True, help="Use Gaussian weights for SSIM")
    pipeline1_parser.add_argument("--sigma", type=float, default=1.5, help="Sigma for SSIM")

    # Pipeline 2
    pipeline2_parser = subparsers.add_parser("pipeline2", help="Pipeline 2")
    pipeline2_parser.add_argument("filename")
    pipeline2_parser.add_argument("folderA")
    pipeline2_parser.add_argument("folderB")
    pipeline2_parser.add_argument("outputA")
    pipeline2_parser.add_argument("outputB")

    # Pipeline 3
    pipeline3_parser = subparsers.add_parser("pipeline3", help="Pipeline 3")
    pipeline3_parser.add_argument("filter", choices=["greyscale", "colour"], help="Filter")
    pipeline3_parser.add_argument("input_folderA", help="Input folder A")
    pipeline3_parser.add_argument("input_folderB", help="Input folder B")
    pipeline3_parser.add_argument("output_folderA", help="Output folder A")
    pipeline3_parser.add_argument("output_folderB", help="Output folder B")

    graph_parser = subparsers.add_parser("graph", help="Graph")
    graph_parser.add_argument("method", help="json file")
    graph_parser.add_argument("json", help="json file")

    filter_parser = subparsers.add_parser("filter", help="Filter")
    filter_parser.add_argument("filter", choices=["greyscale", "colour"], help="Filter")
    filter_parser.add_argument("input_folderA", help="Input folder A")
    filter_parser.add_argument("input_folderB", help="Input folder B")
    filter_parser.add_argument("output_folderA", help="Output folder A")
    filter_parser.add_argument("output_folderB", help="Output folder B")


    args = parser.parse_args()

    if args.pipeline == "pipeline1":
        kwargs = {}
        if args.method == "SSIM":
            kwargs['gaussian_weights'] = args.gaussian_weights
            kwargs['sigma'] = args.sigma
        pipeline_1(args.method, args.folderA, args.folderB, **kwargs)
    elif args.pipeline == "pipeline2":
        pipeline_2(args.filename, args.folderA, args.folderB, args.outputA, args.outputB)
    elif args.pipeline == "pipeline3":
        filterImage(args.filter, args.input_folderA, args.input_folderB, args.output_folderA, args.output_folderB)
    elif args.pipeline == "graph":
        graph(args.method, args.json)
    elif args.pipeline == "resize":
        if args.dimensions:
            if len(args.dimensions) == 2:
                resize(args.dimensions[0], args.dimensions[1], args.folderA, args.folderB)
            else:
                print("Please provide both x_dim and y_dim.")
    elif args.pipeline == "filter":
        filterImage(args.filter, args.input_folderA, args.input_folderB, args.output_folderA, args.output_folderB)

