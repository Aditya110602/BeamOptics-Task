Data Viewer and Predictor GUI App
This is a Python desktop application with a Graphical User Interface (GUI) designed to load, display, and perform a simple prediction on a given dataset.

Features
Load Data: Load a CSV file (data.csv) into the application.

Display Data: View the contents of the loaded dataset in a scrollable text area.

Predict: Compute a predefined prediction based on the sensor_value column.

If the average sensor_value is above 50, the prediction is: "Prediction: System requires calibration".

Otherwise, the prediction is: "Prediction: System functioning normally".

Log/Output Area: Provides real-time status updates and messages.

Refresh Data: Reloads the dataset without restarting the application.

Sensor Value Plot: Displays a plot of sensor_value over time using matplotlib.

Responsive GUI: The application remains responsive during data loading and prediction operations, thanks to threading.

Setup and Run Instructions
Follow these steps to set up and run the application:

1. Prerequisites
Python 3.x installed on your system.

2. Prepare the Files
Save the provided Python code as task.py.

Save the requirements.txt content into a file named requirements.txt in the same directory as task.py.

Ensure the data.csv file is placed in the same directory as task.py.

3. Install Dependencies
Open your terminal or command prompt, navigate to the directory where you saved the files, and install the required Python libraries using pip:

pip install -r requirements.txt

4. Run the Application
After installing the dependencies, run the application from your terminal:

python task.py

5. Using the Application
Load Data: Click the "Load Data" button. The application will automatically attempt to load data.csv from the same directory.

View Data: Once loaded, the dataset will appear in the "Loaded Data" display area.

Predict: Click the "Predict" button to see the prediction result displayed above the data area.

Refresh: Click the "Refresh" button to reload the data.csv file and update the display and plot.

Log: Monitor the "Log/Output" area for status messages and any errors.

Plot: Observe the "Sensor Value Over Time" plot, which updates automatically upon data load/refresh.

Code Structure
The application is structured using a DataViewerApp class, which encapsulates all the GUI elements and logic:

__init__: Initializes the main window and calls methods to create widgets.

_create_widgets: Sets up all the Tkinter widgets (buttons, labels, text areas, plot).

_log_message: A helper function to add messages to the log display.

_load_data_threaded: Initiates data loading in a separate thread to keep the GUI responsive.

_load_data: Reads the data.csv using pandas and updates the GUI.

_display_data: Formats and displays the DataFrame content.

_predict_threaded: Initiates prediction in a separate thread.

_perform_prediction: Implements the core prediction logic.

_refresh_data_threaded: Initiates data refresh in a separate thread.

_plot_data: Generates and updates the matplotlib plot.

The use of threading ensures that heavy operations like file I/O and computations do not freeze the user interface, providing a smooth user experience.