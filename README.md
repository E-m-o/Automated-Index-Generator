# Raster Image Calculator
This tool is a utility to automate the task of downloading satellite images and calculating the 
Normalized indices for a particular region of interest in the Indian Subcontinent. 

## How to use the tool
The subdist_boundingBox.csv file contains the data for each region of India. 
The important data is the State name, District name, Subdistrict name and the bounding box coordinates.

The data can be modified and expanded to contain entirely different countries and their regions.

Run the main.py file and follow the instructions on the screen.

You will be prompted to: 
1. Choose a satellite
2. Choose start and end dates of interest
3. Choose a region of interest
4. Choose which indices you want to have calculated
5. Wait for the analysis to be completed

The result will be in the analysis folder in the latest Request folder in the Images directory.

Example Result:
![Sample Output](./docs/Automated Index Calculator.png "Sample NDVI Output")
