"""
Master_data.py
==============
Static master data pools used across all generators.

Contains India-specific:
    - Name lists (first & last names from major regions/communities)
    - City / State / Pincode tuples
    - Samsung product catalogue (SKU, name, category, MRP, specs)
    - Enum lists for channels, payment modes, issue types, etc.

To add new cities, products, or enum values, edit the relevant
list in this file — no other file needs to change.
"""

# =====================================================================
# PEOPLE — First & Last names (Indian)
# =====================================================================

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ishwar", "Atharv", 
    "Dhruv","Kabir", "Ishaan", "Shaurya", "Advait", "Rudra", "Madhav", "Pranav", "Arnav", 
    "Vedant", "Rohan","Yash", "Ananya", "Aadhya", "Saanvi", "Aanya", "Aaradhya", "Pari", 
    "Priya", "Riya", "Sneha","Diya", "Kavya", "Ishita", "Meera", "Pooja", "Anjali", 
    "Shreya", "Nisha", "Divya", "Neha","Siddharth", "Rahul", "Amit", "Suresh", 
    "Ramesh", "Vikram", "Deepak", "Manish", "Kiran", "Sunita","Rajesh", "Pradeep", 
    "Nikhil", "Kunal", "Gaurav", "Varun", "Ritesh", "Sunil", "Ashok", "Vijay","Harish",
    "Girish", "Prakash", "Manoj", "Ravi", "Ajay", "Abhishek", "Sachin", "Dinesh", 
    "Rakesh","Lakshmi", "Radha", "Geeta", "Savita", "Usha", "Rekha", "Seema", "Shanti", 
    "Lata", "Kumari","Mohit", "Arvind", "Sanjay", "Inder", "Falguni", "Ashwin", "Rishi", 
    "Tanmay", "Daksh", "Zalak","Gurpreet", "Harpreet", "Manpreet", "Jaspreet", 
    "Kuldeep", "Balwinder", "Navdeep", "Amrik", "Baljeet", "Sukh"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Joshi", "Mehta",
    "Rao","Reddy", "Nair", "Pillai", "Menon", "Iyer", "Agarwal", "Bansal", "Goel",
    "Malhotra", "Chopra","Kapoor", "Bose", "Chatterjee", "Mukherjee", "Ghosh", 
    "Banerjee", "Das", "Dutta", "Roy", "Sen","Mishra", "Tiwari", "Tripathi", "Pandey",
    "Shukla", "Dubey", "Yadav", "Chauhan", "Thakur", "Rajput","Kulkarni", "Joshi", 
    "Sawant", "Deshmukh", "Bhatt", "Sarin", "Kohli", "Khanna", "Rawat", "Bisht","Naidu", 
    "Raju", "Babu", "Rao", "Murthy", "Varma", "Chowdary", "Prasad", "Goud", "Desai","Patil",
    "Jadhav", "Shinde", "Pawar", "Bhosale", "More", "Kadam", "Mane", "Salvi", "Kulkarni",
    "Wanjare", "Gaikwad", "Thakkar", "Solanki", "Rathod", "Parmar", "Baria", "Prajapati", 
    "Chaudhari", "Vasava"
]

# =====================================================================
# GEOGRAPHY — (city, state, pincode) tuples covering Tier 1–3 cities
# =====================================================================

