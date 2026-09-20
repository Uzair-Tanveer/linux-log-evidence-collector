from pathlib import Path
# Helps script work with file paths 

from datetime import datetime
# lets script create a timestamp

import socket
import re

LOG_FILE = "/var/log/auth.log"
# Lets the script know which log file to read

REPORTS_DIR = Path("reports")
# Sets the folder where the reports will be saved


def get_local_ip():
	"""Get the IP address of the current machine."""
	try:
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		return ip_address
	except socket.gaierror:
		return "Unable to determine local IP"

def extract_source_ip(line):
	"""Extract an IP address from a log line if one exists."""
	match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', line)
	if match:
		return match.group(1)
	return None

def main():
	results = []
	source_ips = set()
# creates a collection of unique IP addresses found in failed login entries. 

	failed_login_count = 0
# starts the counter at 0 

	try:
		with open(LOG_FILE, "r") as file:
			lines = file.readlines()
# opens the file for reading
# file.readlines() reads all the lines from the file

	except FileNotFoundError:
		print(f"Log File not Found: {LOG_FILE}")
		return
	except PermissionError:
		print(f"Permission denied reading: {LOG_FILE}")
		return
	for line in lines:
		if "Failed password" in line or "authentication failure" in line:
#Checks for failed login text in the log 

			failed_login_count += 1
			results.append(line.strip())

			ip = extract_source_ip(line)
			if ip:
				source_ips.add(ip)

	timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	REPORTS_DIR.mkdir(exist_ok=True)
	report_path = REPORTS_DIR / f"auth_log_report_{timestamp}.txt"

	local_ip = get_local_ip()
# Captures the IP address of the machine running the script

	with open(report_path, "w") as report:
		report.write("Linux Log Review / Evidence Collection Report\n")
		report.write(f"Generated: {datetime.now()}\n")
		report.write(f"Log file reviewed: {LOG_FILE}\n")
		report.write(f"Local Machine IP: {local_ip}\n")
		report.write(f"Failed Login attempts found: {failed_login_count}\n\n")

		report.write("Source IPs found in failed login entries:\n")
		report.write("-" * 60 + "\n")
		if source_ips:
			for ip in sorted(source_ips):
				report.write(ip + "\n")
		else:
			report.write("No Source IP found in the review entries.\n")

		report.write("\nMatching log entries:\n")
		report.write ("-" * 60 + "\n")
		for item in results:
			report.write(item + "\n")

	print("Log Review Completed.")
	print(f"Local Machine IP: {local_ip}")
	print(f"Failed login attempts found: {failed_login_count}")
	print(f"Report saved to: {report_path}")

if __name__ == "__main__":
	main()
