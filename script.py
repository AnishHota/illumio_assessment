# Importing libaries
import csv
import os
import argparse
from collections import defaultdict

# Data path: Pass the data path as a command line argument when running the script
# Default data path is set to 'data' if no argument is provided
parser = argparse.ArgumentParser()
parser.add_argument(
    '--data_path', 
    type=str, 
    default='data',  # Default value
    help='The path to the data directory'
)
args = parser.parse_args()
data_path = args.data_path

# Load the flow log file
def load_log_list(log_file):
    log = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip().split()
            log.append(line)
    return log

# Load the lookup file
def load_lookup(lookup_file):
    lookup = {}
    with open(lookup_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for port, pro, tag in reader:
            lookup[f"{port}_{pro}"] = tag
    return lookup

# Load the protocol numbers file
def protocol_numbers_conversion(protocol_numbers):
    protocol_dict ={}
    with open(protocol_numbers,'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        protocol_dict = {rows[0]:rows[1] for rows in reader}
    return protocol_dict

# Function to count the frequency of each tag and each port-protocol combination.
def tag_protocol_counts(flow_log, lookup, protocol_dict):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    port_protocol_output = []

    # for every log record in the flow log file
    for log_record in flow_log:

        # Dstport and protocol from the protocol number is extracted.
        dstport = log_record[6]
        protocol_num = log_record[7]
        protocol = protocol_dict[protocol_num].lower()
        key = f"{dstport}_{protocol}"

        # Combination of dstport and protocol is used for counting the frequency.
        port_protocol_counts[key] += 1

        # Tag is extracted from the lookup file and the frequency is counted. If the lookup_file
        # doesn't contain the combination of dstport and protocol, it is tagged as "Untagged".
        if key in lookup_file:
            tag_counts[lookup_file[key]] += 1
        else:
            tag_counts["Untagged"] +=1

    # The port_protocol_counts dictionary is converted to a list of lists for easy writing to a CSV file.
    # The key is split into port and protocol and the count is appended to the list.
    for key,value in port_protocol_counts.items():
        port,protocol = key.split("_")
        port_protocol_output.append([int(port),protocol,value])
    
    return tag_counts, port_protocol_output

# Function to write the output to a file
def data_to_output(filename,tag_output,port_protocol_output):
    with open(filename, 'w') as file:
        # 1st file: Tags and their counts
        file.write("Tag Counts: \n")
        file.write("Tag,Count\n")

        # Write the data rows
        for tag, count in tag_output.items():
            file.write(f"{tag},{count}\n")
        
        file.write("\n")

        #2nd file: Port, Protocol and their counts
        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        # Write the data rows
        for row in port_protocol_output:
            file.write(",".join(map(str, row)) + "\n")

if __name__ == "__main__":

    # Paths to the data files
    log_file_path = os.path.join(data_path, "flow_log.txt")
    lookup_file_path = os.path.join(data_path, "lookup.csv")
    protocol_numbers_file = os.path.join(data_path,"protocol-numbers.csv")

    # Loading the 3 files: flow_log, lookup and protocol_numbers
    flow_log = load_log_list(log_file_path)
    lookup_file = load_lookup(lookup_file_path)
    protocol_dict = protocol_numbers_conversion(protocol_numbers_file)

    # Counting the frequency of tags and port/protocol combinations
    tag_counts, port_protocol_output = tag_protocol_counts(flow_log, lookup_file, protocol_dict)

    # Writing the output to a file
    data_to_output("output.txt",tag_counts,port_protocol_output)