CITIES_STATES = [
    ("Mumbai",             "Maharashtra",       "400001"),
    ("Delhi",              "Delhi",             "110001"),
    ("Bengaluru",          "Karnataka",         "560001"),
    ("Hyderabad",          "Telangana",         "500001"),
    ("Chennai",            "Tamil Nadu",        "600001"),
    ("Kolkata",            "West Bengal",       "700001"),
    ("Pune",               "Maharashtra",       "411001"),
    ("Ahmedabad",          "Gujarat",           "380001"),
    ("Jaipur",             "Rajasthan",         "302001"),
    ("Surat",              "Gujarat",           "395001"),
    ("Lucknow",            "Uttar Pradesh",     "226001"),
    ("Kanpur",             "Uttar Pradesh",     "208001"),
    ("Nagpur",             "Maharashtra",       "440001"),
    ("Indore",             "Madhya Pradesh",    "452001"),
    ("Thane",              "Maharashtra",       "400601"),
    ("Bhopal",             "Madhya Pradesh",    "462001"),
    ("Visakhapatnam",      "Andhra Pradesh",    "530001"),
    ("Pimpri-Chinchwad",   "Maharashtra",       "411017"),
    ("Patna",              "Bihar",             "800001"),
    ("Vadodara",           "Gujarat",           "390001"),
    ("Ghaziabad",          "Uttar Pradesh",     "201001"),
    ("Ludhiana",           "Punjab",            "141001"),
    ("Agra",               "Uttar Pradesh",     "282001"),
    ("Nashik",             "Maharashtra",       "422001"),
    ("Faridabad",          "Haryana",           "121001"),
    ("Meerut",             "Uttar Pradesh",     "250001"),
    ("Rajkot",             "Gujarat",           "360001"),
    ("Kalyan-Dombivli",    "Maharashtra",       "421301"),
    ("Vasai-Virar",        "Maharashtra",       "401202"),
    ("Varanasi",           "Uttar Pradesh",     "221001"),
    ("Srinagar",           "Jammu & Kashmir",   "190001"),
    ("Aurangabad",         "Maharashtra",       "431001"),
    ("Dhanbad",            "Jharkhand",         "826001"),
    ("Amritsar",           "Punjab",            "143001"),
    ("Navi Mumbai",        "Maharashtra",       "400706"),
    ("Allahabad",          "Uttar Pradesh",     "211001"),
    ("Ranchi",             "Jharkhand",         "834001"),
    ("Howrah",             "West Bengal",       "711101"),
    ("Coimbatore",         "Tamil Nadu",        "641001"),
    ("Jabalpur",           "Madhya Pradesh",    "482001"),
    ("Gwalior",            "Madhya Pradesh",    "474001"),
    ("Vijayawada",         "Andhra Pradesh",    "520001"),
    ("Jodhpur",            "Rajasthan",         "342001"),
    ("Madurai",            "Tamil Nadu",        "625001"),
    ("Raipur",             "Chhattisgarh",      "492001"),
    ("Kota",               "Rajasthan",         "324001"),
    ("Guwahati",           "Assam",             "781001"),
    ("Chandigarh",         "Chandigarh",        "160001"),
    ("Thiruvananthapuram", "Kerala",            "695001"),
    ("Mysuru",             "Karnataka",         "570001"),
    ("Noida",              "Uttar Pradesh",     "201301"),
]

# Convenience flat lists derived from the CITIES_STATES
CITIES   = [c[0] for c in CITIES_STATES]
STATES   = [c[1] for c in CITIES_STATES]
PINCODES = [c[2] for c in CITIES_STATES]

# =====================================================================
# SAMSUNG PRODUCT CATALOGUE
# Each tuple: (SKU, name, category, subcategory, MRP_INR,
#              RAM_GB|None, storage_GB|None, display_inches|None)
# =====================================================================

