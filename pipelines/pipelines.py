import argparse
import os
import cv2
import numpy as np
import json
from skimage.metrics import structural_similarity as ssim
from graph import colourmap
from methods import *
from filters import *

def pipeline_1(method, x_dim=None, y_dim=None):
    folderA = r"C:\Users\jonat\Documents\doors\doorA"
    folderB = r"C:\Users\jonat\Documents\doors\doorB"
    
    if x_dim is not None and y_dim is not None:
        if not (check_image_dimensions("resizedA", x_dim, y_dim) and check_image_dimensions("resizedB", x_dim, y_dim)):
            print("Resizing images to dimensions:", x_dim, y_dim)
            block_average_png_to_json(folderA, "resizedA", x_dim, y_dim)
            block_average_png_to_json(folderB, "resizedB", x_dim, y_dim)
        else:
            print("Resized images with matching dimensions already exist.")
        folderA = "resizedA"
        folderB = "resizedB"

    iterateThroughImages(folderA, folderB, method)
    colourmap(method, "results.json")

def pipeline_2(area_of_interest=None, grid_resolution=None):
    pass

def apply_filter_to_images(filter_name, input_folderA, input_folderB, output_folderA, output_folderB):
    filters = {
        "greyscale": greyscale,
        # Add other filters here as needed
    }

    if filter_name not in filters:
        raise ValueError(f"Unknown filter: {filter_name}")

    filter_function = filters[filter_name]

def iterateThroughImages(folderA, folderB, method):
    comparison_techniques = {
        "PSNR": psnr,
        "MAE": mae,
        "NCC": ncc,
        "DSSIM": dssim,
        "Histogram Intersection": histogram_intersection,
        "EMD": emd,
        "Absolute Difference": abs_diff,
        "Correlation Coefficient": correlation,
        "Bhattacharyya Distance": bhattacharyya
    }    

    results = {}

    for filename in os.listdir(folderA):
        if filename.endswith(".png"):
            print(filename)
            imageA = cv2.imread(os.path.join(folderA, filename))
            imageB = cv2.imread(os.path.join(folderB, filename))
            if imageA is None or imageB is None:
                continue
            image_results = {}

            function = comparison_techniques[method]
            try:
                result = function(imageA, imageB)
                image_results[method] = result
            except Exception as e:
                image_results[method] = str(e)
            results[filename] = image_results

    with open("results.json", "w") as f:
        json.dump(results, f)

    print("Saved to results.json")

def check_image_dimensions(folder, x_dim, y_dim):
    # Check if folder exists
    if not os.path.exists(folder):
        return False

    # List all files in the directory
    files = os.listdir(folder)
    if not files:
        return False

    # Read the first PNG image
    first_image_path = os.path.join(folder, files[1])
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
    pipeline1_parser.add_argument("method", choices=["PSNR", "MAE", "NCC", "DSSIM", "Histogram Intersection", "EMD", "Absolute Difference", "Correlation Coefficient", "Bhattacharyya Distance", "RMSE"], help="Method")
    pipeline1_parser.add_argument("dimensions", nargs='*', type=int, help="Dimensions (x_dim, y_dim)")

    # Pipeline 2
    pipeline2_parser = subparsers.add_parser("pipeline2", help="Pipeline 2")
    group = pipeline2_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--area-of-interest", help="Area of interest")
    group.add_argument("--grid-resolution", help="Grid resolution")

    filter_parser = subparsers.add_parser("filter", help="Apply a filter to images in two folders")
    filter_parser.add_argument("filter_name", choices=["greyscale"], help="Filter to apply")
    filter_parser.add_argument("input_folderA", help="First input folder")
    filter_parser.add_argument("input_folderB", help="Second input folder")
    filter_parser.add_argument("output_folderA", help="First output folder")
    filter_parser.add_argument("output_folderB", help="Second output folder")

    args = parser.parse_args()

    if args.pipeline == "pipeline1":
        if len(args.dimensions) == 2:
            pipeline_1(args.method, args.dimensions[0], args.dimensions[1])
        elif len(args.dimensions) == 0:
            pipeline_1(args.method)
        else:
            print("Please provide both x_dim and y_dim or leave them out completely.")
    elif args.pipeline == "pipeline2":
        pipeline_2(args.area_of_interest, args.grid_resolution)
