import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def colourmap(method, file):
    with open(file, "r") as f:
        image_comparisons_data = json.load(f)
    door_positions_data = pd.read_csv(r"C:\Users\jonat\source\repos\pipelines\pipelines\\doorA_positions.csv")

    mae_values = {image_name: data['MAE'] for image_name, data in image_comparisons_data.items()}

    # Merge MAE values with door positions
    door_positions_data[method] = door_positions_data["image"].map(mae_values)

    # Handle potential NaNs if some images in door_positions_data are not in mae_values
    door_positions_data[method].fillna(0, inplace=True)  # or some other fill value or method

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 6))

    # MAE color map
    mae_map = ax.scatter(door_positions_data["x"], door_positions_data["y"], c=door_positions_data[method], cmap='viridis')
    ax.set_title('MAE')
    fig.colorbar(mae_map, ax=ax, label='MAE')

    # Show plot
    plt.tight_layout()
    plt.show()