# Flight Data Service as implemented for GoodData homework.  
<br/>

## How to test what it does 

1. Navigate to `/Flight_Data_Service_homework/flight_data_service`
2. Run `python launch.py` By default, the service runs on port 8080. If you want, you can specify a different port with `python launch.py -p 9090`, for example.
    * Example of successful launch:
        ```
        jrehanek@jan flight_data_service % python launch.py
        FlightData data loaded successfully...
        Server now running...
        ```
3. Open a second terminal window and navigate to `/Flight_Data_Service_homework/test`
4. Run `bash test.sh`. You will be prompted for the port the service is running on. Enter it without colon, like this: `8080`. This simple script uses several curl requests to test the functionality of the endpoints. To keep the terminal uncluttered, the results are deposited in `/Flight_Data_Service_homework/test/output` in CSV form.
<br/>

## What it doesn't do <a name="missing"></a>

I only completed tasks: 1, 2, 3, 4, and bonus 1.

The rest of the tasks are not implemented. Testing of the functionality is also not great: I provided a simple shell script that tests the endpoints with curls, but the code as a whole would benefit a lot from a thorough unit-testing suite.
<br/>

## Endpoint documentation

The following endpoints are available:
```
/datasets
/aircraft/models
/aircraft/active
```
#### **/datasets**
Only GET is supported. According to homework task num. 2.

Results are returned in CSV form. It returns a summary of available datasets with their name, columns, and rowcount.

Example:
```
curl "http://localhost:8080/datasets" \
    -H "Accept: text/csv" -X GET >> datasets.csv
```

#### **/aircraft/models**
Only GET is supported. According to homework task num. 3.

Results are returned in CSV form. It returns a summary of all aircraft models with the following columns: model,manufacturer,seats

Example:
```
curl "http://localhost:8080/aircraft/models" \
    -H "Accept: text/csv" -X GET >> air_models.csv
```


#### **/aircraft/active**
Only GET is supported. According to homework task num. 4.

Query parameters `model` and `manufacturer` are supported. For those that contain spaces, replace spaces with underscores. If the given query parameter is not supplied, the service assumes that no filtering for it is desired and returns the full result.

Results are returned in CSV form. It returns a summary of all active aircraft filtered by the parameters above with the following columns: manufacturer,model,seats,aircraft_serial,name,county

Examples:

```
# Model and manufacturer unspecified
curl "http://localhost:8080/aircraft/active" \
    -H "Accept: text/csv" -X GET >> air_active_unfiltered.csv

# Model specified
curl "http://localhost:8080/aircraft/active?model=E75N1" \
    -H "Accept: text/csv" -X GET >> air_active_model.csv

# Manufacturer specified
curl "http://localhost:8080/aircraft/active?manufacturer=BOEING" \
    -H "Accept: text/csv" -X GET >> air_active_manufacturer.csv

# Model and manufacturer specified:
curl "http://localhost:8080/aircraft/active?model=E75N1&manufacturer=BOEING" \
    -H "Accept: text/csv" -X GET >> air_active_model+manufacturer.csv

# Manufacturer with spaces specified. Note that spaces are replaced with underscores.
curl "http://localhost:8080/aircraft/active?manufacturer=SATER_VERNON_D" \
    -H "Accept: text/csv" -X GET >> air_active_manufacturer_spaces.csv
```
<br/>

## Ending notes and thanks
Overall, this was a pretty good opportunity to learn something new. My experience with pandas before I started this was pretty much non-existent. I also had to learn how to setup a HTTP server and handler in Python and try to make it all work together. Due to that time needed for learning, there wasn't really any time left to tackle the more advanced tasks.

I appreciate the opportunity and I'd be grateful for any feedback on where I should improve and any learning materials/example projects I could continue with.
