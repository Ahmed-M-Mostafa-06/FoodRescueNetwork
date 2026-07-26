import json

class user_register_data:
    def __init__(self,name,e_mail,password):
        self.name=name
        self.e_mail=e_mail
        self.password=password
        
    @staticmethod
    def add_data(name,e_mail,password,typee): 
        with open ("users.json","r") as file :
         data=json.load(file)
         
         new_user = {"name": name,"email": e_mail,"password": password,"type": typee}
         data.append(new_user)
         
        with open ("users.json","w") as file :
         json.dump(data, file, indent=4)
         
        print()
        print("______Login ______")
        print()
        
        with open ("users.json","r") as file :
          data=json.load(file)
          e_mail_entered=input("Enter your email : ").strip()
          password_entered=input("Enter your password : ").strip()
          for i in data:
            login_email=i["email"]
            login_password=i["password"]
            if e_mail_entered==login_email and password_entered==login_password:
                print("--------------------------")
                print(" Login Successful! 😃 ")
                break
          else:
            print("--------------------------")
            print("incorect password or e_mail 🙁")
def start():
    statu=input("register or login ? ").lower().strip()
    if statu=="register" :
        name=input("Enter youe name : ")
        e_mail=input("Enter your email : ").strip()
        password=input("Enter your password : ").strip()
        typee=input("Enter your type (restaurant/hotel/family/charity/volunteer) : ").lower().strip()
        print("--------------------------")
        print(" register Successful! 😃 ")
        
        regester1 = user_register_data(name,e_mail, password)
        regester1.add_data(name,e_mail, password,typee)
        return typee
    elif statu=="login":
        with open ("users.json","r") as file :
            data=json.load(file)
            e_mail_entered=input("Enter your email : ").strip()
            password_entered=input("Enter your password : ").strip()
            for i in data:
                login_email=i["email"]
                login_password=i["password"]
                if e_mail_entered==login_email and password_entered==login_password:
                    print("--------------------------")
                    user_type=i["type"]
                    print(" Login Successful! 😃 ")
                    return user_type
            else:
                print("--------------------------")
                print("incorect password or e_mail 🙁")
                return None
    else:
        print("Enter register or login right 🫵 ")