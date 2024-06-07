import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def colourmap(method, results_file):
    # Read image comparisons data
    with open(results_file, "r") as f:
        image_comparisons_data = json.load(f)

    # Read door positions data
    door_positions_data = pd.read_csv("C:\\Users\\jonat\\source\\repos\\doors\\doors\\doorA_positions.csv")

    # Extract the specified metric values
    metric_values = {}
    for image_name, metrics in image_comparisons_data.items():
        metric_values[image_name] = metrics[method]

    # Merge metric values with door positions
    door_positions_data[method] = door_positions_data["image"].map(metric_values)

    # Print original min and max values before normalization
    original_min_metric = door_positions_data[method].min()
    original_max_metric = door_positions_data[method].max()
    print(f"Original min {method}:", original_min_metric)
    print(f"Original max {method}:", original_max_metric)

    # Calculate the normalization factors
    metric_range = original_max_metric - original_min_metric

    # Normalize the metric values to range between 0 and 1
    door_positions_data[f"{method}_normalized"] = door_positions_data[method] / original_max_metric

    # Calculate the minimum color scale value for the color maps
    min_metric_color_value = original_min_metric / original_max_metric

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot normalized metric (0 to 1)
    normalized_map = axs[0].scatter(door_positions_data["x"], door_positions_data["y"], c=door_positions_data[f"{method}_normalized"], cmap='rainbow', norm=Normalize(vmin=0, vmax=1))
    axs[0].set_title(f'{method} (Normalized 0 to 1)')
    axs[0].set_axis_off()  # Remove x and y axes
    fig.colorbar(normalized_map, ax=axs[0], label=method)

    # Plot normalized metric (relative to minimum)
    relative_norm = Normalize(vmin=min_metric_color_value, vmax=1)
    relative_map = axs[1].scatter(door_positions_data["x"], door_positions_data["y"], c=door_positions_data[f"{method}_normalized"], cmap='rainbow', norm=relative_norm)
    axs[1].set_title(f'{method} (Relative to Min)')
    axs[1].set_axis_off()  # Remove x and y axes
    fig.colorbar(relative_map, ax=axs[1], label=method)

    plt.tight_layout()
    plt.show()