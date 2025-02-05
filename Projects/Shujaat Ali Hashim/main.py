import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize,Qt
from record_module import Record
from web_driver_module import WebDriver
from conversation_module import conversation
import threading
import time
import ai

class MainWindow(QMainWindow,conversation,Record,WebDriver):
    def __init__(self):
        super().__init__()
        conversation.__init__(self) 
        Record.__init__(self)  
        WebDriver.__init__(self)
        self.setWindowTitle("VBVA")
        self.setGeometry(880, 30, 400, 600)
        self.setStyleSheet("background-color: black;")
        self.image_path = "C:/Users/Syed Usama/Desktop/Project/assets/"

        # Speaking and accent states initialization
        self.is_male_accent = True
        self.is_listening= False
        self.ai_speaking=False


        # initializing write methode, web driver
        self.record=Record()
        self.search=WebDriver()

        # Microphone button
        self.speak_button = QPushButton(self)
        self.speak_button.setGeometry(350, 10, 40, 40)

        #ai microphone button 
        self.ai_speak_button= QPushButton(self)
        self.ai_speak_button.setGeometry(350, 60, 40, 40)


        # Accent button
        self.accent_button = QPushButton(self)
        self.accent_button.setGeometry(300, 10, 40, 40)

        # Assistant logo label
        self.ai_logo_label = QLabel(self)
        self.ai_logo_label.setGeometry(150, 250, 100, 100)

        self.text_label=QLabel(self)
        # self.text_label.setGeometry(0,350,400,250)

        self.initUI()
        
        
        

    def initUI(self):
        # Microphone button icons
       
        mic_pixmap_not_speaking = QPixmap(self.image_path + "microphone.png")
        mic_pixmap_speaking = QPixmap(self.image_path + "microphone (1).png")

        self.mic_icon_not_speaking = QIcon(mic_pixmap_not_speaking)
        self.mic_icon_speaking = QIcon(mic_pixmap_speaking)

        self.speak_button.setIcon(self.mic_icon_not_speaking)
        self.speak_button.setIconSize(QSize(25, 25))

        #ai_microphone speak button
        ai_mic_not_speaking_pixmap = QPixmap(self.image_path + "voice (1).png")
        ai_mic_speaking_pixmap=QPixmap(self.image_path + "voice.png")
        
        self.ai_mic_not_speaking_pixmap = QIcon(ai_mic_not_speaking_pixmap)
        self.ai_mic_speaking_pixmap = QIcon(ai_mic_speaking_pixmap)

        self.ai_speak_button.setIcon(self.ai_mic_not_speaking_pixmap)
        self.ai_speak_button.setIconSize(QSize(25, 25))




        # Accent button icons
        accent_pixmap_female = QPixmap(self.image_path + "female.png")
        accent_pixmap_male = QPixmap(self.image_path + "volume.png")

        self.accent_icon_female = QIcon(accent_pixmap_female)
        self.accent_icon_male = QIcon(accent_pixmap_male)

        self.accent_button.setIcon(self.accent_icon_male)
        self.accent_button.setIconSize(QSize(40, 40))

        #text_label ui defination     
        self.text_label = QLabel(self)
        self.text_label.setGeometry(0, 350, 400, 250)
        self.text_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; ")
        self.text_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)  
        self.text_label.setWordWrap(True)
        

        # Assistant logo icons
        self.female_pixmap = QPixmap(self.image_path + "women.png")
        self.male_pixmap = QPixmap(self.image_path + "man.png")

        self.ai_logo_label.setPixmap(self.male_pixmap.scaled(100, 100))
        self.ai_logo_label.setScaledContents(True)
        self.ai_logo_label.setStyleSheet("""
    QLabel {
        border: 3px solid white;  /* Optional: Set the border color and width */
        border-radius: 50px;     /* Half of the width/height to make it circular */
        background-color: black; /* Optional: Background color if image is transparent */
    }
""")
        # Button styles
        button_style = """
            QPushButton {
                border: 2px solid white;
                border-radius: 20px;
            }
        """
        self.speak_button.setStyleSheet(button_style)
        self.accent_button.setStyleSheet(button_style)
        self.ai_speak_button.setStyleSheet(button_style)

        # Connect button actions
        self.accent_button.clicked.connect(self.change_accent)
        self.speak_button.clicked.connect(self.toggle_speaking)
        self.ai_speak_button.clicked.connect(self.toggle_ai)
        

    def change_accent(self):
        """Change the voice accent between male and female."""
        self.toggle_voice() 
        self.text_label.setText('')
        if self.is_male_accent:
            self.accent_button.setIcon(self.accent_icon_female)
            self.ai_logo_label.setPixmap(self.female_pixmap.scaled(100, 100))
            self.text_label.setText('')
            self.text_label.setText("hi, i am powder")
            self.speak('hi, i am powder')
        else:
            self.accent_button.setIcon(self.accent_icon_male)
            self.ai_logo_label.setPixmap(self.male_pixmap.scaled(100, 100))
            self.text_label.setText('')
            self.text_label.setText("hi my name is jeff!")
            self.speak('hi my name is jeff!')
        self.is_male_accent = not self.is_male_accent

    def toggle_ai(self):
        if self.ai_speaking:
            self.ai_speaking= False
            self.ai_speak_button.setIcon(QIcon(self.image_path + "voice (1).png"))
            self.is_listening = False
        else:
            self.ai_speaking=True
            self.ai_speak_button.setIcon(QIcon(self.image_path + 'voice.png'))   
            self.is_listening = True
        threading.Thread(target=self.start_listening).start()    

    def toggle_speaking(self):
        " turn on listening "
        
        if self.is_listening:
            self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
            self.is_listening = False
        else:
            self.speak_button.setIcon(QIcon(self.image_path + "microphone (1).png"))
            self.is_listening = True
            threading.Thread(target=self.start_listening).start()
           
    def start_listening(self):
        if not self.ai_speaking:
            while self.is_listening:
                self.speak_button.setIcon(QIcon(self.image_path + "microphone (1).png"))
                text=self.listen()
                self.record.create_file('User: '+ text)
                
                if 'search' in text:
                    text=text.replace('search','').strip()
                    if 'for' in text:
                        text=text.replace('for','').strip()

                    self.text_label.setText(f"{text}")
                    time.sleep(2)
                    self.text_label.setText(' ')    
                    self.text_label.setText(f"sure sir, searching for {text}")
                    self.speak(f"sure sir, searching for {text}")
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
                    # self.search.get_info(text)
                    threading.Thread(target=self.search.get_info(text)).start()

                elif "play" in text:
                
                    text= text.replace('play',' ').strip()
                    self.text_label.setText(f"play {text}")
                    time.sleep(2)
            
                    self.text_label.setText(' ')    
                
                    self.text_label.setText(f"sure sir, playing {text}")
                    self.speak(f"sure sir, playing {text}")
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
                    # self.search.play_yt(text)
                    threading.Thread(target=self.search.play_yt(text)).start()
    
                elif 'launch' in text:
                    site_name=text.replace('launch',' ').strip()

                    self.text_label.setText(f"{text}")
                    time.sleep(2)
                    self.text_label.setText(' ') 
                    self.text_label.setText(f"sure sir, launching {site_name}")

                    self.speak(f"sure sir, launching {site_name.lower()}")
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
                    self.search.web_launcher(site_name)

                elif 'time' in text:
                    now=self.time
                    self.text_label.setText(f"{text}")
                    time.sleep(2)
                    self.text_label.setText(' ') 
                    self.text_label.setText(f"sure sir, time is {now}")
                    
                    self.speak(f"sure sir, time is {now}")
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
                
                elif 'date' in text or 'day' in text:
                    now=self.today
                    now= now.replace('_'," ").strip()
                    self.text_label.setText(f"{text}")
                    time.sleep(2)
                    self.text_label.setText(' ') 
                    self.text_label.setText(f"sure sir, date is {now}")
                    
                    self.speak(f"sure sir, today date is {now}")
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
                
                elif 'stop' in text:
                    self.text_label.setText('sure call me back when you need me :) ') 
                    self.speak("Sure call me back when you need me :)")
                    self.is_listening=  not self.is_listening
                    self.speak_button.setIcon(QIcon(self.image_path + "microphone.png"))
        else:
            while self.ai_speaking:
                self.is_listening = not self.is_listening
                self.ai_speak_button.setIcon(QIcon(self.image_path + "voice.png"))
                text=self.listen()
                self.record.create_file('User: '+ text)
                self.text_label.setText(f"{text}")
                response=ai.ai_convo(text)
                self.record.create_file('AI: '+ response)
                time.sleep(2)
                self.text_label.setText(" ")
                self.ai_speak_button.setIcon(QIcon(self.image_path + "voice (1).png"))
                self.text_label.setText(response); 
                self.speak(response)
                self.record.create_file(response)
                print(response)





def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()