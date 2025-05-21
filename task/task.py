import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Viewer and Predictor")
        self.root.geometry("1000x800")

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.data = None

        self._create_widgets()

    def _create_widgets(self):
        button_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        button_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        self.load_button = tk.Button(button_frame, text="Load Data", command=self._load_data_threaded,
                                     font=("Inter", 10, "bold"), bg="#4CAF50", fg="white",
                                     relief="raised", bd=3, padx=10, pady=5, cursor="hand2")
        self.load_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.predict_button = tk.Button(button_frame, text="Predict", command=self._predict_threaded,
                                        font=("Inter", 10, "bold"), bg="#2196F3", fg="white",
                                        relief="raised", bd=3, padx=10, pady=5, cursor="hand2")
        self.predict_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.predict_button.config(state=tk.DISABLED)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self._refresh_data_threaded,
                                        font=("Inter", 10, "bold"), bg="#FFC107", fg="black",
                                        relief="raised", bd=3, padx=10, pady=5, cursor="hand2")
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.refresh_button.config(state=tk.DISABLED)

        self.prediction_label = tk.Label(self.root, text="Prediction: N/A",
                                         font=("Inter", 12, "bold"), fg="#333", bg="#f0f0f0",
                                         padx=10, pady=10, relief="sunken", bd=1)
        self.prediction_label.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        data_label = tk.Label(self.root, text="Loaded Data:", font=("Inter", 10, "bold"))
        data_label.grid(row=2, column=0, padx=10, sticky="nw")

        self.data_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20,
                                                      font=("Courier New", 9), bg="#f8f8f8", fg="#333",
                                                      relief="sunken", bd=1, padx=5, pady=5)
        self.data_display.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(3, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.ax.set_title("Sensor Value Over Time")
        self.ax.set_xlabel("Timestamp")
        self.ax.set_ylabel("Sensor Value")
        self.ax.grid(True)
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(4, weight=1)

        log_label = tk.Label(self.root, text="Log/Output:", font=("Inter", 10, "bold"))
        log_label.grid(row=5, column=0, padx=10, sticky="nw")

        self.log_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=8,
                                                     font=("Inter", 9), bg="#e0e0e0", fg="#333",
                                                     relief="sunken", bd=1, padx=5, pady=5)
        self.log_display.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(6, weight=0)

        self._log_message("Application started. Please load a CSV file.")

    def _log_message(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)

    def _load_data_threaded(self):
        self._log_message("Attempting to load data...")
        self.load_button.config(state=tk.DISABLED)
        self.predict_button.config(state=tk.DISABLED)
        self.refresh_button.config(state=tk.DISABLED)
        threading.Thread(target=self._load_data).start()

    def _load_data(self):
        try:
            file_path = "./data.csv"
            self._log_message(f"Loading data from: {file_path}")

            self.data = pd.read_csv(file_path)

            self.root.after(0, self._display_data)
            self.root.after(0, lambda: self._log_message("Data loaded successfully."))
            self.root.after(0, lambda: self.predict_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.refresh_button.config(state=tk.NORMAL))

            self.root.after(0, self._plot_data)

        except FileNotFoundError:
            self.root.after(0, lambda: messagebox.showerror("Error", f"File not found: {file_path}"))
            self.root.after(0, lambda: self._log_message(f"Error: File not found at {file_path}"))
        except pd.errors.EmptyDataError:
            self.root.after(0, lambda: messagebox.showerror("Error", "The CSV file is empty."))
            self.root.after(0, lambda: self._log_message("Error: CSV file is empty."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            self.root.after(0, lambda: self._log_message(f"Error loading data: {e}"))
        finally:
            self.root.after(0, lambda: self.load_button.config(state=tk.NORMAL))


    def _display_data(self):
        if self.data is not None:
            self.data_display.delete(1.0, tk.END)
            self.data_display.insert(tk.END, self.data.to_string(index=False))
        else:
            self.data_display.delete(1.0, tk.END)
            self.data_display.insert(tk.END, "No data loaded yet.")

    def _predict_threaded(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load data first before predicting.")
            self._log_message("Prediction failed: No data loaded.")
            return

        self._log_message("Computing prediction...")
        self.predict_button.config(state=tk.DISABLED)
        threading.Thread(target=self._perform_prediction).start()

    def _perform_prediction(self):
        try:
            if 'sensor_value' not in self.data.columns:
                self.root.after(0, lambda: messagebox.showerror("Error", "Column 'sensor_value' not found in data."))
                self.root.after(0, lambda: self._log_message("Prediction failed: 'sensor_value' column missing."))
                return

            avg_sensor_value = self.data['sensor_value'].mean()
            self._log_message(f"Average sensor_value: {avg_sensor_value:.2f}")

            if avg_sensor_value > 50:
                prediction_result = "Prediction: System requires calibration"
            else:
                prediction_result = "Prediction: System functioning normally"

            self.root.after(0, lambda: self.prediction_label.config(text=prediction_result))
            self.root.after(0, lambda: self._log_message("Prediction complete."))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred during prediction: {e}"))
            self.root.after(0, lambda: self._log_message(f"Error during prediction: {e}"))
        finally:
            self.root.after(0, lambda: self.predict_button.config(state=tk.NORMAL))

    def _refresh_data_threaded(self):
        self._log_message("Refreshing data...")
        self.refresh_button.config(state=tk.DISABLED)
        self.predict_button.config(state=tk.DISABLED)
        threading.Thread(target=self._load_data).start()

    def _plot_data(self):
        self.ax.clear()

        if self.data is not None and 'timestamp' in self.data.columns and 'sensor_value' in self.data.columns:
            try:
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
                self.ax.plot(self.data['timestamp'], self.data['sensor_value'], marker='o', linestyle='-', color='skyblue')
                self.ax.set_title("Sensor Value Over Time")
                self.ax.set_xlabel("Timestamp")
                self.ax.set_ylabel("Sensor Value")
                self.ax.tick_params(axis='x', rotation=45)
                self.ax.grid(True)
                self.fig.tight_layout()
                self.canvas.draw()
                self._log_message("Plot updated successfully.")
            except Exception as e:
                self._log_message(f"Error plotting data: {e}")
                self.ax.set_title("Error: Could not plot data")
                self.canvas.draw()
        else:
            self.ax.set_title("No data or required columns for plotting")
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataViewerApp(root)
    root.mainloop()