import requests
import matplotlib.pyplot as plt
import pandas as pd

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {"latitude": 55.75, "longitude": 37.61, "hourly": "temperature_2m"}
TIMEOUT = 10


def build_dataframe(hours, temps):
    df = pd.DataFrame({"time": pd.to_datetime(hours), "temperature_c": temps})
    df = df.sort_values("time").reset_index(drop=True)
    return df


def fetch_temperature():
    response = requests.get(URL, params=PARAMS, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    hours = data["hourly"]["time"][:24]
    temps = data["hourly"]["temperature_2m"][:24]
    return build_dataframe(hours, temps)


def save_plot(df, path="temperature_24h.png"):
    plt.figure()
    plt.plot(df["time"], df["temperature_c"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Температура в Москве (24 часа)")
    plt.xlabel("Время")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main():
    df = fetch_temperature()
    df.to_csv("temperature_24h.csv", index=False)
    print("Сохранено в temperature_24h.csv")
    save_plot(df)
    print("Сохранено в temperature_24h.png")


if __name__ == "__main__":
    main()