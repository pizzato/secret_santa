import random
import sys
import getpass
import re

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

N_TRIES_NO_WITHIN_GROUP = 1000
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def read_users(fn):
    line_re = re.compile(r'^([^\<]+)\s+?\<([^\>]+)>\s+?(.+?)$')

    with open(fn) as fi:
        user_groups = {}
        user_emails = {}
        for line in fi:
            group = line_re.match(line.strip())
            if not group:
                print("Error in line: ", line)
                return {}, {}

            name, email, group = group.groups()
            name = name.strip()
            group = group.strip()

            if name not in user_groups:
                user_groups[name] = group
                user_emails[name] = email
    return user_groups, user_emails


def draw(do_groups):
    pick_from_same_group = False
    previous_group = None
    pick_groups = dict(do_groups)

    pick_order = []
    while len(pick_groups) > 0:
        pick_list = [u for u, g in pick_groups.items() if g != previous_group]
        if len(pick_list) == 0:
            pick_from_same_group = True
            pick_list = pick_groups.keys()

        picked = random.sample(pick_list, 1)[0]
        pick_order.append(picked)

        previous_group = pick_groups[picked]
        del pick_groups[picked]

    pick_order.append(pick_order[0])
    return pick_order, pick_from_same_group



def send_email(name, email_address, name_match,
               gmailsender, gmailpassword,
               email_subject="Secret Santa"):

    print("Sending email to "+ name, email_address)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = gmailsender
    msg['To'] = email_address

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi {name}\n\n".format(name=name)
    text += "You are the secret santa for: {name_match}\n\n".format(name_match=name_match)
    text += " -- This is an automated email created using: https://github.com/pizzato/secret_santa -- "

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    #part2 = MIMEText(html, 'html')

    msg.attach(part1)
    #msg.attach(part2)

    if gmailsender != "":
        # Send the message via local SMTP server.
        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        s.ehlo()
        s.starttls()
        s.ehlo
        s.login(gmailsender, gmailpassword)

        s.sendmail(gmailsender, email_address, msg.as_string())

        s.quit()



def main():
    if len(sys.argv) != 2:
        print("USE {} <user email group file>".format(sys.argv[0]))
        sys.exit(0)

    user_groups, user_emails = read_users(sys.argv[1])

    # try to obtain a pick that doesn't select within the same group 100 times, otherwise use the last pick
    for i in range(N_TRIES_NO_WITHIN_GROUP):
        pick_order, pick_from_same_group = draw(user_groups)
        if not pick_from_same_group:
            break


    if input("Do you want to see the pick? (Y/N) ").upper() == 'Y':
        print(' -> '.join(pick_order))

    print("Make sure you use application specific password if you have 2FA enable")

    gmailsender = input("Gmail address:")
    gmailpassword = getpass.getpass("Gmail password:")

    for i in random.sample(range(len(pick_order)-1), len(pick_order)-1):
        send_email(pick_order[i], user_emails[pick_order[i]], pick_order[i+1], gmailsender, gmailpassword)

    print("Done - all emails sent")

if __name__ == "__main__":
    main()
