from flightdatawrapper import Flight_data
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

flight_data = Flight_data()

class FlightDataService(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/csv')
        self.end_headers()

        self.wfile.write(bytes(flight_data.list_loaded_datasets(), 'utf-8'))
        return

    def handle_http(self):
        return

    def respond(self):
        return


server = HTTPServer((HOST_NAME, PORT_NUMBER), FlightDataService)


server.serve_forever()