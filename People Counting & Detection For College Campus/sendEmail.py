
import yagmail

def sendEmail(subject,body):
        try:

            yag = yagmail.SMTP("autoemailsender2@gmail.com", "tczewxnxfrpviped")
            yag.send(to='tummakondaguravareddy@gmail.com', subject=subject, contents=body)
            yag.close()
            print('Mail Send Successfully')
        except Exception as e:
            print('Message not Send Due to  ', e)

def sendEmailtolive(subject,body):
        try:

            yag = yagmail.SMTP("autoemailsender2@gmail.com", "tczewxnxfrpviped")
            yag.send(to='sidhusunny2000@gmail.com', subject=subject, contents=body)
            yag.close()
            print('Mail Send Successfully')
        except Exception as e:
            print('Message not Send Due to  ', e)

