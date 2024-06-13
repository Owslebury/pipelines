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

def pipeline_1(method, x_dim=None, y_dim=None, **kwargs):
    folderA = r"C:\Users\jonat\Documents\doors\doorB"
    folderB = r"C:\Users\jonat\Documents\doors\doorA"


    if x_dim is not None and y_dim is not None:
        if not (check_image_dimensions("resizedA", x_dim, y_dim) and check_image_dimensions("resizedB", x_dim, y_dim)):
            print("Resizing images to dimensions:", x_dim, y_dim)
            block_average_png_to_json(folderA, "resizedA", x_dim, y_dim)
            block_average_png_to_json(folderB, "resizedB", x_dim, y_dim)
        else:
            print("Resized images with matching dimensions already exist.")
        folderA = "resizedA"
        folderB = "resizedB"

    iterateThroughImages(folderA, folderB, method, **kwargs)
    updated_colourmap(method, "results.json")

def pipeline_2(filename=None):
    crop_image(filename)
    pass

def filterImage(filter_name, input_folderA, input_folderB, output_folderA, output_folderB):
    filters = {
        "greyscale": greyscale,
        "colour": replaceColour
        # Add other filters here as needed
    }


    if filter_name not in filters:
        raise ValueError(f"Unknown filter: {filter_name}")

    filter_function = filters[filter_name]

    # Apply the filter to all images in both input folders and save to the respective output folders
    for folder, output_folder in [(input_folderA, output_folderA), (input_folderB, output_folderB)]:
        for filename in os.listdir(folder):
            if filename.lower().endswith('.png'):
                input_path = os.path.join(folder, filename)
                output_path = os.path.join(output_folder, filename)

                # Read the image
                image = cv2.imread(input_path)
                if image is None:
                    continue

                # Apply the filter
                filter_function(image, output_folderA)
                filter_function(image, output_folderB)
                # Save the filtered image
                #cv2.imwrite(output_path, filtered_image)
                #print(f"Processed and saved: {output_path}")

def graph(json):
    colourmap(None, "results.json")

def iterateThroughImages(folderA, folderB, method, **kwargs):
    comparison_techniques = {
        "PSNR": psnr,
        "MAE": mae,
        "NCC": ncc,
        "SSIM": lambda imgA, imgB: ssim(imgA, imgB, **kwargs),
        "Histogram": histogram_intersection,
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
    pipeline1_parser.add_argument("method", choices=["PSNR", "MAE", "NCC", "SSIM", "Histogram", "EMD", "Absolute Difference", "Correlation Coefficient", "Bhattacharyya Distance"], help="Method")
    pipeline1_parser.add_argument("dimensions", nargs='*', type=int, help="Dimensions (x_dim, y_dim)")

    # SSIM specific arguments
    pipeline1_parser.add_argument("--gaussian_weights", type=bool, default=True, help="Use Gaussian weights for SSIM")
    pipeline1_parser.add_argument("--sigma", type=float, default=1.5, help="Sigma for SSIM")

    # Pipeline 2
    pipeline2_parser = subparsers.add_parser("pipeline2", help="Pipeline 2")
    pipeline2_parser.add_argument("filename")

    # Pipeline 3
    pipeline3_parser = subparsers.add_parser("pipeline3", help="Pipeline 3")
    pipeline3_parser.add_argument("filter", choices=["greyscale", "colour"], help="Filter")
    pipeline3_parser.add_argument("input_folderA", help="Input folder A")
    pipeline3_parser.add_argument("input_folderB", help="Input folder B")
    pipeline3_parser.add_argument("output_folderA", help="Output folder A")
    pipeline3_parser.add_argument("output_folderB", help="Output folder B")

    graph_parser = subparsers.add_parser("graph", help="Graph")
    graph_parser.add_argument("json", help="json file")


    args = parser.parse_args()

    if args.pipeline == "pipeline1":
        kwargs = {}
        if args.method == "SSIM":
            kwargs['gaussian_weights'] = args.gaussian_weights
            kwargs['sigma'] = args.sigma

        if args.dimensions:
            if len(args.dimensions) == 2:
                pipeline_1(args.method, args.dimensions[0], args.dimensions[1], **kwargs)
            else:
                print("Please provide both x_dim and y_dim.")
        else:
            pipeline_1(args.method)
    elif args.pipeline == "pipeline2":
        pipeline_2(args.filename)
    elif args.pipeline == "pipeline3":
        filterImage(args.filter, args.input_folderA, args.input_folderB, args.output_folderA, args.output_folderB)
    elif args.pipeline == "graph":
        graph(args.json)
