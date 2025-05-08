# Marine Computational Lab Assignment

This project is a web application for analyzing marine data and performing various calculations related to marine systems.

## Features

- Upload and process marine data files
- Perform calculations on marine systems
- Generate visualizations and plots
- Analyze damping characteristics

## Project Structure

- `src/` - Source code directory
  - `app.py` - Main Streamlit application
  - `data_processor.py` - Data processing and handling
  - `marine_calculator.py` - Marine system calculations
  - `visualizer.py` - Plotting and visualization functions
- `data/` - Data storage directory
- `uploads/` - Temporary file upload directory
- `damping/` - Damping analysis results

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Requirements

- Python 3.8+
- See requirements.txt for all dependencies

## Usage

1. Start the application using `streamlit run src/app.py`
2. Upload your marine data files
3. Adjust ship parameters in the sidebar
4. Set time parameters for analysis
5. View results and visualizations

## License

This project is licensed under the MIT License. 