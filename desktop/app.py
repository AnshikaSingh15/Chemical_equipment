import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE_URL = "http://127.0.0.1:8000/api"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(200, 100, 700, 550)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Upload button
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_button)

        # Summary label
        self.summary_label = QLabel("Upload a CSV file to see summary.")
        self.summary_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.summary_label)

        # Matplotlib figure
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            # Upload CSV to backend
            with open(file_path, "rb") as f:
                response = requests.post(
                    f"{API_BASE_URL}/upload/",
                    files={"file": f}
                )

            if response.status_code != 200:
                QMessageBox.critical(
                    self,
                    "Upload Failed",
                    response.text
                )
                return

            # Fetch latest summary
            summary_response = requests.get(
                f"{API_BASE_URL}/latest-summary/"
            )

            if summary_response.status_code != 200:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to fetch summary"
                )
                return

            data = summary_response.json()
            self.update_ui(data)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def update_ui(self, data):
        # Update summary text
        self.summary_label.setText(
            f"Total Equipment: {data['total_count']}\n"
            f"Avg Flowrate: {data['avg_flowrate']:.2f}\n"
            f"Avg Pressure: {data['avg_pressure']:.2f}\n"
            f"Avg Temperature: {data['avg_temperature']:.2f}\n"
        )

        # Plot bar chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = list(data["type_distribution"].keys())
        counts = list(data["type_distribution"].values())

        ax.bar(types, counts)
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Application closed")
