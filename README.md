# Sheets To Charts

Graphicx is a web application that allows you to convert .xlsx and .csv files into interactive and customizable charts.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [License](#license)
- [Feedback and Contributions](#feedback-and-contributions)

## Overview

Graphicx is a user-friendly tool for data visualization. It simplifies the process of creating charts from Excel (.xlsx) and CSV files. With Graphicx, you can quickly turn your data into insightful visualizations with a modern and intuitive interface.

## Features

- **Easy File Upload:** Simply upload your .xlsx or .csv files to get started
- **Multiple Chart Types:** Choose from bar, line, radar, pie, and doughnut charts
- **Customizable:** Change colors, formats, and axis labels
- **Interactive Charts:** View and interact with your charts directly in the browser
- **Format Options:** Apply currency, percentage, and unit formatting to axes
- **Print-Friendly:** Export your charts directly to PDF via browser print
- **No Coding Required:** No coding or technical skills needed

## Requirements

Before using this project, ensure that you have the following software installed:

- **Python 3.11 or later:** Download from [python.org](https://www.python.org/downloads/)

![python](https://logosmarcas.net/wp-content/uploads/2021/10/Python-Logo.png)

## Installation and Setup

**1. Clone the Repository:**

```bash
git clone https://github.com/Mulekotd/sheets-to-charts.git
cd sheets-to-charts/
```

**2. Create Virtual Environment:**

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

**3. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables:**

Create a `.env` file in the project root:

```bash
FLASK_SECRET_KEY=your_secure_secret_key_here
```

**5. Run the Application:**

```bash
python run.py
```

## Project Structure

```bash
sheets-to-charts/
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   └── main.py
│   ├── static
│   │   ├── css
│   │   │   ├── files.css
│   │   │   └── styles.css
│   │   ├── favicon.ico
│   │   └── js
│   │       ├── chart-controls.js
│   │       └── file-preview.js
│   ├── templates
│   │   ├── base.html.jinja
│   │   ├── dashboards.html.jinja
│   │   ├── index.html.jinja
│   │   └── select_columns.html.jinja
│   └── utils
│       ├── __init__.py
│       ├── chart_creator.py
│       └── file_processor.py
├── requirements.txt
└── run.py
```

## Usage

1. Start the application (see [Installation](#installation-and-setup))
2. Visit `http://localhost:5000/` and have fun!

## License

This project is open-source and is provided under the MIT License. You are free to use and modify it as needed. Feel free to contribute to the project or report any issues on the GitHub repository.

![mit](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1920px-MIT_logo.svg.png)

## Feedback and Contributions

We welcome feedback, suggestions, and contributions from the community. If you have ideas for improvements or encounter any issues, please don't hesitate to [open an issue](https://github.com/Mulekotd/sheets-to-charts/issues) on GitHub.
