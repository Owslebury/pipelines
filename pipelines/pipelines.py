
import argparse
import os
import cv2
import numpy as np
import json
from skimage.metrics import structural_similarity as ssim
from methods import *

def pipeline_1(method, x_dim, y_dim):
    print("foghreoig")
    if method == "PSNR":
        pass
    elif method == "MAE":
        pass
    elif method == "NCC":
        pass
    elif method == "DSSIM":
        pass
    elif method == "Histogram Intersection":
        pass
    elif method == "EMD":
        pass
    elif method == "Absolute Difference":
        pass
    elif method == "Correlation Coefficient":
        pass
    elif method == "Bhattacharyya Distance":
        pass
    elif method == "RMSE":
        pass

def pipeline_2(area_of_interest=None, grid_resolution=None):
    pass

def iterateThroughImages(method):

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

    # Path to the directories containing the images
    folderA = r"C:\Users\jonat\Documents\doors\doorA"
    folderB = r"C:\Users\jonat\Documents\doors\doorB"

    # Initialize dictionary to store results
    results = {}

    for filename in os.listdir(folderA):
        print(filename)
        if filename.endswith(".png"):
            imageA = cv2.imread(os.path.join(folderA, filename))
            imageB = cv2.imread(os.path.join(folderB, filename))
            if imageA is None or imageB is None:
                continue
            image_results = {}
            for technique, function in comparison_techniques.items():
                try:
                    result = function(imageA, imageB)
                    image_results[technique] = result
                except Exception as e:
                    image_results[technique] = str(e)
            results[filename] = image_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line Interface for Pipelines")

    subparsers = parser.add_subparsers(dest="pipeline")

    # Pipeline 1
    pipeline1_parser = subparsers.add_parser("pipeline1", help="Pipeline 1")
    pipeline1_parser.add_argument("method", choices=["PSNR", "MAE", "NCC", "DSSIM", "Histogram Intersection", "EMD", "Absolute Difference", "Correlation Coefficient", "Bhattacharyya Distance", "RMSE"], help="Method")
    pipeline1_parser.add_argument("x_dim", type=int, help="X dimension")
    pipeline1_parser.add_argument("y_dim", type=int, help="Y dimension")

    # Pipeline 2
    pipeline2_parser = subparsers.add_parser("pipeline2", help="Pipeline 2")
    group = pipeline2_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--area-of-interest", help="Area of interest")
    group.add_argument("--grid-resolution", help="Grid resolution")

    args = parser.parse_args()

    if args.pipeline == "pipeline1":
        pipeline_1(args.method, args.x_dim, args.y_dim)
    elif args.pipeline == "pipeline2":
        pipeline_2(args.area_of_interest, args.grid_resolution)
