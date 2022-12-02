#!/bin/bash

echo "Enter the port which the service is running on. Example input: 8080"
read PORT

## /datasets endpoint according to task num. 2

curl "http://localhost:$PORT/datasets" \
    -H "Accept: text/csv" -X GET >> ./output/datasets.csv


## /aircraft/models endpoint according to task num. 3

curl "http://localhost:$PORT/aircraft/models" \
    -H "Accept: text/csv" -X GET >> ./output/air_models.csv


## /aircraft/active endpoint according to task num. 4

# Model and manufacturer unspecified
curl "http://localhost:$PORT/aircraft/active" \
    -H "Accept: text/csv" -X GET >> ./output/air_active_unfiltered.csv

# Model specified
curl "http://localhost:$PORT/aircraft/active?model=E75N1" \
    -H "Accept: text/csv" -X GET >> ./output/air_active_model.csv

# Manufacturer specified
curl "http://localhost:$PORT/aircraft/active?manufacturer=BOEING" \
    -H "Accept: text/csv" -X GET >> ./output/air_active_manufacturer.csv

# Model and manufacturer specified:
curl "http://localhost:$PORT/aircraft/active?model=E75N1&manufacturer=BOEING" \
    -H "Accept: text/csv" -X GET >> ./output/air_active_model+manufacturer.csv

# Manufacturer with spaces specified. Note that spaces are replaced with underscores.
curl "http://localhost:$PORT/aircraft/active?manufacturer=SATER_VERNON_D" \
    -H "Accept: text/csv" -X GET >> ./output/air_active_manufacturer_spaces.csv
