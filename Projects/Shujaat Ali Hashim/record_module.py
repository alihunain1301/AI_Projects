import os
import datetime

class Record:
    def __init__(self, directory_path="C:\\Users\\Syed Usama\\Desktop"):
        self.directory_path = directory_path
        self.today = datetime.date.today().strftime('%d_%m_%Y')
        self.time = datetime.datetime.now().strftime("%H:%M:%S")

    def create_directory(self):
        directory = os.path.join(self.directory_path, 'record')
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory created successfully: {directory}") 
            return directory
        except OSError as e:
            print(f"Error creating directory: {e}") 

    def create_file(self, txt):
        text= txt
        directory_path = self.create_directory()  
        if directory_path:  
            file_path = os.path.join(directory_path, f"{self.today}.txt") 
            try:
                with open(file_path, "a") as file:
                    file.write(f'\nTimestamp: {self.time}')
                    file.write(f'\n {text}')
                print("File created successfully!")
            except Exception as e:
                print(f"Error creating file: {e}")
