import matplotlib.pyplot as plt
import pandas as pd

def generate_bar_chart(data, x_key, y_key, output_path="chart.png"):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_key], pd.to_numeric(df[y_key].str.replace("$", "").str.replace("M", "e6").str.replace("B", "e9")))
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.title(f"{y_key} by {x_key}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    return output_path
