import csv
import os
from collections import defaultdict

data_path = "data" #Change the path to the directory where the data files are located

def load_log_list(log_file):
    log = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip().split()
            log.append(line)
    return log

def load_lookup(lookup_file):
    lookup = {}
    with open(lookup_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for port, pro, tag in reader:
            lookup[f"{port}_{pro}"] = tag
    return lookup

def protocol_numbers_conversion(protocol_numbers):
    protocol_dict ={}
    with open(protocol_numbers,'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        protocol_dict = {rows[0]:rows[1] for rows in reader}
    return protocol_dict


def tag_protocol_counts(flow_log, lookup, protocol_dict):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    port_protocol_output = []
    for log_record in flow_log:
        dstport = log_record[6]
        protocol_num = log_record[7]
        protocol = protocol_dict[protocol_num].lower()
        key = f"{dstport}_{protocol}"
        port_protocol_counts[key] += 1
        if key in lookup_file:
            tag_counts[lookup_file[key]] += 1
        else:
            tag_counts["Untagged"] +=1

    for key,value in port_protocol_counts.items():
        port,protocol = key.split("_")
        port_protocol_output.append([int(port),protocol,value])
    
    return tag_counts, port_protocol_output


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
    log_file_path = os.path.join(data_path, "flow_log.txt")
    lookup_file_path = os.path.join(data_path, "lookup.csv")
    protocol_numbers_file = os.path.join(data_path,"protocol-numbers.csv")

    flow_log = load_log_list(log_file_path)
    lookup_file = load_lookup(lookup_file_path)
    protocol_dict = protocol_numbers_conversion(protocol_numbers_file)

    tag_counts, port_protocol_output = tag_protocol_counts(flow_log, lookup_file, protocol_dict)

    data_to_output("output.txt",tag_counts,port_protocol_output)

