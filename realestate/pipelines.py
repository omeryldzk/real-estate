import mysql.connector
from itemadapter import ItemAdapter
from datetime import datetime

class RealestatePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert price string to int
        if 'price' in adapter and adapter['price']:
            value = adapter.get('price')
            int_val = value.replace(".", "").strip()
            adapter['price'] = int(int_val) if int_val.isdigit() else 0
        
        # Clean up the 'rooms' field
        if 'rooms' in adapter and adapter['rooms']:
            rooms = adapter.get('rooms')
            cleaned_rooms = rooms.replace("\n", "").replace(" ", "").strip()
            adapter['rooms'] = cleaned_rooms

        # Clean up the 'size' field
        if 'size' in adapter and adapter['size']:
            size = adapter.get('size')
            cleaned_size = size.replace(" m²", "").strip()
            adapter['size'] = int(cleaned_size) if cleaned_size.isdigit() else 0
        
        # Extract numeric part from 'age' field
        if 'age' in adapter and adapter['age']:
            age = adapter.get('age')
            cleaned_age = age.split()[0].strip()
            adapter['age'] = int(cleaned_age) if cleaned_age.isdigit() else None

        # Convert 'date' field to a datetime object
        if 'date' in adapter and adapter['date']:
            date_str = adapter.get('date')
            try:
                adapter['date'] = datetime.strptime(date_str, '%d-%m-%Y').date()  # Assuming format is 'day-month-year'
            except ValueError:
                adapter['date'] = None  # Handle invalid date formats

        return item

class SaveToMySQLPipeline:
    def open_spider(self, spider):
        # Establish connection to the MySQL database
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='master',
            password='123456',
            database='real-estate'
        )
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS realestate (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                price INT NOT NULL,
                currency VARCHAR(10) NOT NULL,
                property_type VARCHAR(100),
                rooms VARCHAR(50),
                size INT,
                age INT,
                floor VARCHAR(50),
                date DATE,
                image_url TEXT,
                agency_logo TEXT
            );
        """
        self.cursor.execute(create_table_query)

    def process_item(self, item, spider):
        # Prepare the SQL query for inserting the scraped data into MySQL
        insert_query = """
            INSERT INTO realestate (title, price, currency, property_type, rooms, size, age, floor, date, image_url, agency_logo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Extract item values
        values = (
            item.get('title', None),
            item.get('price', 0),  # Integer
            item.get('currency', ''),
            item.get('property_type', ''),
            item.get('rooms', ''),
            item.get('size', 0),  # Integer
            item.get('age', None),  # Integer (can be NULL)
            item.get('floor', ''),
            item.get('date', None),  # Date (can be NULL)
            item.get('image_url', ''),
            item.get('agency_logo', '')
        )

        # Execute the query
        self.cursor.execute(insert_query, values)
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # Close the connection to the database when the spider is closed
        self.cursor.close()
        self.conn.close()
