from http.server import HTTPServer
from flight_data_request_handler import FlightDataRequestHandler
import argparse

HOST_NAME = 'localhost'


def parse_arguments() -> int:
    """
    The user has the option is specifying the port the application will run on with the -p/--port parameter.

    By default, 8080 is used.
    """
    parser = argparse.ArgumentParser(
        description='This program launches a service hosted on localhost that can be queried by API calls to retrieve data from attached parquet files. Available endpoints are listed in the README.md file.',
        add_help=True,
    )

    parser.add_argument(
        '-p',
        '--port',
        help='Unoccupied port that the service will run on. If not provided, 8080 is used by default.',
        default=8080,
        type=int
    )

    args = parser.parse_args()

    return args.port


if __name__ == "__main__":
    """
    This is the starting point of the service. Data is loaded separately in flight_data_request_handler.py as a constant (not ideal).

    The server serves requests on localhost with the port specified. Documentation on the implemented API calls is available in README.md.
    """
    
    port_number = parse_arguments()
    http_server = HTTPServer((HOST_NAME, port_number), FlightDataRequestHandler)

    print('Server now running...')
    http_server.serve_forever()
