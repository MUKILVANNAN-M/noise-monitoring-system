import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

NOISE_THRESHOLD_DB = 85

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_date_input(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), "%Y-%m-%d").date()
        except ValueError:
            print("Invalid input. Please use YYYY-MM-DD format.")

def collect_noise_data(start_date, end_date):
    data = []
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')

        while True:
            avg_noise = get_float_input(f"Enter average noise level for {date_str} (dB): ")
            max_noise = get_float_input(f"Enter highest noise level for {date_str} (dB): ")

            if max_noise >= avg_noise:
                break
            else:
                print("Highest noise must be >= average noise.")

        data.append({
            "date": date_str,
            "average_noise": avg_noise,
            "highest_noise": max_noise
        })

        current_date += timedelta(days=1)

    return pd.DataFrame(data)

def plot_data(df, location, start_date, end_date, overall_avg):
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['highest_noise'], label="Highest Noise", marker='o')
    plt.plot(df['date'], df['average_noise'], label="Average Noise", marker='x')

    plt.axhline(overall_avg, linestyle='--', label=f"Avg: {overall_avg:.2f} dB")
    plt.axhline(NOISE_THRESHOLD_DB, linestyle='--', label="Threshold (85 dB)")

    plt.title(f"Noise Levels - {location}")
    plt.xlabel("Date")
    plt.ylabel("Noise (dB)")
    plt.legend()
    plt.grid()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    print("📊 Noise Monitoring System")

    location = input("Enter location: ")
    start_date = get_date_input("Start date (YYYY-MM-DD): ")
    end_date = get_date_input("End date (YYYY-MM-DD): ")

    if end_date < start_date:
        print("End date must be after start date")
        return

    df = collect_noise_data(start_date, end_date)

    overall_avg = df["average_noise"].mean()

    payload = {
        "location": location,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "average_noise": overall_avg,
        "timestamp": time.time()
    }

    print("\nGenerated Data Payload:")
    print(payload)

    plot_data(df, location, start_date, end_date, overall_avg)

if __name__ == "__main__":
    main()
