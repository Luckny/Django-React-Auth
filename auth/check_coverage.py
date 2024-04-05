import subprocess


# Function to check coverage percentage
def check_coverage():
    try:
        # Run 'coverage report' command and capture output
        output = subprocess.check_output(["coverage", "report"])
        output_str = output.decode("utf-8")  # Convert bytes to string
        lines = output_str.split("\n")

        # Extract coverage percentage from the output
        coverage_percentage = float(lines[-2].split()[-1].strip("%"))

        # Check if coverage is 100%
        if coverage_percentage < 100.0:
            message = f"Code coverage is {coverage_percentage}%, not 100%"
            raise Exception(message)

    except Exception as e:
        print(f"Code coverage check failed: {e}")
        exit(1)


if __name__ == "__main__":
    check_coverage()
