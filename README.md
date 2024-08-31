# illumio Assessment
Take home assessment for illumio

## Project Overview

This project provides a program that parses flow log data and maps each row to a tag based on a predefined lookup table. The program is designed to process network flow logs and categorize them according to destination port and protocol combinations.

## Features

- Parses flow log data from a file
- Uses a CSV lookup table to map port/protocol combinations to tags
- Generates an output file with:
  - Count of matches for each tag
  - Count of matches for each port/protocol combination

## Input Data

### Flow Logs

The program accepts flow log data in the following format (Version 2):

```
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
```

Each line represents a single flow log entry. The fields are separated by spaces. The 6th field represents the destination port, and the 7th field represents the protocol number.All the fields and their description can be found [here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html). The program uses these fields to determine the tag for each flow log entry.

Assumptions: The flow log file uses the same format and is restricted to the version 2. The program assumes that the flow log file is well-formed and does not contain any errors or inconsistencies. The program does not perform any validation on the input data.

### Lookup Table

The lookup table is a CSV file with the following structure:

```csv
dstport,protocol,tag
25,tcp,sv_P1
68,udp,sv_P2
23,tcp,sv_P1
...
```
Assumptions: The lookup table file is a CSV file and uses the same formatting and structure as described above. The program assumes that the lookup table file is well-formed and does not contain any errors or inconsistencies. The program does not perform any validation on the input data.

### Protocol Numbers 
The protocol numbers is a static CSV file obtained from the following link:
https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

The file structure is as follows:

```csv
Decimal,Keyword,Protocol,IPv6 Extension Header,Reference
0,HOPOPT,IPv6 Hop-by-Hop Option,Y,[RFC8200]
1,ICMP,Internet Control Message,,[RFC792]
2,IGMP,Internet Group Management,,[RFC1112]
...
```

The decimal and keyword  columns are used to map the protocol numbers obtained from the flow logs to the protocol names.

Assumptions: The protocol numbers file is present in the data directory and the above script doesn't download the above csv file. Although, the script can be modified to check whether the csv file is present or not, and can download if it's not present in the data directory.

## Output

The program generates an output file containing 1.Count of matches for each tag: and 2. Count of matches for each port/protocol combination. The output file is a txt file with the following structure:
  
   ```
   Tag Counts:
   Tag,Count
   sv_P2,1
   sv_P1,2
   sv_P4,1
   email,3
   Untagged,9

   Port/Protocol Combination Counts:
   Port,Protocol,Count
   22,tcp,1
   23,tcp,1
   25,tcp,1
   ```

## Requirements

- Python 3.11 or higher
- pipenv

## Installation

1. Clone the repository:
   ```
   git https://github.com/AnishHota/illumio_assessment.git
   cd illumio_assessment
   ```

2. Install pipenv if you haven't already:
   ```
   pip install pipenv
   ```

3. Install the project dependencies:
   ```
   pipenv install
   ```

   This will create a virtual environment and install all necessary dependencies based on the Pipfile and Pipfile.lock.

## Usage

1. Activate the virtual environment:
   ```
   pipenv shell
   ```

2. Place the flow_log files and lookup.csv in a directory of the project. The flow_log file, lookup.csv file, protocol_numbers.csv file should be in the format described above. The protocol_numbers.csv file is already present in the data directory.

3. Run the program:
   ```
   python script.py --data_path=data
   ```
   
   Default data_path is "data". If you want to change the data_path, you can use the --data_path flag to specify the path to the data directory.
   notebook.ipynb contains the early development of the script. The final script is present in the script.py file.

4. View the results in the output file:
   ```
   cat output.txt
   ```

## Future work
This could be implemented as a future work to make the script more robust and efficient. 
- The script can be modified to handle large flow log files by using a streaming approach to process the data in chunks rather than loading the entire file into memory. This would allow the script to handle flow log files of any size, regardless of the available system resources. 
- Additionally, the script can be modified to support other formats for the flow log files and lookup table, such as JSON or XML. This would allow the script to be used with a wider range of data sources and tools.
- The script can contain unit tests to ensure that the functions are working as expected. This would help to catch any errors or bugs in the code and ensure that the script is producing accurate results.
- The script can also validate the formatting and structure of the input data to ensure that it is well-formed and does not contain any errors or inconsistencies. This would help to prevent any errors or issues from occurring during the processing of the data.
- The lookup table can be loaded into a sql database and can be queried using sql queries. This would allow the script to be more efficient and scalable, and would allow the lookup table to be updated or modified without having to modify the script itself.