SAMSUNG_PRODUCTS = [
    # Galaxy S Series 
    ("SM-S938BZKGINS", "Galaxy S25 Ultra",       "Smartphones", "Galaxy S Series",  139999, 12, 512, "6.9"),
    ("SM-S931BZBGINS", "Galaxy S25",             "Smartphones", "Galaxy S Series",   82999,  8, 256, "6.3"),
    ("SM-S928BZKGINS", "Galaxy S24 Ultra",       "Smartphones", "Galaxy S Series",  134999, 12, 512, "6.8"),
    ("SM-S921BZBGINS", "Galaxy S24",             "Smartphones", "Galaxy S Series",   79999,  8, 256, "6.2"),
    ("SM-S918BZKGINS", "Galaxy S23 Ultra",       "Smartphones", "Galaxy S Series",  124999, 12, 512, "6.8"),
    # Galaxy A Series 
    ("SM-A566EBKCINS", "Galaxy A56 5G",          "Smartphones", "Galaxy A Series",   42999,  8, 256, "6.6"),
    ("SM-A366MBKCINS", "Galaxy A36 5G",          "Smartphones", "Galaxy A Series",   33999,  8, 256, "6.6"),
    ("SM-A556BZKGINS", "Galaxy A55 5G",          "Smartphones", "Galaxy A Series",   39999,  8, 128, "6.6"),
    ("SM-A356PBKCINS", "Galaxy A35 5G",          "Smartphones", "Galaxy A Series",   30999,  8, 128, "6.6"),
    ("SM-A166FBKCINS", "Galaxy A16 5G",          "Smartphones", "Galaxy A Series",   18999,  6, 128, "6.7"),
    ("SM-A066FBKCINS", "Galaxy A06s",            "Smartphones", "Galaxy A Series",   14999,  4, 128, "6.7"),
    ("SM-A546ELBGINS", "Galaxy A54 5G",          "Smartphones", "Galaxy A Series",   35999,  8, 256, "6.4"),
    # Galaxy M Series
    ("SM-M556BBKCINS", "Galaxy M55 5G",          "Smartphones", "Galaxy M Series",   28999,  8, 128, "6.7"),
    ("SM-M356BBKCINS", "Galaxy M35 5G",          "Smartphones", "Galaxy M Series",   20999,  8, 128, "6.6"),
    ("SM-M156BBKCINS", "Galaxy M15 5G",          "Smartphones", "Galaxy M Series",   15999,  6, 128, "6.5"),
    ("SM-M546BZKGINS", "Galaxy M54 5G",          "Smartphones", "Galaxy M Series",   24999,  8, 128, "6.7"),
    # Galaxy Z Series 
    ("SM-F956BZKGINS", "Galaxy Z Fold6",         "Smartphones", "Galaxy Z Series",  164999, 12, 512, "7.6"),
    ("SM-F741BZKGINS", "Galaxy Z Flip6",         "Smartphones", "Galaxy Z Series",  109999, 12, 256, "6.7"),
    # Tablets 
    ("SM-X826BZKGINS", "Galaxy Tab S10 FE",      "Tablets",     "Galaxy Tab S",      52999,  8, 256, "10.9"),
    ("SM-X720NZAGINS", "Galaxy Tab S10",         "Tablets",     "Galaxy Tab S",      79999, 12, 256, "11.0"),
    ("SM-X920NZAGINS", "Galaxy Tab S10 Ultra",   "Tablets",     "Galaxy Tab S",     112999, 12, 512, "14.6"),
    ("SM-T235NZAGINS", "Galaxy Tab A9 Lite",     "Tablets",     "Galaxy Tab A",      14999,  4,  64,  "8.7"),
    ("SM-X215NZAGINS", "Galaxy Tab A9+",         "Tablets",     "Galaxy Tab A",      20999,  8, 128, "11.0"),
    # Televisions
    ("UA65DU8000KLXL", "65\" Crystal 4K DU8000", "Televisions", "Crystal 4K",        82900, None, None, "65.0"),
    ("UA55DU7700KLXL", "55\" Crystal 4K DU7700", "Televisions", "Crystal 4K",        56900, None, None, "55.0"),
    ("UA43DU7700KLXL", "43\" Crystal 4K DU7700", "Televisions", "Crystal 4K",        39900, None, None, "43.0"),
    ("QA65QN90DAKLXL", "65\" Neo QLED 4K",       "Televisions", "Neo QLED",         234900, None, None, "65.0"),
    ("QA55Q80DAKLXL",  "55\" QLED 4K",           "Televisions", "QLED",             119900, None, None, "55.0"),
    # Air Conditioners
    ("AR18CYNZABE",    "1.5 Ton Wind-Free",       "Air Conditioners", "Wind-Free",    65990, None, None, None),
    ("AR12CYNZABE",    "1 Ton Wind-Free",         "Air Conditioners", "Wind-Free",    54990, None, None, None),
    ("AR18AYHYBWK",    "1.5 Ton Convertible 5in1","Air Conditioners", "Digital Inverter", 47990, None, None, None),
    ("AR12AYHYBWK",    "1 Ton Convertible 5in1",  "Air Conditioners", "Digital Inverter", 39990, None, None, None),
    # Washing Machines 
    ("WW80T604DAB",    "8Kg AI Ecobubble Front",  "Washing Machines", "Front Load",   48990, None, None, None),
    ("WW70T602DAX",    "7Kg AI Ecobubble Front",  "Washing Machines", "Front Load",   41990, None, None, None),
    ("WA80CG4441BX",   "8Kg Eco Bubble Top",      "Washing Machines", "Top Load",     30990, None, None, None),
    ("WA65B4002GS",    "6.5Kg Eco Bubble Top",    "Washing Machines", "Top Load",     19990, None, None, None),
    # Refrigerators 
    ("RT42DG6421S8",   "415L Bespoke Double Door","Refrigerators",   "Double Door",   48990, None, None, None),
    ("RT34D4522S8",    "324L Bespoke Double Door","Refrigerators",   "Double Door",   37990, None, None, None),
    ("RR20D2723S8",    "198L Digital Inverter",   "Refrigerators",   "Single Door",   19990, None, None, None),
    ("RF65DG977FSE",   "653L Family Hub French",  "Refrigerators",   "French Door",  164900, None, None, None),
]

# =====================================================================
# ENUMERATIONS — shared across multiple generators
# =====================================================================

PAYMENT_MODES = [
    "UPI", "Credit Card", "Debit Card", "Net Banking",
    "EMI", "Cash on Delivery", "Wallet",
]

CHANNELS = [
    "Samsung.com", "Flipkart", "Amazon IN", "Croma",
    "Reliance Digital", "Vijay Sales", "Samsung SmartCafé", "Blinkit",
]

BANKS = [
    "SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra",
    "PNB", "Bank of Baroda", "Canara Bank", "Yes Bank", "Federal Bank",
]

