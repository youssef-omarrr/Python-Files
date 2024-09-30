def add_data(): #func to add data to txt file
    data = open("students.txt", 'a')
    while True:
        print("Enter the data with this formla:")
        x = input("FIRST name LAST name TERM GPA ID \nIf you want to exit type 'done'.\n").lower()
        
        if (len(x.split()) != 5):
            print("Wrong input")
            break
        if (x == 'done'):
            data.close()
            break
        data.write(x+'\n')
        print("Data added successfully.")
        print("--------------------------------------------------")

def print_data(): #prints all data
    data = open("students.txt", 'r')
    y= data.read().strip().split('\n')
    print(y)
    data.close()

def search_data(reg): #searchs for student using reg number
    test = 0
    data = open("students.txt", 'r')
    y = data.read().strip().split('\n')
    for i in range (len(y)):
        if (reg == (y[i].split())[4]):
            test = 1
            data.close()
            return test, y[i]
        
    data.close()

def remove_data(reg, add=0, up='none'): #removes a certain line
    test, y = search_data(reg)
    if test == 1:
        with open ("students.txt", 'r') as fread: #reads all lines
            lines = fread.readlines()

            with open("students.txt", 'w') as fwrite: #over-writes all file but a specfic line
                for line in lines: #reads line by line
                    if line.strip('\n') != y: 
                        fwrite.write(line)
                    elif add == 1: #if we want to update data not remove it
                        fwrite.write(up)
        if add == 1: #returns to update function to know if we updated the data or not
            return 1
        
        print(f"{reg} deleted successfully.")
    else:
        print(f"{reg} not found")

def update_data(reg): #updates a certain students data
    test, y = search_data(reg)
    if test == 1:
        y = input("Please enter the new data in the same format as before: \n")
        x = remove_data(reg, 1, y) #instead of writing the remove code again
        if x == 1:
            print(f"{reg} updated successfully.")
    else:
        print(f"{reg} not found")

def sort_data(opt2):
    data = open("students.txt", 'r')
    y = data.read().strip().split('\n')
    data.close()

    if (opt2 == 1):
        y = sorted(y)
        data = open("students.txt", 'w')
        for x in y:
            data.write(str(x)+'\n') #line by line
        data.close()
        print("Sorted successfully.")
        
    elif (opt2 == 2):
        y = sorted(y, reverse= True)
        data = open("students.txt", 'w')
        for x in y:
            data.write(str(x)+'\n') #line by line
        data.close()
        print("Sorted successfully.")

    else:
        print("Wrong input")


######################### MAIN ###########################
while True:
    opt = input("1- Enter new student. \n2- Print all. \n3- Search. \n4- Remove. \n5- Update data. \n6- Sort.\nType 'done' to exit.\nEnter your choise: ").lower()
    if (opt == 'done'):
        break

    elif (opt == 'help'):
        help()

    elif (opt == '1'):
        add_data()

    elif (opt == '2'):
        print_data()

    elif (opt == '3'):
        reg = input("Please enter the registeration number of the student you want to search for: \n")
        test, y = search_data(reg)
        if test == 1:
            print (f"{reg} found")
            print (y)
        else:
            print(f"{reg} not found")
        print("------------------------------------------------")

    elif (opt == '4'):
        reg = input("Please enter the registeration number of the student you want to remove: \n")
        remove_data(reg)
        print("------------------------------------------------")

    elif (opt == '5'):
        reg = input("Please enter the registeration number of the student you want to update his/her data: \n")
        update_data(reg)
        print("------------------------------------------------")
    
    elif (opt == '6'):
        opt2 = int(input("1- Sorted ascendingly. \n2- Sorted descendingly. \n"))
        sort_data(opt2)
        print("------------------------------------------------")



