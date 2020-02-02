from hungrynigga import db
from hungrynigga.models import *
from random import randint
from hungrynigga import bcrypt

db.create_all()

while True:
    print('''
    Choose which table you want to insert data?
    1. User
    2. Item
    3. Orderinfo
    4. Ordereditem
    Enter the number:
    ''')
    choice = int(input())

    if choice==1:
        #User
        print("Enter Username: ", end="")
        un = str(input())
        print("Enter Email: ", end="")
        mail = str(input())
        print("Enter Password: ", end="")
        pswd = str(input())
        passwd = bcrypt.generate_password_hash(pswd).decode('utf-8')
        x = User(username=un, email=mail, password=passwd)
        db.session.add(x)
        
    elif choice == 2:
        #Item
        print("Enter food name: ", end="")
        foodname = str(input())
        price = int(randint(4,40)*10)
        ofer = randint(0,100)
        rat = randint(50,100)
        while True:
            print("Is food veg? Please ans in y for yes and n for no(y/n)?")
            x = input()
            if x == 'y':
                v = True
                break
            elif x == 'n':
                v = False
                break
            else:
                continue

        print("Enter Category of Food")
        cat = input()
        print
        x = Item(title=foodname, mrp=price, offer=ofer, rating=rat, category=cat, veg=v)
        db.session.add(x)
        
    elif choice == 3:
        #Orderinfo
        print("Enter the address: ", end="")
        adres = input()
        zipcode = randint(24000, 30000)
        contact = randint(7000000000,9999999999)
        print("Enter username of customer: ", end="")
        name = str(input())
        user = User.query.filter_by(username=name).first()
        if user is None:
            print("No user with this username exist")
            continue
        
        uid = user.id
        x = Orderinfo(address=adres, phone=contact, zip_code=zipcode, user_id=uid)
        db.session.add(x)
        
    elif choice == 4:
        #Ordereditem
        print("Item ID: ", end="")
        iid = int(input())
        print("Enter username of customer: ", end="")
        name = str(input())
        user = User.query.filter_by(username=name).first()
        if user is None:
            print("No user with this username exist")
            continue

        uid = user.id
        print("Enter Amount: ", end="")
        amount = int(input())
        print("Order ID: ", end="")
        oid = int(input())
        x = Orderitem(item_id=iid, quantity=amount, user_id=uid ,order_id=oid)
        db.session.add(x)
    else:
        print("Please Choose Correctly")
        continue

    try:
        db.session.commit()
        print("Data Inserted Successfully")
    except Exception as e:
        print("Error: " + str(e))
            
