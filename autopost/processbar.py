import sys

def process_bar(nowwork, total, bar_length=100,folder_name = 'Progress',symbol = '#'):
    # Calculate the percentage of completion
    percent = float(nowwork) / total
    # Calculate the number of hash marks to show
    hashes = symbol * int(percent * bar_length)
    # Calculate the remaining space in the progress bar
    spaces = ' ' * (bar_length - len(hashes))
    name = folder_name+" "*(30-len(folder_name))

    # Format the progress bar string
    sys.stdout.write(f"\r{name}: [{hashes}{spaces}] {percent * 100:.2f}%    {nowwork}\\{total}")
    sys.stdout.flush()

    # Print a new line when the process is complete
    if nowwork == total:
        sys.stdout.write('\n')

