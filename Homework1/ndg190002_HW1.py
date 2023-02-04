import sys
import re
import pickle


# Defining the employee class to hold each employee's name, id, and phone number
class Employee:
    def __init__(self, last, first, mi, eid, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = eid
        self.phone = phone

    def display(self):
        print("Name:", self.last, self.first, self.mi)
        print("ID:", self.id)
        print("Phone:", self.phone, "\n")


def process_file(employeeData):
    employees = {}
    with open(employeeData, 'r') as info:
        next(info)  # skipping the first line -> file header for each "column" of data
        # splitting each line from file on the delimiter "," and adding into an array "personData"
        for line in info:
            employeeInformation = line.strip().split(',')
            last = employeeInformation[0].capitalize()  # ensuring last name & first name are capitalized
            first = employeeInformation[1].capitalize()
            mi = employeeInformation[2].upper() if employeeInformation[2] else 'X'  # Adding in` a middle initial if none exists
            eid = employeeInformation[3]
            phone = employeeInformation[4]

            # check if id is in correct format
            if not re.match(r'[A-Za-z]{2}\d{4}', eid):
                print("Error: Invalid ID format", eid)
                # taking in user input to make sure a valid id is present
                eid = input("Enter a valid ID (2 letters and 4 digits):")
                while not re.match(r'[A-Za-z]{2}\d{4}', eid):
                    eid = input("Enter a valid ID (2 letters and 4 digits):")

            # check if phone number is in correct format
            if not re.match(r'\d{3}-\d{3}-\d{4}', phone):
                phone = re.sub(r'[^0-9]', '', phone)
                # fixing the formatting for phone number to get into ###-###-#### format
                phone = '-'.join([phone[i:i + 3] for i in range(0, len(phone), 3)])

            # check if id already exists
            if eid in employees:
                print("Error: Duplicate ID")
                continue

            employees[id] = Employee(last, first, mi, eid, phone)
    return employees


# Runs a check on the sys args to ensure that there was something being passed into the function
if len(sys.argv) < 2:
    print("Error: No file specified")
    sys.exit()

# define the passed sys arg as the file ot be read
data = sys.argv[1]
people = process_file(data)

# Dumping formatted data into the pickle file, serializing object into a byte stream
with open('persons.pkl', 'wb') as f:
    pickle.dump(people, f)

# Reading the pickle file by reading the byte stream and converting back into a byte stream
with open('persons.pkl', 'rb') as f:
    people = pickle.load(f)

# Displaying the reformatted data
for person in people.values():
    person.display()


def main(args):
    # Run check to see if a file was passed using sys args
    if len(args) < 2:
        print("Error: Please specify a file path.")
