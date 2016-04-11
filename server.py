from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.error import HTTPError
from datetime import datetime

from pokedex import PokedexEntry
from config import PORT, HOSTNAME

class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
         self.send_response(200)
         self.send_header("Content-type", "text/html")
         self.end_headers()

    def do_GET(self):
        path = self.path.split("/")[1:]

        if (len(path)==1 and path[0] == ""):
            self.handle_page_from_file("index.html")
        elif (len(path)==1):
            self.handle_page_from_file(path[0])
        elif (len(path)==2 and path[0] == "pokemon"):
            self.handle_pokemon_search(path[1])
        else:
            self.handle_error_page()

    def send_str(self, string):
        self.wfile.write(string.encode("utf-8"))
 
    def handle_page_from_file(self, pagename):

        try:
            with open("client/"+pagename) as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.send_str(f.read())
        except IOError:
            self.handle_error_page()

    def handle_error_page(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.send_str("<html><head><title>Pokedex</title></head><body>")
        self.send_str("<p>Prof. Oak: There's a time and place for everything!</p>")
        self.send_str("</body></html>")

    def handle_pokemon_search(self,pokemon):
        try:
            pokemon = PokedexEntry(pokemon)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.send_str(pokemon.get_json())
        except HTTPError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.send_str("{}")

if __name__ == '__main__':
     server_class = HTTPServer
     httpd = server_class((HOSTNAME, PORT), MyHandler)
     print(datetime.now(), "Server Starts - %s:%s" % (HOSTNAME, PORT))
     try:
         httpd.serve_forever()
     except KeyboardInterrupt:
         pass
     httpd.server_close()
     print(datetime.now(), "Server Stops - %s:%s" % (HOSTNAME, PORT))
