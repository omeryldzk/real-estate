# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import re



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
