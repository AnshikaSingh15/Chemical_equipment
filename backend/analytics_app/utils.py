import pandas as pd

def analyze_csv(file):
    df = pd.read_csv(file)

    summary = {
        "total_count": len(df),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    return summary
