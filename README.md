**auto-telnet.py**

**Description:**

"Autotelnet.py" is a simple Python program that allows users to automatically perform telnet to a specified host and port. The program prompts the user to enter a URL containing information about the target host and port for telnet. Valid URLs can be in the form of HTTP or HTTPS protocols and must contain host and port information. If the user-entered URL does not contain port information, the program will automatically add the default port 80.

The program then extracts the host and port information from the entered URL and generates a telnet command based on that information. The generated telnet command is displayed to the user on the screen.

Additionally, the program has an additional feature that will attempt to execute the telnet command and display the output. If the telnet command successfully connects to the target host and port, the program will display the message "Connected to [host]." However, if the telnet command fails to connect after waiting for 10 seconds, the program will display the message "Telnet connection failed."

**Requirements:**
- Python 3 installed on the system.

**How to Run:**
1. Open a terminal or command prompt.
2. Navigate to the directory where "auto-telnet.py" is located.
3. Run the following command:
   ```
   python3 auto-telnet.py
   ```
4. Enter the URL containing the host and port information when prompted.
5. The program will display the generated telnet command on the screen.
6. If the telnet command successfully connects, the message "Connected to [host]" will be displayed. If it fails to connect within 10 seconds, the message "Telnet connection failed" will be shown.

**Note:** Make sure to provide a valid URL containing correct host and port information for the program to function correctly.