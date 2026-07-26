from user import start
from donation import Donation
from reservation import reserve_donation, view_reserved_donations, start_delivery, complete_delivery
from emails_and_reports import generate_report,EmailService

def system_services():
    while True:
        print("\n===== System Services =====")
        print("1. Generate Report")
        print("2.Exit")
        service=input("choose Service To Implement")
        if service=="1":
            generate_report()
        elif service=="2":
            print("Good Bye")
            break
        else:
            print("Invalid Choice")
        

user_type=start()
donation=Donation(donor_name="", food_name="", quantity="", expiry_date="", location="", status="")
email_service = EmailService(
    "janaqoura@gmail.com",
    "ibwpqdnnjnxtuifr"
)
while True:
    if user_type in ["restaurant", "hotel", "family"]:
        print("\n===== Donor Menu =====")
        print("1. Add Donation")
        print("2. View Donations")
        print("3. Delete Donation")
        print("4. System Services")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            donor_name=input("Enter Donor Name : ")
            food_name=input("Enter Food Name : ")
            quantity=input("Enter Quantity : ")
            expiry_date=input("Enter Expiry_Date : ")
            location=input("Enter Donor Location : ")
            donor_one=Donation(donor_name, food_name, quantity, expiry_date, location,"Available")
            donor_one.add_donation()
            print("Donation Added Successfully")
            email_service.notify_new_donation(donor_one.to_dict())
        elif choice == "2":
            print(donation.view_donations())
        elif choice == "3":
            ID=input("Enter Id Of Donation You Want To Delete : ")
            donation.delete_donation(ID)
        elif choice == "4":
            system_services()
        elif choice=="5":
            print("Good Bye")
            break
        else:
            print("Invalid choice")
            
            
    elif user_type == "charity":
        print("\n===== Charity Menu =====")
        print("1. View Donations")
        print("2. Reserve Donation")
        print("3. System Services")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print(donation.view_donations())
        elif choice == "2":
            ID=input("Enter Id Of Donation You Want To Reserve : ")
            charity=input("Enter Charity Name : ")
            reserved=reserve_donation(ID, charity)
            if reserved:
                email_service.notify_reservation(reserved)
        elif choice == "3":
            system_services()
        elif choice=="4":
            print("Good Bye")
            break
        else:
            print("Invalid choice")
            
            
    elif user_type == "volunteer":
        print("\n===== Volunteer Menu =====")
        print("1. View Reserved Donations")
        print("2. Start Delivery")
        print("3. Complete Delivery")
        print("4. System Services")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print(view_reserved_donations())
        elif choice == "2":
            ID=input("Enter Id Of Donation You Want To Start Delivery : ")
            start_delivery(ID)
        elif choice == "3":
            ID=input("Enter Id Of Donation You Want To Complete Delivery : ")
            delivered=complete_delivery(ID)
            if delivered:
                email_service.notify_receipt_confirmation(delivered)
        elif choice == "4":
            system_services()
        elif choice=="5":
            print("Good Bye")
            break
        else:
            print("Invalid choice")
    else:
        print("This Role Is NOT Found")
        break