# DeepNeuroBoun - Rodent Behavior Analysis GUI

Welcome to the DeepNeuroBoun project! This open-source software project has been developed under the guidance of Associate Professor Güneş Ünal and aims to create an intuitive Graphical User Interface (GUI) for automating behavioral neuroscience research analysis. The project facilitates the analysis of rodent behavior, enabling researchers to process and interpret experimental data efficiently.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [How to Use](#how-to-use)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Understanding rodent behavior is crucial in the field of behavioral neuroscience. However, manual analysis of behavioral data can be time-consuming and prone to human error. The DeepNeuroBoun project addresses this challenge by providing a user-friendly GUI that automates the analysis process. By utilizing this tool, researchers can save time, reduce errors, and focus more on the interpretation of results.

## Features

- **User-friendly GUI**: The DeepNeuroBoun GUI offers an intuitive interface for researchers to interact with the analysis tools effortlessly.

- **Automated Analysis**: The project implements state-of-the-art **DeepLabCut** algorithms to automatically analyze rodent behavior data, reducing the need for manual intervention.

- **Data Visualization**: Visualize and explore behavioral data through interactive graphs and plots, aiding in the understanding of experimental outcomes.

- **Export Capabilities**: The GUI allows users to export analysis results in various formats, making it easy to share and collaborate with colleagues.

- **Customization**: Researchers can customize analysis parameters and algorithms according to their specific research requirements.

## Getting Started

Follow these instructions to set up the DeepNeuroBoun project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher installed on your system.
- The required Python packages can be found in the `requirements.txt` file.

### Installation

1. Clone the repository to your local machine using the following command:

```
git clone https://github.com/DenizK00/DeepNeuroBoun.git
```

2. Change your working directory to the project's root folder:

```
cd DeepNeuroBoun
```

3. Install the required Python packages using pip:

```
pip install -r requirements.txt
```

## How to Use

1. After completing the installation, run the GUI using the following command:

```
python GUI.py
```

2. The GUI will launch, and you can start by selecting Generate New Analysis (for analysing the video) or Use Existing Analysis (using the data of an already processed video).

3a. If the generate new analysis option is selected, there will be another selection of Generic Dry Maze or Morris Water Maze.

3b. If the use existing analysis option is selected gui will continue to the 4th step

4. Continue by drawing an arbitrary line and type how long that line is, this way, the program will have the pixel distance to cm transition, And also draw the maze by following the instructions in the GUI.

5. Once the analysis is complete, explore the concluding info and visualizations.
  
6.  Afterwards, export the results in your desired format.

## Contributing

We welcome contributions from the open-source community to enhance the DeepNeuroBoun project. If you would like to contribute, please follow these steps:

1. Fork the repository to your GitHub account.

2. Create a new branch from the `develop` branch with a descriptive name.

3. Make your code changes and additions.

4. Test your changes to ensure they work as expected.

5. Commit your changes and push them to your forked repository.

6. Open a pull request to the `develop` branch of the main repository, describing the changes you made.

7. We will review your pull request and collaborate with you to address any feedback or necessary changes.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

Thank you for showing interest in the DeepNeuroBoun project. We hope this software proves to be a valuable tool in your rodent behavior analysis endeavors. For any queries or feedback, feel free to contact the project maintainers. Happy analyzing!

![DeepNeuroBoun Logo](https://cogsci.boun.edu.tr/sites/cogsci.boun.edu.tr/files/styles/lab_200x300/public/banner_magenta_and_cyan_neurons.jpg?itok=0F5a7XMz&c=5948ea4bbdc9dadfd4c0ef6e30578da3)
