# secret_santa

This secret santa script combines family groupings and automatically sends emails to everyone with their picks.

To run the script you must first write a file containing the names, emails and groupings of all participants of the secret santa.

This file must contain one person per line in the following format:

```Name <email> Group Name```

For instance, the following is a valid file format (see example.txt).
```
John Smith <johnemail@email.com> Smith-Family
Mary Smith <johnemail@email.com> Smith-Family
Abe B  <abeemail@email.com>  Abe-Family
Alice <alice@email.com>  Abe-Family
Bob M <bob@email.com> Bob-Family
Cris C <cris@email.com>  Cris-Family
```

To execute the script run:

```bash
python secret_santa.py example.txt
```

Where example is the file with the participants.

The program will run, make a pick, offer to show you the pick (if you are a participant, please say no - otherwise you will know who picked you).

The it will ask for your Gmail username and password. If you want to use another email server, please modify the following lines: 
```
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
```
