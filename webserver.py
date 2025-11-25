#!/usr/bin/env python3
import http.server
import socketserver
import socket
import os
import sys
import logging
from pathlib import Path
import errno
import urllib.parse
from io import BytesIO
import subprocess
import re
import cgi       
import shutil    

# --- Configuration ---
DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0" 

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Helper Functions (get_local_ip, get_pid_using_port remain the same) ---

def get_local_ip():
    """Get the local non-loopback IP address of the machine for display."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_pid_using_port(port):
    """
    Attempts to find the PID of the process using the given port using OS-specific commands.
    Returns the PID (int) or None if not found.
    """
    pid = None
    port_str = str(port)

    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        command = ['lsof', '-t', '-i', f':{port_str}']
        try:
            output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
            if output:
                pid = int(output.decode().strip().splitlines()[0])
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
    elif sys.platform == 'win32':
        command = ['netstat', '-ano', '-p', 'TCP']
        try:
            output = subprocess.check_output(command).decode()
            regex = re.compile(r'TCP\s+\S+\:(' + re.escape(port_str) + r')\s+\S+\s+LISTENING\s+(\d+)', re.IGNORECASE)
            
            for line in output.splitlines():
                match = regex.search(line)
                if match:
                    pid = int(match.group(2))
                    break
        except subprocess.CalledProcessError:
            pass
    return pid

# ----------------------------------------------------
# NEW: Interactive Menu Function
# ----------------------------------------------------

def show_menu(initial_host, initial_port, initial_directory):
    """Presents an interactive menu for configuring the server."""
    current_host = initial_host
    current_port = initial_port
    current_directory = initial_directory
    
    while True:
        print("\n" + "="*50)
        print("🚀 Server Configuration Menu")
        print("="*50)
        print(f"1. Start Server (Host: {current_host}, Port: {current_port})")
        print(f"2. Change Port (Current: {current_port})")
        print(f"3. Change Directory (Current: {current_directory})")
        print("4. Exit Setup")
        print("="*50)
        
        choice = input("Enter your choice (1, 2, 3, or 4): ").strip()
        
        if choice == '1':
            # Start the server with current settings
            return current_host, current_port, current_directory
        
        elif choice == '2':
            new_port = input("Enter new port number (e.g., 8080): ").strip()
            try:
                new_port = int(new_port)
                if 1 <= new_port <= 65535:
                    current_port = new_port
                    logger.info(f"Port set to {new_port}")
                else:
                    print("Invalid port number. Must be between 1 and 65535.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == '3':
            new_dir = input("Enter new directory path (absolute or relative): ").strip()
            # Check if the directory exists and is accessible
            if os.path.isdir(new_dir):
                current_directory = os.path.abspath(new_dir)
                logger.info(f"Directory set to {current_directory}")
            else:
                print(f"Error: Directory not found or inaccessible: {new_dir}")
                
        elif choice == '4':
            logger.info("Exiting server setup as requested.")
            sys.exit(0)
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


# ----------------------------------------------------
# CustomHTTPRequestHandler (remains the same)
# ----------------------------------------------------

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def log_message(self, format, *args):
        logger.info(format % args)

    def do_POST(self):
        """Handle a POST request to allow file uploads."""
        current_path = self.translate_path(self.path)
        
        if not os.path.isdir(current_path) or not os.access(current_path, os.W_OK):
            self.send_error(403, "Forbidden: Cannot upload to this location.")
            return

        content_type = self.headers.get('Content-type', '').lower()
        if not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Bad Request: Only multipart/form-data uploads are supported.")
            return

        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
            
            if 'file' not in form:
                 self.send_error(400, "Bad Request: Missing 'file' field in form data.")
                 return
                 
            uploaded_file = form['file']
            
            if not hasattr(uploaded_file, 'file') or uploaded_file.file is None:
                self.send_error(400, "Bad Request: 'file' field content is not a file.")
                return

            if not uploaded_file.filename:
                self.send_error(400, "Bad Request: Filename is empty.")
                return

            filename = os.path.basename(uploaded_file.filename)
            destination = os.path.join(current_path, filename)
            
            with open(destination, 'wb') as out_file:
                shutil.copyfileobj(uploaded_file.file, out_file)
            
            logger.info(f"File uploaded successfully: {filename} to {self.path}")

            self.send_response(302)
            self.send_header("Location", self.path)
            self.end_headers()
            
        except Exception as e:
            logger.error(f"Upload processing error: {e}", exc_info=True) 
            self.send_error(500, "Error processing file upload. Check server logs for details.")


    def list_directory(self, path):
        """
        Overrides the default directory listing to add the upload form
        and target="_blank" to file links.
        """
        try:
            list_data = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        list_data.sort(key=lambda a: a.lower())

        r = []
        parent_url = urllib.parse.quote('..', errors='surrogatepass')
        
        displaypath = self.path
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE html>')
        r.append('<html lang="en">')
        r.append(f'<head><meta charset="{enc}"><title>{title}</title></head>')
        r.append(f'<body><h1>{title}</h1>')
        
        # --- File Upload Form ---
        r.append('<hr>')
        r.append('<h2>➕ Upload File</h2>')
        r.append(f'<form enctype="multipart/form-data" method="post" action="{urllib.parse.quote(self.path)}" target="_self">')
        r.append('<input type="file" name="file" required>')
        r.append('<input type="submit" value="Upload to Current Directory">')
        r.append('</form>')
        r.append('<hr>')
        # -----------------------------

        r.append('<ul style="list-style-type: none; padding: 0;">')
        
        r.append(f'<li><a href="{parent_url}" target="_self">⬆️ Parent Directory</a></li>')

        for name in list_data:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            
            if os.path.isdir(fullname):
                displayname += '/'
                linkname += '/'
            
            if os.path.islink(fullname):
                displayname += '@'

            quoted_linkname = urllib.parse.quote(linkname, errors='surrogateescape')

            r.append(f'<li><a href="{quoted_linkname}" target="_blank">{displayname}</a></li>')

        r.append('</ul>')
        r.append('<hr>')
        r.append(f'<p>Simple Python Web Server ({self.server_version}, {self.sys_version})</p>')
        r.append('</body></html>')
        
        encoded_content = '\n'.join(r).encode(enc, 'surrogateescape')
        
        f = BytesIO()
        f.write(encoded_content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded_content)))
        self.end_headers()
        return f


# ----------------------------------------------------
# Server Startup and Error Handling (remain the same)
# ----------------------------------------------------

def handle_startup_error(host, port, directory, e):
    """
    Handles the 'Address already in use' error (Errno 98 or 48) with interactive options,
    including automated kill of the conflicting process.
    """
    if e.errno in (errno.EADDRINUSE, 48): 
        print("\n" + "#"*60)
        logger.error(f"🔴 ERROR: Port {port} is already in use by another process.")
        print("#"*60 + "\n")
        
        while True:
            pid = get_pid_using_port(port)
            
            print("Please select an option:")
            print("1. **Try a different port** (e.g., 8080 or 9000)")
            
            if pid:
                print(f"2. **Force-stop** the running process (PID: {pid}) and restart.")
            else:
                print(f"2. **(Manual Kill)** Attempt automated kill or try again.")

            print("3. **Exit** the server setup.")
            
            choice = input("Enter your choice (1, 2, or 3): ").strip()
            
            if choice == '1':
                new_port = input("Enter a new port number (e.g., 8080): ").strip()
                try:
                    new_port = int(new_port)
                    if 1 <= new_port <= 65535 and new_port != port:
                        logger.info(f"Retrying server startup on new port: {new_port}")
                        # Pass back to start_server with new port
                        start_server(host, new_port, directory)
                        return
                    else:
                        print("Invalid port number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif choice == '2':
                if pid:
                    try:
                        logger.warning(f"Attempting to kill process PID {pid}...")
                        os.kill(pid, 9) 
                        print(f"Process {pid} terminated. Retrying startup...")
                        start_server(host, port, directory) 
                        return
                    except Exception as kill_e:
                        logger.error(f"Failed to kill process {pid} using `os.kill`: {kill_e}")
                        if sys.platform == 'win32':
                            try:
                                logger.warning(f"Attempting Windows kill command `taskkill /F /PID {pid}`...")
                                subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True, stdout=subprocess.DEVNULL)
                                print(f"Process {pid} terminated. Retrying startup...")
                                start_server(host, port, directory)
                                return
                            except Exception as taskkill_e:
                                logger.error(f"Failed to kill process {pid} using `taskkill`: {taskkill_e}")
                                print("Automated kill failed. Please try killing it manually or select option 1.")
                        else:
                            print("Automated kill failed. Please try killing it manually or select option 1.")
                else:
                    print("\n--- Manual Kill Recommended ---")
                    print(f"Could not find PID for port {port} automatically.")
                    print("Please try killing it manually or select option 1.")
                
            elif choice == '3':
                logger.info("Exiting server setup as requested.")
                sys.exit(0)
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    else:
        logger.error(f"\nError: A non-port related error occurred during startup.")
        logger.error(f"Details: {e}")
        sys.exit(1)


def start_server(host, port, directory):
    # 1. Change to the specified directory
    try:
        os.chdir(directory)
        cwd = os.getcwd() 
    except FileNotFoundError:
        logger.error(f"Error: Directory not found or inaccessible: {directory}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error changing directory to {directory}: {e}")
        sys.exit(1)

    # 2. Print server information
    local_ip = get_local_ip()
    hostname = socket.gethostname()

    print("\n" + "="*60)
    print("🌐 Python Web Server Started")
    print("="*60)
    print(f"📁 Serving files from: {cwd}")
    print(f"🖥️  Hostname: {hostname}")
    print(f"🔗 Binding Address: {host}")
    print(f"📍 Localhost: http://127.0.0.1:{port}")
    
    if host in ["0.0.0.0", local_ip]:
        print(f"🌍 Network Access: http://{local_ip}:{port}")
    
    print("="*60)
    logger.info(f"Serving HTTP on {host} port {port}...")
    print("Press Ctrl+C to stop the server\n")
    
    # 3. Start the server
    try:
        # ReusableTCPServer subclass to set SO_REUSEADDR
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
            
        with ReusableTCPServer((host, port), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except OSError as e:
        handle_startup_error(host, port, directory, e)
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
        sys.exit(0)

# ----------------------------------------------------
# Main Execution Block (Modified)
# ----------------------------------------------------

if __name__ == "__main__":
    
    # Start the interactive menu to get configuration
    final_host, final_port, final_directory = show_menu(
        DEFAULT_HOST, 
        DEFAULT_PORT, 
        os.getcwd()
    )
    
    # Start the server with the configuration selected by the user
    start_server(final_host, final_port, final_directory)
