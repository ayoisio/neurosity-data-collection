import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dotenv import load_dotenv
from neurosity import NeurositySDK
from pathlib import Path


class DataCollection:

    def __init__(self, session_duration: int = 30, session_buffer: int = 5, verbose: bool = True):
        """
        Initialize.

        Args:
            session_duration (int): Duration of session in minutes.
            session_buffer (int): End buffer time in minutes.
            verbose (bool): Verbosity
        """
        load_dotenv()

        # Configure user and device
        self.device_id = self.prompt_for_env_var("NEUROSITY_DEVICE_ID")
        self.email = self.prompt_for_env_var("NEUROSITY_EMAIL")
        self.password = self.prompt_for_env_var("NEUROSITY_PASSWORD")

        # Configure session duration and buffer
        self.session_duration = session_duration
        self.session_buffer = session_buffer

        # Configure output directory
        self.output_session_dir = self.prompt_for_env_var("OUTPUT_SESSION_DIR")
        self.session_dir = Path(self.output_session_dir) / "session_{}".format(time.strftime("%Y%m%d-%H%M%S"))
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Login to Neurosity SDK
        self.neurosity = None
        self.login_neurosity()

        # Verbose
        if verbose:
            self.print_session_details()
        self.verbose = verbose

        # Subscribe to metrics
        self.subscribe_to_metrics()

    def prompt_for_env_var(self, var_name: str, units: str = ''):
        """
        Prompt for env var.

        Use Case: Prompt for missing environment variables.
        """
        value = os.getenv(var_name)
        if not value:
            value = input(f"Enter your Neurosity {var_name.lower().replace('_', ' ')}{units}: ")
            os.environ[var_name] = value
        return value

    def login_neurosity(self):
        """Login to Neurosity SDK."""
        self.neurosity = NeurositySDK({
            "device_id": self.device_id,
        })

        try:
            self.neurosity.login({
                "email": self.email,
                "password": self.password,
            })
        except Exception as e:
            if "EMAIL_NOT_FOUND" in str(e):
                raise ValueError("The provided email does not exist. Please check and try again.")
            elif "INVALID_PASSWORD" in str(e):
                raise ValueError("The provided password is invalid. Please check and try again.")
            else:
                raise Exception("An error occurred. Please confirm that the provided email and password are correct.")

    def create_callback(self, metric_name):
        """
        Create callback.

        Use Case: Callback template to save data to a specified metric file
        """
        def callback(data):
            # output data
            output_data = {
                'collected': data,
                'collected_timestamp': datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")
            }
            file_path = self.session_dir / f"{metric_name}.txt"
            with open(file_path, "a") as file:
                file.write(json.dumps(output_data) + "\n")

        return callback

    def subscribe_to_metric(self, metric):
        """Function to handle metric subscription in a thread."""
        non_brain_wave_metrics = ["signal_quality", "accelerometer", "calm", "focus"]
        method_name = f"brainwaves_{metric}" if metric not in non_brain_wave_metrics else metric
        if hasattr(self.neurosity, method_name):
            callback = self.create_callback(metric)
            unsubscribe = getattr(self.neurosity, method_name)(callback)

            # Keep streaming for the session duration
            time.sleep(60 * (self.session_duration + self.session_buffer))
            unsubscribe()

    def subscribe_to_metrics(self):
        metrics = [
            "raw",
            "raw_unfiltered",
            "psd",
            "power_by_band",
            "signal_quality",
            "accelerometer",
            "calm",
            "focus"
        ]

        if self.verbose:
            print(f"Data streaming has started and will stop in {self.session_duration} mins.")
            print("Use Ctrl+C to stop manually.")

        with ThreadPoolExecutor() as executor:
            # Launch a thread for each metric subscription
            futures = {executor.submit(self.subscribe_to_metric, metric): metric for metric in metrics}
            for future in as_completed(futures):
                metric = futures[future]
                try:
                    future.result()  # Wait for thread completion and catch exceptions
                except Exception as exc:
                    print(f"{metric} generated an exception: {exc}")

    def print_session_details(self):
        """Print session details."""
        print('Step 1. Configure User and Device:')
        print('-----------------------')
        print('Email:', self.email)
        print('Device ID:', self.device_id)
        print('Password:', ''.join((len(self.password) * ['*'])))
        print()
        print('Step 2. Configure Session Duration (mins):')
        print('-----------------------')
        print('Session Duration (mins):', self.session_duration)
        print()
        print('Step 3. Configure Output Directory:')
        print('-----------------------')
        print('Output Session Directory:', self.output_session_dir)
        print()
        print('Step 4. Login to Neurosity:')
        print('-----------------------')
        print('Successfully logged in ✔')
        print()
