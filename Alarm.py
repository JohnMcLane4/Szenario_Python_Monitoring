import smtplib, Monitoring, threading
from _datetime import datetime
from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")

EMAIL_USER = config.get("E-MAIL", "user")
EMAIL_PASSWORD = config.get("E-MAIL", "pw")
EMAIL_SENDER = config.get("E-MAIL", "sender")
EMAIL_RECIPIENT = config.get("E-MAIL", "recipient")
interval = float(config.get("INTERVAL", "seconds"))
cpu_soft_limit = float(config.get("LIMITS", "cpu_soft"))
cpu_hard_limit = float(config.get("LIMITS", "cpu_hard"))
mem_soft_limit = float(config.get("LIMITS", "mem_soft"))
mem_hard_limit = float(config.get("LIMITS", "mem_hard"))
log_file = "logfile.log"


# Hauptfunktion, ruft in Zeitabständen andere Funktionen auf
def schedule():
    check_cpu(),
    check_mem(),
    log_sys(),
    threading.Timer(interval, schedule).start()

# Funktion zum Login und Versand der E-Mails
def send_email(p_subject, p_body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_USER, EMAIL_PASSWORD)

        subject = p_subject
        body = p_body

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg)


# Überprüft ob CPU Soft-/Hardlimit überschritten wurde, gibt diese aus und ruft im Bedarfsfall "send_email" auf
def check_cpu():
    print("CPU Usage: " + str(Monitoring.psutil.cpu_percent()) + "%")
    if cpu_soft_limit <= Monitoring.psutil.cpu_percent() < cpu_hard_limit:
        send_email("Monitoring Alarm: high values reached", "CPU utilization is at: " + str(Monitoring.psutil.cpu_percent()) + "%")
    elif Monitoring.psutil.cpu_percent() >= cpu_hard_limit:
        send_email("Monitoring Alarm: critical values reached", "CPU utilization is at: " + str(Monitoring.psutil.cpu_percent()) + "%")


# Überprüft ob RAM Soft-/Hardlimit überschritten wurde, gibt diese aus und ruft im Bedarfsfall "send_email" auf
def check_mem():
    print("Main memory usage: " + str(Monitoring.psutil.virtual_memory().percent) + "%")
    if mem_soft_limit <= Monitoring.psutil.virtual_memory().percent < mem_hard_limit:
        send_email("Monitoring Alarm: high values reached", "Main memory allocation is at: " + str(Monitoring.psutil.virtual_memory().percent) + "%")
    elif Monitoring.psutil.virtual_memory().percent >= mem_hard_limit:
        send_email("Monitoring Alarm: critical values reached", "Main memory allocation is at: " + str(Monitoring.psutil.virtual_memory().percent) + "%")

# Schreibt CPU und RAM Nutzung in eine Logdatei
def log_sys():
    with open(log_file, "a") as f:
        f.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " CPU utilization: " + str(Monitoring.psutil.cpu_percent()) + "%" + "\n")
        f.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " Main Memory allocation: " + str(Monitoring.psutil.virtual_memory().percent) + "%" + "\n")
        f.close()

schedule()
