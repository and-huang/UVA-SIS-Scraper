import requests
import sys
import smtplib, ssl
from time import sleep
from email.mime.text import MIMEText


def internet_connection():
    try:
        requests.get("https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1242&page=1", timeout=20)
        return True
    except requests.ConnectionError:
        return False    


def main():
    clist = [('CS','3140', "LEC"), ('CS','3140' "LEC"), ('CS','3130', 'LEC'), ('STAT', "1620", "LEC")]
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1242&page=1'
    # Replace 1228 with the appropriate term. The formula is “1” + [2 digit year] + [2 for Spring, 8 for Fall]. 
    # For example, 1228 is Fall 2022. 
    # See the README for more information on API usage
    notifiedClasses = []    
    while True:
        openClasses = ''
       
        for c in clist:
            r = requests.get(url + '&subject=' + c[0] + '&catalog_nbr=' + c[1])
            for classInfo in r.json():
                # print(c['subject'], c['catalog_nbr'] + '-' + c['class_section'], c['component'], c['descr'], \
                #         c['class_nbr'], c['class_capacity'], c['enrollment_available'])
                if classInfo['enrollment_available'] != 0 and c[2] == classInfo['component'] and classInfo['class_nbr'] not in notifiedClasses:
                    courseName = classInfo['subject'], classInfo['catalog_nbr'] + '-' + classInfo['component'], classInfo['descr']
                    seatsOpen = str(classInfo['enrollment_available'])
                    res = ' '.join(map(str, courseName))
                    openClasses += res
                    openClasses += " has " + seatsOpen + " seats available."+ '\n'
                    notifiedClasses.append(int(classInfo['class_nbr']))

                    sendMail(openClasses)
                    sleep(500)

#replace with your details
def sendMail(openClasses):
    port = 0 #usually a 3 digit number
    smtp_server = "" #ex. smtp.gmail.com
    sender_email = ""
    receiver_email = ""
    password = "" #for gmail, https://support.google.com/mail/answer/185833?hl=en

    msg = MIMEText(f'Seats are now available in the follwing classes: \n {openClasses}')
    msg['Subject'] = 'Seats are now available in the follwing classes:'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()


if __name__ == '__main__':
        if internet_connection():
            main()
        else:
            sys.exit("Connection error: Check your internet connection or computer power.")
