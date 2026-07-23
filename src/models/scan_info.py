"""
scan_info.py

Represents scan information returned by the Camera Controller protocol.
"""


from dataclasses import dataclass


@dataclass
class ScanInfo:
    
    """Information about a scan returned by the protocol."""
    scan: str

    
    