EMI_PARTNERS = [
    "HDFC Bank", "Bajaj Finserv", "ICICI Bank", "SBI Card",
    "Kotak Mahindra", "Home Credit", "Amazon Pay Later", "CASHe",
]

ISSUE_TYPES = [
    "Screen Damage", "Battery Drain", "Software Issue", "Camera Issue",
    "Charging Problem", "Speaker Issue", "Network Issue", "Water Damage",
    "Physical Damage", "Performance Issue", "Heating Issue", "Bluetooth Issue",
    "WiFi Issue", "Fingerprint Sensor", "Touch Not Working",
]

RETURN_REASONS = [
    "Dead on Arrival", "Changed Mind", "Wrong Product",
    "Better Price Elsewhere", "Product Not as Described",
    "Manufacturing Defect", "Damaged in Transit", "Feature Not Working",
    "Size Mismatch", "Duplicate Order",
]

COMPLAINT_STATUS = [
    "Open", "In Progress", "Resolved", "Closed",
    "Escalated", "Pending Parts", "Awaiting Customer",
]

CAMPAIGN_NAMES = [
    "Diwali Dhamaka Sale", "IPL Season Special", "Republic Day Offer",
    "Independence Day Sale", "Onam Festival Offer", "Pongal Special",
    "Holi Bumper Sale", "Big Shopping Days", "Samsung Upgrade Fest",
    "Galaxy Fest India", "Navratri Mega Sale", "Eid Special", "Christmas Carnival",
    "New Year Bonanza", "Black Friday Sale", "Back to School", "Student Offer",
    "Galaxy AI Launch", "Monsoon Madness", "Summer Cool Deal",
]

STORE_TYPES = [
    "Samsung SmartCafé", "Samsung Brand Store", "Large Format Retail",
    "Multi-Brand Outlet", "Online Exclusive Partner",
]

RETAIL_CHAINS = [
    "Croma", "Reliance Digital", "Vijay Sales", "Poorvika Mobiles",
    "Sangeetha Mobiles", "Pai International", "Big Electronics",
    "Amazon IN", "Flipkart", "Samsung SmartCafé",
]

DEPARTMENTS = [
    "Sales", "Marketing", "R&D", "Manufacturing", "Supply Chain",
    "Finance", "HR", "Customer Service", "IT", "Legal",
    "Quality Assurance", "Logistics", "After Sales Service", "ESG & Sustainability",
]

DESIGNATIONS = [
    "Executive", "Senior Executive", "Team Lead", "Manager",
    "Senior Manager", "Assistant Manager", "General Manager",
    "Deputy Manager", "Vice President", "Director",
    "Chief Technology Officer", "Product Owner", "Engineer",
    "Senior Engineer", "Data Scientist", "Senior Analyst",
]

LOCATIONS_OFFICE = [
    "Noida HQ", "Sriperumbudur Factory", "Bengaluru R&D",
    "Mumbai Office", "Chennai Office", "Hyderabad Office",
    "Kolkata Office", "Pune Office", "Delhi Office", "Ahmedabad Office",
]

SUPPLIER_CATEGORIES = [
    "Display Panels", "Batteries", "Camera Modules", "Memory Chips",
    "Processors", "Plastic Components", "Packaging", "PCB Boards",
    "Chargers & Cables", "Metal Parts", "Software Licenses", "Logistics",
    "Glass", "Cooling Systems", "Microphones & Speakers",
]

# Colour variants used when generating product colour-variant SKUs
COLOUR_VARIANTS = [
    "Phantom Black", "Cream", "Green", "Lavender",
    "Graphite", "Blue", "Silver", "Gold",
]

# Messy casing map for category names (simulates upstream ingestion errors)
CATEGORY_MESS_MAP = {
    "Smartphones":      "smartphones",
    "Televisions":      "TELEVISIONS",
    "Tablets":          "tablet",
    "Air Conditioners": "Air Conditioner",
    "Washing Machines": "Washing machine",
    "Refrigerators":    "refrigerators",
}

# Sample product review texts
REVIEW_TEXTS = [
    "Excellent product! Worth every rupee.",
    "Camera quality is outstanding.",
    "Battery life could be better.",
    "Screen is amazing for the price.",
    "Delivery was fast, product is genuine.",
    "Build quality is premium.",
    "Overpriced for the features offered.",
    "Very happy with my purchase.",
    "Samsung service is great in my city.",
    "Sound quality is top notch.",
    "Gets hot during gaming sessions.",
    "Perfect gift for Diwali.",
    "Bought during sale, great deal!",
    "Software updates are smooth.",
    "Value for money in this segment.",
    "Would recommend to friends.",
    "Disappointed with battery backup.",
    "Best phone under this budget.",
    "Display colors are very vibrant.",
    "Touch response is excellent.",
]
