#listening email from internet
import imaplib, email, getpass
from email import policy

imap_host = 'imap.gmail.com'
imap_user = 'phamthaiduong526@gmail.com'
imap_pass = 'nzhelooeohpegybw'

#tduong.hust02@gmail.com
imap_pass1 = 'wkbnazljcpnklukb'

# init imap connection
mail = imaplib.IMAP4_SSL(imap_host, 993)
rc, resp = mail.login(imap_user, imap_pass)

# select only unread messages from inbox
mail.select('Inbox')

status, data = mail.search(None, '(UNSEEN)')

# for each e-mail messages, print text content
for num in data[0].split():
    # get a single message and parse it by policy.SMTP (RFC compliant)
    status, data = mail.fetch(num, '(RFC822)')
    email_msg = data[0][1]
    email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

    print("\n----- MESSAGE START -----\n")

    print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
        str(email_msg['From']), \
        str(email_msg['To']), \
        str(email_msg['Date']), \
        str(email_msg['Subject'] )))

    # print only message parts that contain text data
    print("Mail content:\n")
    for part in email_msg.walk():
        if part.get_content_type() == "text/plain":
            for line in part.get_content().splitlines():
                print(line)

    print("\n----- MESSAGE END -----\n")

# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.
while 1:
    # Have to log in/logout each time because that's the only way to get fresh results.

    mail = imaplib.IMAP4_SSL(imap_host, 993)
    rc, resp = mail.login(imap_user, imap_pass)
    mail.select('Inbox')

    status, data = mail.search(None, '(UNSEEN)')

    # for each e-mail messages, print text content
    for num in data[0].split():
        # get a single message and parse it by policy.SMTP (RFC compliant)
        status, data = mail.fetch(num, '(RFC822)')
        email_msg = data[0][1]
        email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

        print("\n----- MESSAGE START -----\n")

        print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
            str(email_msg['From']), \
            str(email_msg['To']), \
            str(email_msg['Date']), \
            str(email_msg['Subject'] )))

        # print only message parts that contain text data
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                for line in part.get_content().splitlines():
                    print(line)

        print("\n----- MESSAGE END -----\n")

    mail.logout()
time.sleep(1)
