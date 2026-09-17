# Network Security Tools

A collection of Python scripts for network diagnostics and reconnaissance, built as hands-on practice with sockets, concurrency, and error handling.

## Scripts

### `ip_subnet_calculator.py`
Validates an IPv4 address and subnet mask, then computes the network address, broadcast address, and usable host range.

### `ping_sweep.py`
Pings a list of hosts from a file, with adaptive retry logic (a second, deeper scan on timeout) and classifies failures as DNS resolution failure, unreachable, or timeout. Logs timestamped results to a file.

### `port_scanner.py`
A TCP connect-scan port scanner with two modes: scanning a specific list of ports from a file, or scanning a numeric range. Uses OS-level socket error codes (`errno`) to distinguish closed vs. filtered ports, and logs results with timing.

### `port_scanner_threaded.py`
An evolution of `port_scanner.py` using `ThreadPoolExecutor` (50 workers) to scan a port range concurrently, cutting scan time significantly. Includes input validation, optional logging of closed ports, and handles `KeyboardInterrupt`/DNS errors gracefully.

## Usage
Each script is standalone and interactive — run it directly and follow the prompts:

```bash
python3 ip_subnet_calculator.py
python3 ping_sweep.py
python3 port_scanner.py
python3 port_scanner_threaded.py
```

## Platform Compatibility

- **`ip_subnet_calculator.py`** — Fully cross-platform. Pure Python logic with no OS-level calls.
- **`ping_sweep.py`** — **Windows only.** Uses the Windows `ping` syntax (`-n` for count) and parses Windows-specific output strings (e.g., `"Request timed out"`). It will not behave correctly on Linux/macOS, which use different flags and output formats.
- **`port_scanner.py`** and **`port_scanner_threaded.py`** — Cross-platform at the socket level, but most accurate on Linux/macOS. These scripts label errors using Python's `errno` module, which maps POSIX error codes (used by Linux/macOS) correctly — e.g., a refused connection is labeled `ECONNREFUSED`. On Windows, socket errors return WinSock-specific codes that don't map cleanly to `errno`, so error labels may come back as `None` or generic on that platform, even though the scan itself still runs.

## Disclaimer
These tools are for educational use and authorized network diagnostics only. Only scan hosts and networks you own or have explicit permission to test.
