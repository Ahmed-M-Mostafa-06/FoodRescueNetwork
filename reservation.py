import json
from prettytable import PrettyTable


def load_data():
    with open("donations.json") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("donations.json", "w") as file:
        json.dump(data, file,indent=4)


# ---------- Feature 4: Reserve Donation ----------

def reserve_donation(ID, charity_name):
    data = load_data()
    found = False
    for donation in data["donations"]:
        if str(ID) == donation["donation_id"]:
            found = True
            if donation["status"] == "Available":
                donation["status"] = "Reserved"
                donation["reserved_by"] = charity_name
                save_data(data)
                print("Donation Reserved Successfully")
                return donation
            else:
                print("This Donation Is Not Available For Reservation")
                return None
            break
    if found == False:
        print("NOT FOUND !!")


# ---------- Feature 5: Volunteer Delivery ----------

def view_reserved_donations():
    data = load_data()
    table = PrettyTable()
    table.field_names = ["donation_id", "donor_name", "food_name", "quantity",
                          "expiry_date", "location", "status", "reserved_by"]
    for donation in data["donations"]:
        if donation["status"] == "Reserved":
            table.add_row([donation["donation_id"], donation["donor_name"],
                           donation["food_name"], donation["quantity"],
                           donation["expiry_date"], donation["location"],
                           donation["status"], donation.get("reserved_by", "")])
    return table


def start_delivery(ID):
    data = load_data()
    found = False
    for donation in data["donations"]:
        if str(ID) == donation["donation_id"]:
            found = True
            if donation["status"] == "Reserved":
                donation["status"] = "On Delivery"
                save_data(data)
                print("Delivery Started")
            else:
                print("This Donation Is Not Reserved Yet")
            break
    if found == False:
        print("NOT FOUND !!")


def complete_delivery(ID):
    data = load_data()
    found = False
    for donation in data["donations"]:
        if str(ID) == donation["donation_id"]:
            found = True
            if donation["status"] == "On Delivery":
                donation["status"] = "Delivered"
                save_data(data)
                print("Donation Delivered Successfully")
                return donation
            else:
                print("This Donation Is Not On Delivery")
                return None
            break
    if found == False:
        print("NOT FOUND !!")
