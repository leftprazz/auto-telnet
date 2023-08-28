**AutoTelnet**

This project consists of two Python programs: `autotelnet.py` and `autotelnet-v2.py`. The former is the initial version that lacks the capability to display endpoint details and method response, while the latter, `autotelnet-v2.py`, includes these additional features.

**Description:**

`autotelnet.py` is a simple Python script designed to automate telnet connections to specified hosts and ports. The program prompts users to provide a URL containing information about the target host and port for telnet. Valid URLs can utilize either the HTTP or HTTPS protocols and should contain the host and port information. If the URL entered by the user lacks port information, the program will automatically use the default port, which is 80.

The program then extracts the host and port information from the URL and generates a telnet command based on these details. The generated telnet command is displayed to the user on the terminal.

However, `autotelnet-v2.py` goes a step further. In addition to the capabilities of the original version, it includes the ability to display endpoint details and the response from the HTTP method. When executed, the program prompts users to input a URL as before. It then separates the host and port from the URL and generates a telnet command. Afterward, it initiates the telnet command and displays the output, providing insight into the connection status. Following the telnet step, the program utilizes the `requests` module to send an HTTP request to the specified endpoint and prints the response details, including the HTTP status code and response content.

**Requirements:**
- Python 3 installed on your system.
- `requests` module for the second version (`autotelnet-v2.py`).

**How to Run:**

For `autotelnet.py`:
1. Open a terminal or command prompt.
2. Navigate to the directory where `autotelnet.py` is located.
3. Run the following command:
   ```
   python3 autotelnet.py
   ```
4. Input the URL containing the host and port information when prompted.
5. The program will display the generated telnet command on the terminal.
6. If the telnet command successfully connects, it will show "Connected to [host]." If it fails to connect within 10 seconds, it will display "Telnet connection failed."

For `autotelnet-v2.py`:
1. Open a terminal or command prompt.
2. Navigate to the directory where `autotelnet-v2.py` is located.
3. Run the following command:
   ```
   python3 autotelnet-v2.py
   ```
4. Input the URL containing the host and port information when prompted.
5. The program will display the generated telnet command on the terminal.
6. If the telnet command successfully connects, it will show "Connected to [host]." If it fails to connect within 10 seconds, it will display "Telnet connection failed."
7. The program will then proceed to send an HTTP request to the specified endpoint and display the HTTP status code and response content.

**Note:** Ensure you provide a valid URL containing accurate host and port details for proper functionality of both versions. The second version, `autotelnet-v2.py`, requires the `requests` module.