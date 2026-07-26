# FoodRescueNetwork 🍲

A Python application for managing food donations, connecting donors (restaurants, hotels, and families) with charities and volunteers to reduce food waste and support communities in need.

## Features

- **Multiple user roles**: Restaurant, Hotel, Family (donors), Charity, and Volunteer
- **Donation management**: Post, track, and reserve food donations
- **Reservation system**: Charities/volunteers can reserve available donations
- **Reports & emails**: Automated status reports and email notifications for donations
- **Desktop GUI**: Built with Tkinter for a simple, local interface
- **Data storage**: Donations and user data stored in JSON files

## Project Structure

```
FoodRescueNetwork/
├── main.py                  # Entry point of the application
├── gui.py                   # Tkinter GUI interface
├── donation.py               # Core donation logic
├── reservation.py            # Reservation handling
├── user.py                   # User roles and authentication
├── emails_and_reports.py     # Email notifications and reporting
├── donations.json             # Donation records (sample/test data)
├── users.json                 # User records (sample/test data)
├── email_config.py           # Email credentials (NOT included — see setup)
└── .gitignore
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Ahmed-M-Mostafa-06/FoodRescueNetwork.git
   cd FoodRescueNetwork
   ```

2. Install the required packages:
   ```
   pip install prettytable pandas
   ```

3. Create your own `email_config.py` file (not included in the repo for security) with your email credentials:
   ```python
   EMAIL_ADDRESS = "your_email@example.com"
   EMAIL_PASSWORD = "your_app_password"
   ```

4. Run the application:
   ```
   python main.py
   ```
   Or launch the GUI version:
   ```
   python gui.py
   ```

## Notes

- The data in `users.json` and `donations.json` is sample/test data for demonstration purposes.
- This project is under active development as part of a university course.

## Author

Ahmed Mostafa
