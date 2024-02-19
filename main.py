import argparse
from src.data_collection import DataCollection

# Create the parser
parser = argparse.ArgumentParser(description='Collect data from Neurosity device.')

# Add an argument for session duration
parser.add_argument('--duration', type=int, default=30, help='Duration of the data collection session in minutes.')

parser.add_argument('--buffer', type=int, default=10, help='Duration of the data collection buffer in minutes.')

# Parse the arguments
args = parser.parse_args()

# Stream and collect data for the given duration
data_collection = DataCollection(session_duration=args.duration, session_buffer=args.buffer)
