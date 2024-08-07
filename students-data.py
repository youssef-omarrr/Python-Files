students = list() #global variable that contains all our data

def help():
    print("The term should be in range of 1:10 as int")
    print("The GPA should be in range of 0:4 as float")
    print("The ID should be in range of 1000:10000 as int")
    print("------------------------------------------------")

def add_data(): #fn to add data to the original list
    global students
    while True:
        print("Enter the data with this formla:")
        data = input("FIRST name LAST name TERM GPA ID \nIf you want to exit type 'done'.\n").lower()
        if (data == 'done'):
            break
        students.append(data)
        print("----------------------------------")

def split (): #a funcion that splits the data to individual arrays
    words = []
    for phr in students:
        words.append(phr.split())
    return words

def joined(words):
    temp = list()
    for wrd in words:
        temp.append(' '.join(wrd))
    return (temp)
    
def search(opt2): #a fn to search for specific data
    words = split()
    if (opt2 == 1):
            fname = input("Enter the FIRST name you want to search for: \n")
            for i in range (len(students)):
                if fname ==  words[i][0]:
                    print (fname, "is found.")
                    break
            else:
                print(fname, "is NOT found!")

    elif (opt2 == 2):
            fname = input("Enter the LAST name you want to search for: \n")
            for i in range (len(students)):
                if fname ==  words [i][1]:
                    print (fname, "is found.")
                    break
            else:
                print(fname, "is NOT found!")

    elif (opt2 == 3):
        term = input("Enter the term you want to search for: \n")
        if (0 < int(term) <= 10):
            for i in range (len(students)):
                if term == int(words [i][2]):
                    print (term, "is found")
                    break
            else:
                print(term,"NOT found")
        else:
            print ("Wrong input!")

    elif (opt2 == 4):
        gpa = input("Enter the GPA you want to search for: \n")
        if (0 <= float(gpa) <= 4):
            for i in range (len(students)):
                if gpa == float(words [i][3]):
                    print (gpa, "is found")
                    break
            else:
                print(gpa,"NOT found")
        else:
            print ("Wrong input!")

    elif (opt2 == 5):
        id = input("Enter the ID you want to search for: \n")
        if (1000 <= int(id) <= 10000):
            for i in range (len(students)):
                if id == int(words [i][4]):
                    print (id, "is found")
                    break
            else:
                print(id,"NOT found")
        else:
            print ("Wrong input!")
    else: 
        print("Wrong input!")

def remove(opt3): #function to remove data by a certain index
    global students
    words = split()
    if (opt3 == 1):
            fname = input("Enter the FIRST name you want to remove: \n")
            for i in range (len(students)):
                if fname ==  words[i][0]:
                    del (students[i])
                    break
            else:
                print(fname, "is NOT found!")

    elif (opt3 == 2):
            fname = input("Enter the LAST name you want to remove: \n")
            for i in range (len(students)):
                if fname ==  words [i][1]:
                    del (students[i])
                    break
            else:
                print(fname, "is NOT found!")

    elif (opt3 == 3):
        term = input("Enter the term you want to remove: \n")
        if (0 < int(term) <= 10):
            for i in range (len(students)):
                if term == int(words [i][2]):
                    del (students[i])
                    break
            else:
                print(term,"NOT found")
        else:
            print ("Wrong input!")

    elif (opt3 == 4):
        gpa = input("Enter the GPA you want to remove: \n")
        if (0 <= float(gpa) <= 4):
            for i in range (len(students)):
                if gpa == float(words [i][3]):
                    del (students[i])
                    break
            else:
                print(gpa,"NOT found")
        else:
            print ("Wrong input!")

    elif (opt3 == 5):
        id = input("Enter the ID you want to remove: \n")
        if (1000 <= int(id) <= 10000):
            for i in range (len(students)):
                if id == int(words [i][4]):
                    del (students[i])
                    break
            else:
                print(id,"NOT found")
        else:
            print ("Wrong input!")
    else: 
        print("Wrong input!")

def edit(opt4, id): # a fn to edit certain data
    global students
    words = split()
    j = 0
    if (1000 <= id <= 10000):
            for i in range (len(students)):
                if id == int(words [i][4]):
                    break
                else:
                    j += 1
            else:
                print(id,"NOT found")
                return 0
    else:
        print("Wrond input!")
        return 0
            
    if (opt4 == 1):
            new = input("Enter the new First name: \n")
            words [j][0] = new

    elif (opt4 == 2):
            new = input("Enter the new LAST name: \n")
            words [j][1] = new

    elif (opt4 == 3):
        new = input("Enter the new term: \n")
        if (0 < int(new) <= 10):
            words [j][2] = new
        else:
            print ("Wrong input!")

    elif (opt4 == 4):
        new = input("Enter the new GPA: \n")
        if (0 <= float(new) <= 4):
            words [j][3] = new
        else:
            print ("Wrong input!")

    elif (opt4 == 5):
        new = input("Enter the new ID: \n")
        if (1000 <= int(new) <= 10000):
            words [j][4] = new
            
        else:
            print ("Wrong input!")
    else: 
        print("Wrong input!")

    students = joined(words)

while True:
    opt1 = input("1- Enter new student. \n2- Print all. \n3- Search. \n4- Remove. \n5- Update data. \n6- Sort.\nType 'done' to exit or type 'help' to get insturctions.\n").lower()
    print("----------------------------------")
    if (opt1 == 'done'): #done to quit
        break

    elif (opt1 == 'help'): #help for instructions
        help()

    elif (opt1 == '1'): #adds new data
        add_data()

    elif (opt1 == '2'): #prints the data
        for i in range (len(students)):
            print(f"Sudent number {i+1}'s data is {students[i]}")
        print("----------------------------------")

    elif (opt1 == '3'): #searches for a certain data 
        print("Choose what data you want to search for:")
        opt2 = int(input("1- First name. \n2- Last name. \n3- Term. \n4- GPA. \n5-ID \n"))
        search(opt2)
        print("----------------------------------")

    elif (opt1 == '4'): #removes data
        print("Choose how you want to remove the data by:")
        opt3 = int(input("1- First name. \n2- Last name. \n3- Term. \n4- GPA. \n5-ID \n"))
        remove (opt3)
        print("----------------------------------")

    elif (opt1 == '5'): #updates data
        id = int(input("Enter the ID of the student you want to edit his data: \n"))
        print("Choose what data you want to edit:")
        opt4 = int(input("1- First name. \n2- Last name. \n3- Term. \n4- GPA. \n5-ID \n"))
        edit(opt4, id)
        print("----------------------------------")

    elif (opt1 == '6'):
        opt3 = int(input("1- Sorted ascendingly. \n2- Sorted descendingly. \n"))
        if (opt3 == 1):
            students = sorted(students)
        elif (opt3 == 2):
            students = sorted(students, reverse = True)
        else: 
            print("Wrong input!")
    else:
        print ("Wrong input please try again!")
