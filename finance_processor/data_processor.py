import pandas as pd
import plotly.graph_objects as go
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinanceDataProcessor:
    def __init__(self, stock_name: str, file_path: str) -> None:
        self.stock_name = stock_name
        self.file_path = file_path
        self.raw_data = None
        self._load_data()
        self._add_day_of_week()

    def _load_data(self) -> None:
        # Load CSV containing OHLC prices and volume for a stock, also parse dates
        try:
            self.raw_data = pd.read_csv(self.file_path)
            self.raw_data["Date"] = pd.to_datetime(self.raw_data["Date"])
            logging.info("Data loaded successfully.")
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            raise
        except pd.errors.ParserError:
            logging.error(f"Error parsing the file: {self.file_path}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error loading data: {e}")
            raise

    def _add_day_of_week(self):
        self.raw_data["Day Of Week"] = self.raw_data["Date"].dt.day_name()

    def save_with_weekdays(self, output_file: str) -> None:
        self.raw_data.set_index("Date").to_csv(output_file)
        logging.info(f"Data with weekdays saved to {output_file}")

    def get_max(self) -> float:
        return self.raw_data[f"{self.stock_name}.High"].max()

    def get_min(self) -> float:
        return self.raw_data[f"{self.stock_name}.Low"].min()

    def get_average(self) -> float:
        return self.raw_data[f"{self.stock_name}.Close"].mean()

    def validate(self) -> float:
        # Validate monotonicity for dates and ensure there are no duplicates
        try:
            assert len(self.raw_data) == len(self.raw_data["Date"].unique()), "Dataset contains duplicates"
            for idx, row in self.raw_data[1:].iterrows():
                assert self.raw_data[0:idx]["Date"].max() < row["Date"], f"Entry for {row['Date']} is out of order!"
            logging.info("Data validation passed.")
        except AssertionError as e:
            logging.error(f"Data validation error: {e}")
            raise

    def get_average_volume(self) -> float:
        return self.raw_data[f"{self.stock_name}.Volume"].mean()

    def remove_low_volume_and_save(self, filename: str) -> pd.DataFrame:
        # Filter out data with trading volume below the average, save output to CSV
        above_avg_volume = self.raw_data[self.raw_data[f"{self.stock_name}.Volume"] >= self.get_average_volume()]
        above_avg_volume.set_index("Date").to_csv(filename)
        logging.info(f"Data with above average volume saved to {filename}")
        return above_avg_volume

    def generate_week_level(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
        # Transform daily stock data into week-level stock data, save it to a CSV file
        week_level = df.resample('W', on='Date').agg({
            f"{self.stock_name}.Open": "first",
            f"{self.stock_name}.High": "max",
            f"{self.stock_name}.Low": "min",
            f"{self.stock_name}.Close": "last",
            f"{self.stock_name}.Volume": "sum",
            f"{self.stock_name}.Adjusted": "last",
            "dn": "min",
            "mavg": "mean",
            "up": "max"
        })

        # Re-calculates direction to compare weekly closing prices versus daily values
        # This determines direction by comparing weekly closing prices to those of the previous week
        # A formula for the original day-to-day direction field was not provided
        week_level["direction"] = "No Change"
        week_iter = week_level.iterrows()
        last_index = next(week_iter)[0]
        for idx, this_week in week_iter:
            last_week = week_level.loc[last_index]
            if last_week[f"{self.stock_name}.Close"] < this_week[f"{self.stock_name}.Close"]:
                week_level.at[idx, "direction"] = "Increasing"
            elif last_week[f"{self.stock_name}.Close"] > this_week[f"{self.stock_name}.Close"]:
                week_level.at[idx, "direction"] = "Decreasing"
            else:
                # Copy values from the previous week if there's no change, otherwise they'll appear as blanks
                for column in week_level.columns:
                    if column != "direction":
                        week_level.at[idx, column] = last_week[column]

            last_index = idx

        week_level["Day Of Week"] = week_level.index.day_name()
        week_level.to_csv(filename)
        logging.info(f"Week-level data saved to {filename}")
        return week_level

    def generate_candlestick_graph(self, df: pd.DataFrame, filename: str) -> None:
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df[f"{self.stock_name}.Open"],
                                             high=df[f"{self.stock_name}.High"],
                                             low=df[f"{self.stock_name}.Low"],
                                             close=df[f"{self.stock_name}.Close"])])
        fig.write_image(filename)
        logging.info(f"Candlestick graph saved to {filename}")
