import base64
import socket

def ip_to_code(ip):
    try:
        parts = ip.split('.')
        if len(parts) != 4: return "INVALID"
        
        ip_bytes = bytes([int(p) for p in parts])
        code = base64.b64encode(ip_bytes).decode('utf-8') # Convert IP bytes to Base64 text
        code = code.replace('=', '').replace('+', '-').replace('/', '_') # Sanitize for URL safety
        return code
    except:
        return "ERROR"

def code_to_ip(code):
    try:
        code += '=' * (4 - len(code) % 4)
        code = code.replace('-', '+').replace('_', '/') # Revert sanitation
        ip_bytes = base64.b64decode(code) # Convert Base64 text back to IP bytes
        if len(ip_bytes) != 4:
            return None
        return '.'.join(str(b) for b in ip_bytes)
    except:
        return None

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
