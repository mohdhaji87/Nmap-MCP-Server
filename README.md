# Nmap MCP Server

A Model Context Protocol (MCP) server that exposes Nmap CLI functionality as MCP tools using **FastMCP** with stdio transport. This server provides comprehensive network scanning capabilities through the Nmap command-line tool.

## 🚀 FastMCP Implementation

This server is built using **FastMCP**, a modern, high-performance MCP framework that provides:
- **Simplified API**: Clean decorator-based tool registration
- **Type Safety**: Full type hints and validation
- **Stdio Transport**: Efficient communication via standard input/output
- **Async Support**: Non-blocking operations with proper error handling

## Features

The Nmap MCP Server exposes the following tools using FastMCP decorators:

### 1. Basic Scan (`nmap_basic_scan`)
Perform basic Nmap scans with different intensity levels:
- **Quick**: Fast scan with high throughput
- **Comprehensive**: Full scan with service detection and OS detection
- **Stealth**: Low-profile scan to avoid detection

### 2. Service Detection (`nmap_service_detection`)
Detect services and versions running on target hosts with configurable intensity levels (0-9).

### 3. OS Detection (`nmap_os_detection`)
Detect operating systems running on target hosts with configurable retry attempts.

### 4. Script Scanning (`nmap_script_scan`)
Run NSE (Nmap Scripting Engine) scripts for advanced reconnaissance and vulnerability assessment.

### 5. Stealth Scan (`nmap_stealth_scan`)
Perform SYN scans with minimal detection using configurable timing templates.

### 6. Comprehensive Scan (`nmap_comprehensive_scan`)
Perform full-featured scans combining multiple detection methods.

### 7. Ping Scan (`nmap_ping_scan`)
Discover live hosts using various ping methods (ICMP, TCP, or both).

### 8. Port Scan (`nmap_port_scan`)
Scan specific ports using different methods (SYN, Connect, UDP).

### 9. Vulnerability Scan (`nmap_vulnerability_scan`)
Run vulnerability detection scripts with different categories.

### 10. Network Discovery (`nmap_network_discovery`)
Discover hosts and services on entire networks.

### 11. Custom Scan (`nmap_custom_scan`)
Perform scans with user-defined Nmap options for maximum flexibility.

## Prerequisites

- Python 3.10 or higher
- Nmap installed and available in your system PATH

### Installing Nmap

**macOS:**
```bash
brew install nmap
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nmap
```

**CentOS/RHEL:**
```bash
sudo yum install nmap
# or for newer versions:
sudo dnf install nmap
```

**Windows:**
Download and install from [nmap.org](https://nmap.org/download.html)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd nmap-mcp-server
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

### Running the FastMCP Server

The server can be run directly with stdio transport:

```bash
python server.py
```

Or using the installed script:

```bash
nmap-mcp-server
```

### Claude Desktop Configuration

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "NmapMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/haji/mcp-servers/nmap-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Configuration Steps:**
1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Add the JSON configuration above
4. Restart Claude Desktop
5. Verify the server is connected

## FastMCP Tool Examples

### Basic Network Scan
```python
# The tool is called with typed parameters
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

## FastMCP Architecture

The server uses FastMCP's clean decorator pattern:

```python
@app.tool(
    name="nmap_basic_scan",
    description="Perform a basic Nmap scan of specified targets"
)
async def nmap_basic_scan(
    targets: str,
    ports: str = "common",
    scan_type: str = "quick"
) -> str:
    """Perform a basic Nmap scan of specified targets."""
    # Implementation here
    return result
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Legal Compliance**: Only scan networks and systems you own or have explicit permission to scan.
2. **Network Impact**: Some scans can be resource-intensive and may impact network performance.
3. **Detection**: Aggressive scans may trigger security systems and firewalls.
4. **Rate Limiting**: The server includes timeouts and rate limiting to prevent abuse.

## Error Handling

The FastMCP server includes comprehensive error handling for:
- Nmap command not found
- Command timeouts
- Invalid arguments
- Network connectivity issues
- Permission errors

## Logging

The server uses Python's built-in logging system. Logs include:
- Command execution details
- Error messages
- Performance metrics

## Testing

Test the FastMCP server:

```bash
# Test tool registration and functionality
python test_fastmcp.py

# Test examples
python example_usage.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before scanning any network or system.

## Support

For issues and questions:
1. Check the error logs
2. Verify Nmap is installed and accessible
3. Ensure you have proper permissions
4. Open an issue on the repository

## Changelog

### Version 1.0.0
- Initial release with FastMCP implementation
- Support for all major Nmap scanning techniques
- Comprehensive error handling
- Stdio transport mode
- Type-safe tool definitions
- Claude Desktop configuration with uv
