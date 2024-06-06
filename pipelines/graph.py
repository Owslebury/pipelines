import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def open():
    with open(r"C:\Users\jonat\source\repos\pipelines\pipelines\results.json", "r") as f:
        image_comparisons_data = json.load(f)
    door_positions_data = pd.read_csv(r"C:\Users\jonat\source\repos\pipelines\pipelinesdoorA_positions.csv")

    