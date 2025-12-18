#!/usr/bin/env python3
"""
Nmap MCP Server

This server exposes Nmap CLI functionality as MCP tools using FastMCP.
It provides comprehensive network scanning capabilities through the Nmap command-line tool.
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from mcp.server import FastMCP
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    LoggingMessageNotification,
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server
app = FastMCP("nmap-mcp-server")

def run_nmap_command(args: List[str], timeout: int = 300) -> Dict[str, Any]:
    """
    Execute an nmap command and return the results.
    
    Args:
        args: List of nmap command arguments
        timeout: Command timeout in seconds
    
    Returns:
        Dictionary containing command output, error, and exit code
    """
    try:
        # Construct the full nmap command
        cmd = ["nmap"] + args
        
        logger.info(f"Executing nmap command: {' '.join(cmd)}")
        
        # Run the command with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "success": result.returncode == 0
        }
        
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "exit_code": -1,
            "success": False
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": "nmap command not found . Please ensure nmap is installed and in PATH",
            "exit_code": -1,
            "success": False
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing nmap command: {str(e)}",
            "exit_code": -1,
            "success": False
        }

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
    args = ["-p", ports]
    
    if scan_type == "quick":
        args.extend(["-T4", "--min-rate=1000"])
    elif scan_type == "comprehensive":
        args.extend(["-sS", "-sV", "-O", "--script=default"])
    elif scan_type == "stealth":
        args.extend(["-sS", "-T2", "--min-rate=100"])
    
    args.append(targets)
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Basic scan completed successfully:\n\n{result['stdout']}"
    else:
        return f"Basic scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_service_detection",
    description="Perform service and version detection scan"
)
async def nmap_service_detection(
    targets: str,
    ports: str = "common",
    intensity: int = 7
) -> str:
    """Perform service and version detection scan."""
    args = ["-sV", f"--version-intensity={intensity}", "-p", ports, targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Service detection scan completed:\n\n{result['stdout']}"
    else:
        return f"Service detection scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_os_detection",
    description="Perform operating system detection scan"
)
async def nmap_os_detection(
    targets: str,
    ports: str = "common",
    max_retries: int = 2
) -> str:
    """Perform operating system detection scan."""
    args = ["-O", f"--osscan-retries={max_retries}", "-p", ports, targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"OS detection scan completed:\n\n{result['stdout']}"
    else:
        return f"OS detection scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_script_scan",
    description="Run NSE (Nmap Scripting Engine) scripts"
)
async def nmap_script_scan(
    targets: str,
    scripts: str = "default",
    ports: str = "common"
) -> str:
    """Run NSE (Nmap Scripting Engine) scripts."""
    args = [f"--script={scripts}", "-p", ports, targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"NSE script scan completed:\n\n{result['stdout']}"
    else:
        return f"NSE script scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_stealth_scan",
    description="Perform stealth scan (SYN scan) with minimal detection"
)
async def nmap_stealth_scan(
    targets: str,
    ports: str = "common",
    timing: int = 3
) -> str:
    """Perform stealth scan (SYN scan) with minimal detection."""
    args = ["-sS", f"-T{timing}", "-p", ports, targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Stealth scan completed:\n\n{result['stdout']}"
    else:
        return f"Stealth scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_comprehensive_scan",
    description="Perform comprehensive scan with all detection methods"
)
async def nmap_comprehensive_scan(
    targets: str,
    ports: str = "all",
    include_scripts: bool = True
) -> str:
    """Perform comprehensive scan with all detection methods."""
    args = ["-sS", "-sV", "-O", "-p", ports]
    
    if include_scripts:
        args.append("--script=default")
    
    args.append(targets)
    
    result = run_nmap_command(args, timeout=600)  # Longer timeout for comprehensive scan
    
    if result["success"]:
        return f"Comprehensive scan completed:\n\n{result['stdout']}"
    else:
        return f"Comprehensive scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_ping_scan",
    description="Perform ping scan to discover live hosts"
)
async def nmap_ping_scan(
    targets: str,
    ping_type: str = "both"
) -> str:
    """Perform ping scan to discover live hosts."""
    if ping_type == "icmp":
        args = ["-sn", targets]
    elif ping_type == "tcp":
        args = ["-PS", targets]
    else:  # both
        args = ["-sn", "-PS", targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Ping scan completed:\n\n{result['stdout']}"
    else:
        return f"Ping scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_port_scan",
    description="Scan specific ports on target hosts"
)
async def nmap_port_scan(
    targets: str,
    ports: str,
    scan_method: str = "syn"
) -> str:
    """Scan specific ports on target hosts."""
    if scan_method == "syn":
        args = ["-sS", "-p", ports, targets]
    elif scan_method == "connect":
        args = ["-sT", "-p", ports, targets]
    else:  # udp
        args = ["-sU", "-p", ports, targets]
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Port scan completed:\n\n{result['stdout']}"
    else:
        return f"Port scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_vulnerability_scan",
    description="Run vulnerability detection scripts"
)
async def nmap_vulnerability_scan(
    targets: str,
    ports: str = "common",
    vuln_category: str = "all"
) -> str:
    """Run vulnerability detection scripts."""
    if vuln_category == "all":
        scripts = "vuln"
    else:
        scripts = f"vuln and {vuln_category}"
    
    args = [f"--script={scripts}", "-p", ports, targets]
    
    result = run_nmap_command(args, timeout=600)
    
    if result["success"]:
        return f"Vulnerability scan completed:\n\n{result['stdout']}"
    else:
        return f"Vulnerability scan failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_network_discovery",
    description="Discover hosts and services on a network"
)
async def nmap_network_discovery(
    network: str,
    discovery_method: str = "all",
    include_ports: bool = True
) -> str:
    """Discover hosts and services on a network."""
    if discovery_method == "ping":
        args = ["-sn", network]
    elif discovery_method == "arp":
        args = ["-PR", network]
    elif discovery_method == "syn":
        args = ["-PS", network]
    else:  # all
        args = ["-sn", "-PS", "-PA", network]
    
    if include_ports:
        args.extend(["-sS", "-sV", "--top-ports=100"])
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Network discovery completed:\n\n{result['stdout']}"
    else:
        return f"Network discovery failed:\n\n{result['stderr']}"

@app.tool(
    name="nmap_custom_scan",
    description="Perform custom Nmap scan with user-defined options"
)
async def nmap_custom_scan(
    targets: str,
    custom_options: str,
    output_format: str = "normal"
) -> str:
    """Perform custom Nmap scan with user-defined options."""
    # Parse custom options
    args = custom_options.split()
    
    # Add output format if specified
    if output_format == "xml":
        args.append("-oX")
        args.append("-")
    elif output_format == "grepable":
        args.append("-oG")
        args.append("-")
    
    args.append(targets)
    
    result = run_nmap_command(args)
    
    if result["success"]:
        return f"Custom scan completed:\n\n{result['stdout']}"
    else:
        return f"Custom scan failed:\n\n{result['stderr']}"

async def main():
    """Main function to run the FastMCP server with stdio transport."""
    # Run the FastMCP server with stdio transport
    await app.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
