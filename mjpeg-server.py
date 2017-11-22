#!/usr/bin/python
"""
    From: https://gist.github.com/Drunkar/6235f591cb53da2b9c3e6eaa81c7ea66
    Original Author: Igor Maculan - n3wtron@gmail.com
    Modified by: Drunkar - drunkars.p@gmail.com
    A Simple mjpg stream http server
"""
import cv2
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import io
import timeit
capture1 = None

class CamHandler(BaseHTTPRequestHandler):
#    @profile
    def do_GET(self):
        N = 10
        k = 0
        t = timeit.default_timer()
        t_prev = 0
        if self.path.endswith("cam1.mjpg"):
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=--jpgboundary")
            self.end_headers()
            while True:
                k=k+1
                try:
                    rc, img1 = capture1.read()

                    if not rc:
                        continue

                    if(k % N == 0):
                        t_prev = t
                        t = timeit.default_timer()
                        print("fps: ",N/(t-t_prev))

                    # imgRGB = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                    result, encimg = cv2.imencode('.jpg', img1, encode_param)
                    self.wfile.write(b"--jpgboundary")
                    self.send_header(b"Content-type", "image/jpeg")
                    self.send_header(b"Content-length", len(encimg))
                    self.end_headers()
                    self.wfile.write(encimg.tobytes())
                except KeyboardInterrupt:
                    break
            return
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head></head><body>")
            self.wfile.write(b"<img src='/cam1.mjpg'/>")
            self.wfile.write(b"</body></html>")
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    global capture1
    capture1 = cv2.VideoCapture(0)
#    capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 1900)
#    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#    capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#    capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
#    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
#    capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 848)
#    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#    capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    capture1.set(cv2.CAP_PROP_FRAME_WIDTH,424);
    capture1.set(cv2.CAP_PROP_FRAME_HEIGHT,240);

    global img1
    try:
        server = ThreadedHTTPServer(("0.0.0.0", 8080), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        capture1.release()
        server.socket.close()


if __name__ == "__main__":
    main()
