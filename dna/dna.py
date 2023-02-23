import csv
import sys


def main():

    # TODO: Check for command-line usage
    if (len(sys.argv) != 3):
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
    
    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as textfile:
        sequence = textfile.read()
     
    # TODO: Find longest match of each STR in DNA sequence
    count = 1
    # Declare the STR counts list
    str_no = []
    # Loop through each STR
    for column in database[1]:
        if (count == 1):
            count += 1
            continue
        str_no.append(longest_match(sequence, column))
        count += 1
    # Check for DNA match
    l = len(str_no)
    seen = False
    for row in database:  
        i = 1
        c = 0
        for column in row:
            if (i == 1):
                i += 1
                continue
            i += 1
            for data_item in str_no:
                if data_item == int(row[column]):
                    c += 1
                    if c == l:
                        print(row["name"])
                        seen = True
    if seen == False:
        print("No match")
                

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
