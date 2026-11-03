# NetPulse

A local network diagnostics dashboard built with Python, HTML, CSS, and JavaScript.



## Features

- Sends one ping to 127.0.0.1 per check
- Checks the local machine at 127.0.0.1
- Checks the configured router at 192.168.1.1
- Rejects other inputs in JavaScripts and Python
- Stops a ping check after five seconds
- Measures total check duration
- Charts the last 10 check durations
- Uses cyan bars for replies and orange for no reply or timeout
- Shows timestamped check history
- Uses a dark interface with cyan accents

## Requirements

- macOS
- Python 3.9 or newer
- A web browser

No additional Python packages are required.

## Run locally

Download this repository and open its folder in Terminal.

Start the server:

```bash
python3 server.py
```

Keep Terminal running and open this address in your browser:

http://127.0.0.1:8000/index.html

Enter 127.0.0.1 and click Run Check.

To stop the server, press Control + C in Terminal.

## How it works

JavaScript requests the /check endpoint. Python runs a single
ping and returns the result as JSON. The webpage displays
the result and updates the chart and history.

## Current limitations

- Checks only 127.0.0.1 and the configured router, 192.168.1.1
- A different router address must be configured in both server.py and index.html.
- A successful loopback check does not verify internet connectivity.
- Duration measures the complete browser-to-server check,
  including starting ping. It is not the ping round-trip time.
- Chart and history clear when the page refreshes.
- The Python server must run locally; GitHub Pages alone
  cannot run the ping backend.

## What I learned

- Building a webpage with HTML and CSS
- Handling input and clicks with JavaScript
- Connecting JavaScript to a Python HTTP server
- Using subprocess to run ping
- Returning and reading JSON
- Displaying measurements in a chart
- Troubleshooting with browser developer tools
