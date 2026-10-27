"""Tiny Chrome DevTools Protocol screenshot helper (no external deps).

Usage:
  python scripts/shot.py URL OUT.png [--w 1440] [--h 900] [--scroll 0] [--full]
Requires Chrome started with --remote-debugging-port=9222.
"""
import base64
import json
import os
import socket
import struct
import sys
import time
import urllib.request

PORT = 9222


class WS:
    def __init__(self, url):
        _, rest = url.split("://", 1)
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.s.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.mid = 0

    def _recv(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(65536)
            if not chunk:
                raise EOFError
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, method, params=None):
        self.mid += 1
        payload = json.dumps({"id": self.mid, "method": method, "params": params or {}}).encode()
        header = b"\x81"
        n = len(payload)
        if n < 126:
            header += struct.pack("B", 0x80 | n)
        elif n < 65536:
            header += struct.pack("!BH", 0x80 | 126, n)
        else:
            header += struct.pack("!BQ", 0x80 | 127, n)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.s.sendall(header + mask + masked)
        while True:
            b1, b2 = self._recv(2)
            ln = b2 & 0x7F
            if ln == 126:
                ln = struct.unpack("!H", self._recv(2))[0]
            elif ln == 127:
                ln = struct.unpack("!Q", self._recv(8))[0]
            data = self._recv(ln)
            if b1 & 0x0F == 1:
                msg = json.loads(data.decode())
                if msg.get("id") == self.mid:
                    return msg


def main():
    url, out = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]

    def arg(name, default):
        return type(default)(args[args.index(name) + 1]) if name in args else default

    w, h = arg("--w", 1440), arg("--h", 900)
    scroll = arg("--scroll", 0)
    full = "--full" in args

    tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list"))
    target = next(t for t in tabs if t["type"] == "page")
    ws = WS(target["webSocketDebuggerUrl"])
    ws.send("Page.enable")
    ws.send("Network.enable")
    ws.send("Network.setCacheDisabled", {"cacheDisabled": True})
    ws.send("Emulation.setDeviceMetricsOverride",
            {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": w < 600})
    ws.send("Page.navigate", {"url": url})
    time.sleep(2.2)
    # force scroll-reveal animations + any lazily animated element to their end state
    ws.send("Runtime.evaluate", {"expression": """
      document.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible'));
      window.scrollTo(0, %d);
    """ % scroll, "awaitPromise": False})
    time.sleep(1.2)
    params = {"format": "png"}
    if full:
        m = ws.send("Page.getLayoutMetrics")["result"]["contentSize"]
        params["clip"] = {"x": 0, "y": 0, "width": w, "height": m["height"], "scale": 1}
        params["captureBeyondViewport"] = True
    shot = ws.send("Page.captureScreenshot", params)["result"]["data"]
    with open(out, "wb") as f:
        f.write(base64.b64decode(shot))
    print("saved", out, w, h, "scroll", scroll)


if __name__ == "__main__":
    main()
