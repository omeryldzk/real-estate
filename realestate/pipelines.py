# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from google.cloud.sql.connector import Connector
import pymysql

import sqlalchemy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy

    # initialize Connector object
connector = Connector()



class RealestatePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
         # Convert price string to float
        if 'price' in adapter:
            value = adapter.get('price')
            int_val = value.replace(".","").strip()
            adapter['price'] = int(int_val)
        
        # Clean up the 'rooms' field
        if 'rooms' in adapter:
            rooms = adapter.get('rooms')
            cleaned_rooms = rooms.replace("\n", "").replace(" ", "").strip()
            adapter['rooms'] = cleaned_rooms

         # Clean up the 'rooms' field
        if 'size' in adapter:
            rooms = adapter.get('size',)
            cleaned_rooms = rooms.replace(" m²", "").strip()
            adapter['size'] = int(cleaned_rooms)
        
         # Fields that need to be converted to integers
        integer_fields = ['age', 'quota', 'status']

        # Extract only the numeric part from 'age' field
        if 'age' in adapter:
            age = adapter.get('age')
            cleaned_age = age.split()[0].strip()  # Split by whitespace and take the first part
            adapter['age'] = int(cleaned_age)
        
        
        ## Yüksek giriş ve bahçe katı durumları bu partı bozuyor
        # if 'floor' in adapter:
        #     floor_str = adapter['floor']
        #     match = re.search(r'\d+', floor_str)
        #     if match:
        #         adapter['floor'] = int(match.group())
        #     else:
        #         adapter['floor'] = None 

        # if 'date' in adapter:
        #     date_str = adapter['date']
        #     try:
        #         # Parse the date string to a datetime object
        #         adapter['date'] = datetime.strptime(date_str, '%d-%m-%Y')
        #     except ValueError:
        #         # Handle the case where the date format is incorrect
        #         adapter['date'] = None  # or some default value
        return item
    
class SaveToMySQLPipeline:
    def open_spider(self, spider):
        # Establish connection to the MySQL database
        self.conn = mysql.connector.connect(
            host='34.173.143.144',
            user='root',
            password='oy159753',
            database='real-estate'
        )
        self.cursor = self.conn.cursor()

        # Create table if it does not exist
        create_table_query = """
            CREATE TABLE realestate (
        id SERIAL PRIMARY KEY,  -- Auto-incrementing ID for each record
        title VARCHAR(255) NOT NULL,  -- Title of the listing
        price INT NOT NULL,  -- Price of the property, converted to an integer
        currency VARCHAR(10) NOT NULL,  -- Currency of the price
        property_type VARCHAR(100),  -- Type of the property (e.g., apartment, house)
        rooms VARCHAR(50),  -- Number of rooms
        size INT,  -- Size of the property in square meters
        age INT,  -- Age of the property
        floor VARCHAR(50),  -- Floor number or level of the property
        date DATE,  -- Date of the listing
        image_url TEXT,  -- URL of the property image
        agency_logo TEXT  -- URL of the agency's logo
    );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()
    
    def close_spider(self, spider):
        # Close the connection to the database when the spider is closed
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        