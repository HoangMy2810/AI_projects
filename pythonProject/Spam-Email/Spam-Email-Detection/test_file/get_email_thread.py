import asyncio
from email import policy

from aioimaplib import aioimaplib, STOP_WAIT_SERVER_PUSH


async def check_mailbox(host, user, password):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()

    await imap_client.login(user, password)

    res, data = await imap_client.select()
    print('there is %s messages INBOX' % data[0])

    await imap_client.logout()


async def fetch_emails(host, userName, password):
    """
        Get emails from server
        """
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()
    await imap_client.login(userName, password)
    await imap_client.select('Inbox')

    status, data = await imap_client.search('(UNSEEN)')

    # for each e-mail messages, print text content
    for num in data[0].split():
        # get a single message and parse it by policy.SMTP (RFC compliant)
        status, data = bytes(await imap_client.fetch(num, '(RFC822)'))
        email_msg = data[0][1]
        email_msg = await imap_client.message_from_bytes(email_msg, policy=policy.SMTP)

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


async def wait_for_new_message(host, user, password):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    await imap_client.wait_hello_from_server()

    await imap_client.login(user, password)
    await imap_client.select()

    idle = await imap_client.idle_start(timeout=10000)
    while imap_client.has_pending_idle():
        msg = await imap_client.wait_server_push()
        print(msg)
        if msg == STOP_WAIT_SERVER_PUSH:
            imap_client.idle_done()
            await asyncio.wait_for(idle, 1)

    await imap_client.logout()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_mailbox('imap.gmail.com', 'tduong.hust02@gmail.com', 'wkbnazljcpnklukb'))
    loop.run_until_complete(fetch_emails('imap.gmail.com', 'tduong.hust02@gmail.com', 'wkbnazljcpnklukb'))
