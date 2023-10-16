import http.server
import http.client


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Define the remote server and URL of the PDF file
            remote_server = 'consolidated-bank.com'
            remote_url = '/pdf/Consolidated%20Bank%20REVISED%20%2033x3%2029-8-23_230829_144619.pdf'

            # Create a connection to the remote server
            conn = http.client.HTTPSConnection(remote_server)

            # Send a GET request to the remote server
            conn.request('GET', remote_url)

            # Get the response from the remote server
            response = conn.getresponse()

            # Check if the response is successful
            if response.status == 200:
                # Set the appropriate headers for PDF content
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, baggage')
                self.end_headers()

                # Send the PDF content to the client
                self.wfile.write(response.read())
            else:
                # Handle other response statuses (e.g., 404 Not Found)
                self.send_error(404, 'File not found')

            # Close the connection to the remote server
            conn.close()

        except Exception as e:
            # Handle exceptions (e.g., network errors)
            print(f"Error: {e}")
            self.send_error(500, 'Internal Server Error')

    def do_OPTIONS(self):
        # Handle OPTIONS requests by sending a 200 OK response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')  # Allow requests from localhost:3000
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, baggage')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, sentry-trace')
        self.end_headers()


if __name__ == '__main__':
    # Define the local server's host and port
    host = 'localhost'
    port = 8060  # You can change this port if needed

    # Create and run the proxy server
    http.server.test(HandlerClass=ProxyHandler, port=port)
