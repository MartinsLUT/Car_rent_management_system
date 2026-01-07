from datetime import datetime
import string

def menu():
    print("\nSelect one of the following oporetions:\n1) List of available cars\n2) Rent a car\n3) Return the car\n4) Count the money\n0) Exit")
    return input("Select the function (0-4):\n")
def list_available_cars():
    file = open("vehicles.txt", 'r', encoding="utf-8")
    rented_vehicle = open("rentedVehicles.txt", 'r', encoding="utf-8")
    rented_cars = []
    for line1 in rented_vehicle:
            rented = line1.strip()
            auto_rented = rented.split(',')
            rented_cars.append(auto_rented[0])
    for line in file:
        vehicle = line.strip()
        auto = vehicle.split(',')
        if auto[0] not in rented_cars:
            print(f"* Reg.nr: {auto[0]}, Model: {auto[1]}, Price per day: {auto[2]}")
            properties = ""
            for i in range(3, len(auto)):
                if i == 3:
                    properties = properties + auto[i]
                else:
                    properties = properties + ", " + auto[i]
            print(f"Properties: {properties}")
    file.close()
    rented_vehicle.close()
    

def rent_car():
    rented_vehicle = open("rentedVehicles.txt", 'r', encoding="utf-8")
    available_vehicle = open("vehicles.txt", 'r', encoding="utf-8")
    customers = open("customers.txt", 'r', encoding="utf-8")
    Customers = open("customers.txt", 'a', encoding="utf-8")
    rentedVehicle = open("rentedVehicles.txt", 'a', encoding="utf-8")
    rented = []
    available = []
    
    register_number = input("Enter the register number of the car you want to rent:\n")
    for line in rented_vehicle:
        vehicle = line.strip()
        auto = vehicle.split(',')
        rented.append(auto[0])

    for line1 in available_vehicle:
        vehicle1 = line1.strip()
        auto1 = vehicle1.split(',')
        available.append(auto1[0])

    if register_number in rented:
        print(f"{register_number} already rented")
        
    elif register_number in available:
        birthdate = get_valid_birthdate()
        birth_date = datetime.strptime(birthdate, "%d/%m/%Y").date()
        now = datetime.now()
        age = now.date() - birth_date
        age_years = int(age.days/365.25)
                
        if age_years < 18:
            print("Sorry, You are to young to rent a car!")
            
        elif age_years > 75:
            print("Sorry, You are to old to rent a car!")
            
        else:
            print("Age OK")
            user = user_check(customers, birth_date)
            
                    
            if user == False:
                while True:
                    first_name = str(input("Enter your first name:\n"))
                    last_name = str(input("Enter your last name:\n"))
                    if first_name[0] in string.ascii_uppercase and last_name[0] in string.ascii_uppercase:
                        x = name_check(first_name, last_name)
                        if x == True:
                            email = input("Enter your email:\n")
                            y = email_check(email)
                            if y == True:
                                now = datetime.now()
                                content = birthdate + ',' + first_name + ',' + last_name + ',' + email
                                Customers.writelines(content + "\n")
                                action = register_number + ',' + birthdate + ',' + now.strftime("%d/%m/%Y %H:%S")
                                rentedVehicle.writelines(action + "\n")
                                print(f"Hello {first_name}\nYou rented the car {register_number}")
                                break
                        
                            else:
                                print("Enter valid email addres")
                        else:
                            print("Names contain only letters and start with capital letters.")
                    else:
                        print("Names contain only letters and start with capital letters.")
            
                
            else:
                now = datetime.now()
                action = register_number + ',' + birth_date.strftime("%d/%m/%Y") + ',' + now.strftime("%d/%m/%Y %H:%S")
                rentedVehicle.writelines(action + "\n")
                customers.close()
                print(f"Hello {user[1]}\nYou rented the car {register_number}")            
                    
                                    
                                    
                        

                    
    else:
        print("Car does not exist")
    rentedVehicle.close()       
    rented_vehicle.close()
    available_vehicle.close()
        
def return_car():
    rented_vehicle = open("rentedVehicles.txt", 'r')
    available_vehicle = open("vehicles.txt", 'r', encoding="utf-8")
    transaction = open("transActions.txt", 'a', encoding="utf-8")
    rented = []
    available = []
    register_number = input("Enter the register number of the car you want to return:\n")
    lines = rented_vehicle.readlines()
    lines1 = available_vehicle.readlines()
    for line1 in lines1:
        vehicle1 = line1.strip()
        auto1 = vehicle1.split(',')
        available.append(auto1[0])
        if register_number == auto1[0]:
            for line in lines:
                vehicle = line.strip()
                auto = vehicle.split(',')
                rented.append(auto[0])
                if register_number == auto[0]:
                    birthdate = auto[1]
                    rented_vehicle_line = line
                    now = datetime.now()
                    pickup_time = datetime.strptime(auto[2], "%d/%m/%Y %H:%M")
                    lenght = (now.date()- pickup_time.date()).days
                    if register_number == auto1[0]:
                        price = float(auto1[2])*lenght
                        action = register_number + ',' + birthdate + ',' + auto[2]+ ',' + now.strftime("%d/%m/%Y %H:%S") + ',' + f"{price:.2f}"
                        transaction.writelines(action + "\n")
                        rentedVehicle = open("rentedVehicles.txt", 'w', encoding="utf-8")
                        for i in lines:
                            if i != rented_vehicle_line:
                                rentedVehicle.write(i)
                        rentedVehicle.close()
                        print(f"You rented the car for {lenght} days and it cost {price:.2f} euros")
                        
                
    rented_vehicle.close()
    available_vehicle.close()
    transaction.close()           
            
    if register_number in available and register_number not in rented:
        print("Car is not rented")
    
    elif register_number not in available:
        print("Car does not exist")

def count_money():
    file = open("transActions.txt", 'r', encoding="utf-8")
    money_sum = 0
    for line in file:
        file1 = line.strip()
        money = file1.split(',')
        money_sum += float(money[-1])
    print(f"Total sum of all transactions is {money_sum:.2f} euros")
    
def name_check(first_name, second_name):
    first = first_name[1:]
    second = second_name[1:]
    for i in first:
        if i not in string.ascii_lowercase:
            return False
    for n in second:
        if n not in string.ascii_lowercase:
            return False

    return True
    
def email_check(e_mail):
    try:
        dot_index = []
        y = e_mail.index("@")
        for n in range(len(e_mail)):
            if e_mail[n] == ".":
                dot_index.append(n)
    

        if y < dot_index[-1]:
            return True
        else:
            False
    except ValueError:
        return False


def get_valid_birthdate():
    while True:
        birthdate = input("Enter your birthdate (DD/MM/YYYY):\n")
        try:
            birth_date = datetime.strptime(birthdate, "%d/%m/%Y").date()
            return birthdate
        except:
            print("No such date, try again!")
def user_check(customers, birth_date):
    for i in customers:
        customer = i.strip()
        client = customer.split(',')
        date = datetime.strptime(client[0], "%d/%m/%Y").date()
        if birth_date == date:
            return client
        
    return False
    
    
        
    


def main():
    while True:
        selection = menu()
        
        if selection == "1":
            list_available_cars()
            
        elif selection == "2":
            rent_car()

        elif selection == "3":
            return_car()
        elif selection == "4":
            count_money()
        
        elif selection == "0":
            print("Bye, see You soon!")
            break
        else:
            print("Invalid choice, try again!")
            


main()

