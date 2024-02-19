# neurosity-data-collection

A Python package that facilitates the collection of brainwave data using the Neurosity hardware. Follow the instructions below to set up your environment and start collecting data.

## Prerequisites
Before you begin, ensure you have the following:
* Python 3.7+ installed on your system
* Access to a Neurosity device and your Neurosity account credentials

## Instructions
### 1. Clone the repository
First, clone the Neurosity Data Collection repository to your local machine using Git:

```
git clone https://github.com/ayoisio/neurosity-data-collection.git
cd neurosity-data-collection
```

### 2. Create a virtual environment (optional but recommended)
To create a virtual environment, run:

```
python -m venv venv
```

To activate the virtual environment:
* On Windows, run: venv\Scripts\activate
* On macOS and Linux, run: source venv/bin/activate

### 3. Install dependencies
Install the required Python packages using __pip__:

```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Fill in your Neurosity account details in the __.env__ file and desired output session directory.

```
NEUROSITY_EMAIL=your_email@example.com
NEUROSITY_PASSWORD=your_password
NEUROSITY_DEVICE_ID=your_device_id
OUTPUT_SESSION_DIR=./output
```

### 5. Running the Data Collection

To start the data collection process, ensure that your Neurosity device is connected and ready to stream data. You can specify the duration of the data collection session (in minutes) as a command-line argument:

```
python main.py --duration 30
```

Replace 30 with the number of minutes you want to collect data for. If you do not specify a duration, it will default to 30 minutes.

### 6. Stopping the Data Collection
The data collection will run for the duration specified by the --duration command-line argument. If you wish to stop the collection manually, use Ctrl+C in the terminal.

### 7. Output
The collected data will be saved in the specified output directory, with each metric stored in a separate .txt file formatted as JSON Lines. Each file will be timestamped and contain the data streamed from your Neurosity device for the duration of the session.
