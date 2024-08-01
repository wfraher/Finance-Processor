from finance_processor import FinanceDataProcessor

# Starts file processor, feeds in Apple stock data
file_path = "data/finance-charts-apple.csv"
processor = FinanceDataProcessor("AAPL", file_path)

# Validates the data
processor.validate()

# Generates week-level data
processor.save_with_weekdays("outputs/original_with_weekdays.csv")

# Determines dataset metrics
print(f"Max value: {processor.get_max()}")
print(f"Min value: {processor.get_min()}")
print(f"Average value: {processor.get_average()}")
print(f"Average volume: {processor.get_average_volume()}")

# Removes low-volume trading days, saves to CSV
higher_volume = processor.remove_low_volume_and_save("outputs/above_average_volume.csv")

# Calculates week-level trading data
original_week_level = processor.generate_week_level(processor.raw_data, "outputs/original_week_level.csv")
higher_volume_week_level = processor.generate_week_level(higher_volume, "outputs/higher_volume_week_level.csv")

# Generates and saves candlestick graphs
processor.generate_candlestick_graph(original_week_level, "graphs/original_week_level_candlestick.jpg")
processor.generate_candlestick_graph(higher_volume_week_level, "graphs/higher_volume_week_level_candlestick.jpg")
