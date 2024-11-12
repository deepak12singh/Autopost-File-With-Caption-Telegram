import sys

def process_bar(nowwork, total, bar_length=100):
    # Calculate the percentage of completion
    percent = float(nowwork) / total
    # Calculate the number of hash marks to show
    hashes = '#' * int(percent * bar_length)
    # Calculate the remaining space in the progress bar
    spaces = ' ' * (bar_length - len(hashes))

    # Format the progress bar string
    sys.stdout.write(f"\rProgress: [{hashes}{spaces}] {percent * 100:.2f}%")
    sys.stdout.flush()

    # Print a new line when the process is complete
    if nowwork == total:
        sys.stdout.write('\n')

# # Example usage
# import time

# total_work = 120
# for i in range(total_work + 1):
#     process_bar(i, total_work)
#     time.sleep(0.1)
