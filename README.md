# Automated-Index-Generator

A program to create the various Noemalised Difference Indices like NDVI, NDMI and NDWI.

## Steps followed
1. Downloads the images from USGS EarthExplorer
2. Unzips the images
3. Performs atmospheric correction
4. Calculates the indices using the unzipped images
5. Creates relevant mosaics
6. Clips the ROI
7. Performs time-series analysis
