import csv
from faker import Faker
import random

# Load the original CSV file
with open('./sensors/sensors.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader) # Skip header row
    original_data = list(reader)

# Generate fake data
fake = Faker()
fake_data = []
for i in range(1000):
    sensor_index = random.randint(1, 999999)
    latitude = fake.latitude()
    longitude = fake.longitude()
    pressure = fake.random_int(min=900, max=1050)
    pm2_5_atm_a = round(random.uniform(0.0, 40.0), 2)
    pm2_5_atm_b = round(random.uniform(0.0, 40.0), 2)
    humidity_a = fake.random_int(min=20, max=80)
    temperature_a = fake.random_int(min=-10, max=50)
    location_type = random.choice([0, 1, 2])
    pm1_0_atm_a = round(random.uniform(0.0, 50.0), 2)
    pm1_0_atm_b = round(random.uniform(0.0, 50.0), 2)
    scattering_coefficient_a = round(random.uniform(0.0, 100.0), 2)
    scattering_coefficient_b = round(random.uniform(0.0, 100.0), 2)
    
    fake_data.append([sensor_index, latitude, longitude, pressure, pm2_5_atm_a, pm2_5_atm_b, humidity_a, temperature_a, location_type, pm1_0_atm_a, pm1_0_atm_b, scattering_coefficient_a, scattering_coefficient_b])

# # Add a blank row
# fake_data.append(['', '', '', '', '', '', '', '', '', '', '', '', ''])

# Save the fake data to a new CSV file
with open('fake_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fake_data)
