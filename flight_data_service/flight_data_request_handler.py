from http.server import BaseHTTPRequestHandler
from typing import Callable
from urllib import parse
from flight_data import FlightData

"""
FLIGHT_DATA is currently defined as a constant available to the whole package.

Unfortunately, I ran into the problem of how to properly interface the FlightDataRequestHandler and the FlightData class too late,\
    and this is here instead of a proper solution that I would need more time to figure out.

tl;dr ->  :(
"""
FLIGHT_DATA = FlightData()


class FlightDataRequestHandler(BaseHTTPRequestHandler):
    """
    FlightDataRequestHandler handles the HTTP requests sent to FlightDataService. It includes rudimentary routing and some helper functions.\
        Its functionality is currently tied to the FLIGHT_DATA constant being loaded and ready.

    Currently enabled endpoints are:
    
        /datasets

        /aircraft/models

        /aircraft/active
    """
    parsed_path: parse.ParseResult

    def parse_path(self) -> None:
        """
        Function converting the path of a request into the parsed object created by parse.urlparse. The result is stored as an instance attribute.
        """
        self.parsed_path = parse.urlparse(self.path)

    def do_GET(self) -> None:
        """
        Function handling incoming GET requests. The path of the request is parsed and the response is handled according to routing defined in handle_GET.

        The response is stored in the respond variable (a callable), which is immediately called after.
        """
        self.parse_path()

        respond = self.handle_GET()

        respond()

    def handle_GET(self) -> Callable[[], None]:
        """
        Function routing according to the request path. A callable is returned that is subsequently invoked in do_GET.

        If the request path doesn't match any known endpoint, a generic function is returned instead that informs the user about which endpoints are available.
        """
        if self.parsed_path.path == '/datasets':
            return self.get_datasets
        elif self.parsed_path.path == '/aircraft/models':
            return self.get_aircraft_models
        elif self.parsed_path.path == '/aircraft/active':
            return self.get_aircraft_active
        else:
            return self.unsupported_endpoint

    def get_datasets(self) -> None:
        """
        Function returning CSV data as specified in list_loaded_datasets of the FlightData class.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/csv')
        self.end_headers()

        resp = bytes(FLIGHT_DATA.list_loaded_datasets(), 'utf-8')

        self.wfile.write(resp)

    def get_aircraft_models(self) -> None:
        """
        Function returning CSV data as specified in list_aircraft_models of the FlightData class.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/csv')
        self.end_headers()

        resp = bytes(FLIGHT_DATA.list_aircraft_models(), 'utf-8')

        self.wfile.write(resp)

    def get_aircraft_active(self) -> None:
        """
        Function returning CSV data as specified in list_active_aircraft of the FlightData class.

        This endpoint allows for filtering by model and manufacturer, which implemented as query strings.\
            If no values are provided, the filter_by object has them listed as keys with None value.

        Manufacturer/Model names which contain spaces should be provided with underscores replacing the spaces. Example: SATER VERNON D -> manufacturer=SATER_VERNON_D
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/csv')
        self.end_headers()

        filter_by: dict[str, str | None] = {
            'manufacturer': None,
            'model': None
        }

        query_params = dict(parse.parse_qsl(self.parsed_path.query))

        if 'manufacturer' in query_params:
            filter_by['manufacturer'] = query_params['manufacturer'].replace('_', ' ')
        if 'model' in query_params:
            filter_by['model'] = query_params['model'].replace('_', ' ')

        resp = bytes(FLIGHT_DATA.list_active_aircraft(filter_by), 'utf-8')

        self.wfile.write(resp)

    def do_POST(self) -> None:
        """
        POST request are currently not supported.
        """
        self.unsupported_method()

    def do_PUT(self) -> None:
        """
        PUT request are currently not supported.
        """
        self.unsupported_method()

    def do_PATCH(self) -> None:
        """
        PATCH request are currently not supported.
        """
        self.unsupported_method()

    def do_DELETE(self) -> None:
        """
        DELETE request are currently not supported.
        """
        self.unsupported_method()

    def unsupported_method(self) -> None:
        """
        Function designed to provide a generic message to the user that the method they used is not supported

        The response is sent with a 405 Method Not Allowed status code.
        """
        self.send_response(405)

        self.send_header('Content-type', 'text/plain')
        self.send_header('Allow', 'GET')
        self.end_headers()

        self.wfile.write(bytes('Unsupported method. Allowed methods are:\n\n\tGET', 'utf-8'))

    def unsupported_endpoint(self) -> None:
        """
        Function designed to provide a generic message to the user that the endpoint they used is not supported.\
            It provides the user with a list of endpoints which they can access.

        The response is sent with a 404 Not Found Not status code.
        """
        self.send_response(404)

        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(
            bytes('Unsupported endpoint. Allowed endpoints are:\n\n\t/datasets\n\t/aircraft/models\n\t/aircraft/active', 'utf-8'))
