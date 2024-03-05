import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number
import requests
import pycountry
from fuzzywuzzy import process
import random
import string
import regex as re
import datetime


def country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country:
            return country.name
        else:
            return np.nan
    except:
        return np.nan


def ip_to_country(ip_address):
        
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            data = response.json()
            return country_code_to_name(data.get('country'))
        else:
            return np.nan
    except:
        return np.nan
    

def city_to_country(city):
    geolocator = Nominatim(user_agent="city_to_country_converter")
    location = geolocator.geocode(city, language="en")
    if location:
        return location.address.split(",")[-1].strip()
    else:
        return np.nan


def phone_number_to_country(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country_code = region_code_for_number(parsed_number)
        if country_code:
            return country_code_to_name(country_code)
        else:
            return np.nan
    except:
        return np.nan


def consistent_country(country_input:str):
    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
        "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
        "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
        "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
        "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
        "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon",
        "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
        "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
        "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan",
        "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
        "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
        "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
        "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay",
        "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
        "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
        "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
        "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago",
        "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
        "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia",
        "Zimbabwe"
    ]

    if isinstance(country_input, str) and country_input:
        return process.extractOne(country_input, countries)[0]
    else:
        return "Prefer not to say"
        

def consistent_gender(gender_input:str):
    valid_set = ["Male", "Female", "Gender Fluid", "Non Binary", "Prefer not to say"]

    if isinstance(gender_input, str) and gender_input:
        if gender_input == "M":
            return "Male"
        elif gender_input == "F":
            return "Female"
        else:
            return process.extractOne(gender_input, valid_set)[0]
    else:
        return "Prefer not to say"
        

def username_from_email(email):
    at_index = email.find("@")
    return email[:at_index]


def generate_random_username(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def combine_interests(group):
    all_interests = ','.join(group['interests']).split(',')
    unique_interests = list(set(all_interests))
    return pd.Series({'combined_interests': [','.join(unique_interests)]})


def clean_subscription(row):
    if row in [1, "Yes", "yes", "1"]:
        return 1
    else:
        return 0
    

def consistent_card_type(card_type:str):
    valid_set = ["mastercard", "jcb", "americanexpress",
                    "visa", "maestro", "paypal", "dinersclub",
                    "chinaunionpay", "creditcard", "debitcard", "laser",
                    "bankcard", "instapayment", "solo", "switch", "card"
                ]

    if isinstance(card_type, str) and card_type:
        result, threshold = process.extractOne(card_type, valid_set)
        if threshold >= 75:
            return result
        else:
            return np.nan
    else: 
        return np.nan
    

def month_fuzzy_match(month_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    return months_dict[process.extractOne(month_str, months)[0]]


def two_len_year(year):
    if len(year) == 2 and int(year) > 23:
        return "19" + year
    elif len(year) == 2:
        return "20" + year
            

def date_list_to_datetime(date):
    a = date[0]
    b = date[1]
    c = date[2]
    if len(c) == 2:
        c = two_len_year(c)
    try:
        return datetime.datetime(day=int(a), month=int(b), year=int(c))
    except:
        return datetime.datetime(day=int(b), month=int(a), year=int(c))


def clean_birth_date(birth_date):
    if isinstance(birth_date, str):
        if "/" in birth_date:
            try:
                date = birth_date.split("/")
                return date_list_to_datetime(date)
            except:
                return np.nan
            
        elif "-" in birth_date:
            try:
                date = birth_date.split("-")
                return date_list_to_datetime(date)
            except:
                return np.nan
            
        else:
            matches = re.search(r"(\d*)?(th)? ?(\w*) (\d*)", birth_date)
            try:
                day, _, month, year = matches.groups()
                if len(year) == 2:
                    year = two_len_year(year)

                if not day:
                    day = 1
                return datetime.datetime(day=int(day), month=month_fuzzy_match(month), year=int(year))
            except:
                return np.nan
    else:
        if isinstance(birth_date, datetime.datetime):
            return birth_date
        else:
            return np.nan
        

if __name__ == '__main__':
    pass