import json
from prettytable import PrettyTable
class Donation:
    def __init__(self,donor_name,food_name,quantity,expiry_date,location,status):
        self.donation_id=None
        self.donor_name=donor_name
        self.food_name=food_name
        self.quantity=quantity
        self.expiry_date=expiry_date
        self.location=location
        self.status=status
        
        
        
    def to_dict(self):
        return {
            "donation_id":self.donation_id,
            "donor_name":self.donor_name,
            "food_name":self.food_name,
            "quantity":self.quantity,
            "expiry_date":self.expiry_date,
            "location":self.location,
            "status":self.status
            }
    
    
    
    def load_data(self):
        with open("donations.json") as file:
            data=json.load(file)
        return data
    
    
    
    def save_data(self,data):
        with open("donations.json","w") as file:
            json.dump(data,file,indent=4) 
            
            
            
    def generate_id(self, data):
        id_list=[]
        for donation in data["donations"]:
            id_list.append(int(donation["donation_id"]))
        if id_list:
            count=max(id_list)+1
        else:
            count=1
        return f"{count}"
    
    
    
    def add_donation(self):
        data=self.load_data()
        self.donation_id = self.generate_id(data)
        data["donations"].append(self.to_dict())
        self.save_data(data)
        
        
        
        
    def view_donations(self):
        data=self.load_data()
        if not data["donations"]:
            print("No Donations Yet!!!!")
        table=PrettyTable()
        table.field_names=["donation_id","donor_name","food_name","quantity","expiry_date","location","status"]
        for donation in data["donations"]:
            table.add_row([donation["donation_id"],donation["donor_name"],
                           donation["food_name"],donation["quantity"],
                           donation["expiry_date"],donation["location"],
                           donation["status"]])
        return table

    def delete_donation(self,ID):
       data=self.load_data()
       flag=False
       for donation in data["donations"]:
           if str(ID)==donation["donation_id"]:
               data["donations"].remove(donation)
               self.save_data(data)
               flag=True
               print("Donation Deleted Successfully")
               break
       if flag==False:
           print("NOT FOUND !!")
