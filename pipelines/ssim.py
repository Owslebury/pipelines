import os
import argparse
from skimage import io
from skimage.metrics import structural_similarity as ssim
import json

def compute_ssim(img1, img2, gaussian_weights=True, sigma=1.5):
    # Convert images to grayscale
    gray1 = io.imread(img1, as_gray=True)
    gray2 = io.imread(img2, as_gray=True)
    # Compute SSIM
    score = ssim(gray1, gray2, data_range=gray2.max() - gray2.min(), gaussian_weights=gaussian_weights, sigma=sigma)
    return score

def process_images(directory1, directory2, gaussian_weights=True, sigma=1.5):
    ssim_dict = {}
    for filename in os.listdir(directory1):
        if filename.endswith(".png"):
            print(filename)
            ssim_score = compute_ssim(os.path.join(directory1, filename), os.path.join(directory2, filename), gaussian_weights=gaussian_weights, sigma=sigma)
        print(filename)
        # Store SSIM score in dictionary
        ssim_dict[filename] = ssim_score
    return ssim_dict

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Compute SSIM between images in two directories')
    parser.add_argument('directory1', help='Path to the first directory containing images')
    parser.add_argument('directory2', help='Path to the second directory containing images')
    parser.add_argument('--gaussian', action='store_true', help='Whether to use Gaussian weights (default: True)')
    parser.add_argument('--sigma', type=float, default=1.5, help='Value for sigma (default: 1.5)')
    args = parser.parse_args()

    ssim_dict = process_images(args.directory1, args.directory2, gaussian_weights=args.gaussian, sigma=args.sigma)
    save_to_json(ssim_dict, "ssim_results.json")

if __name__ == "__main__":
    main()
