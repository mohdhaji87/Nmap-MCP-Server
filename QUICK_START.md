# Nmap MCP Server - Quick Start Guide

## 🚀 FastMCP Implementation

This server uses **FastMCP** with stdio transport for high-performance MCP communication.

## Quick Installation

1. **Prerequisites:**
   - Python 3.10+
   - Nmap installed

2. **Install:**
   ```bash
   ./install.sh
   ```

## 🎯 Available Tools

The FastMCP server provides 11 powerful Nmap tools:

| Tool | Description |
|------|-------------|
| `nmap_basic_scan` | Quick, comprehensive, or stealth scans |
| `nmap_service_detection` | Detect services and versions |
| `nmap_os_detection` | Detect operating systems |
| `nmap_script_scan` | Run NSE scripts |
| `nmap_stealth_scan` | SYN scans with minimal detection |
| `nmap_comprehensive_scan` | Full-featured scans |
| `nmap_ping_scan` | Discover live hosts |
| `nmap_port_scan` | Scan specific ports |
| `nmap_vulnerability_scan` | Run vulnerability scripts |
| `nmap_network_discovery` | Discover network hosts |
| `nmap_custom_scan` | Custom Nmap options |

## 🔧 FastMCP Usage Examples

### Basic Network Scan
```python
result = await nmap_basic_scan(
    targets="192.168.1.0/24",
    ports="common",
    scan_type="quick"
)
```

### Service Detection
```python
result = await nmap_service_detection(
    targets="example.com",
    ports="80,443,8080",
    intensity=7
)
```

### Vulnerability Assessment
```python
result = await nmap_vulnerability_scan(
    targets="192.168.1.100",
    ports="common",
    vuln_category="all"
)
```

### Custom Scan
```python
result = await nmap_custom_scan(
    targets="example.com",
    custom_options="-sS -p 1-1000 -A --script=vuln",
    output_format="normal"
)
```

## 🏃‍♂️ Running the FastMCP Server

### Method 1: Direct Execution (Stdio Transport)
```bash
python server.py
```

### Method 2: MCP Client Integration
Use the `mcp_config.json` file with your MCP client.

### Method 3: Test FastMCP Tools
```bash
python test_fastmcp.py
```

### Method 4: Test Examples
```bash
python example_usage.py
```

## ⚠️ Security Notice

- **Only scan networks you own or have permission to scan**
- **Some scans may trigger security systems**
- **Be mindful of network impact**

## 🆘 Troubleshooting

1. **"nmap command not found"**
   - Install nmap: `brew install nmap` (macOS) or `sudo apt install nmap` (Ubuntu)

2. **Import errors**
   - Install dependencies: `pip install -e .`

3. **Permission errors**
   - Some scans require elevated privileges

4. **FastMCP issues**
   - Ensure you're using Python 3.10+
   - Check that MCP package is up to date

## 📚 Full Documentation

See `README.md` for complete documentation and advanced usage examples.

## 🔍 FastMCP Features

- **Type Safety**: Full type hints and validation
- **Clean API**: Simple decorator-based tool registration
- **Stdio Transport**: Efficient communication
- **Async Support**: Non-blocking operations
- **Error Handling**: Comprehensive error management 