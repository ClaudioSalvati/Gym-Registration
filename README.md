# Gym-Registration
This script automates the online registration for the ELEMENTS gyms in Germany, as a registration on the day before is mandatory.

## Motivation
As the registration time frame is restrictive and I am very forgetful, I wrote this script to automate the registration, avoiding going there and being sent home because there is no registration in my name.

## Limitations
The code is quite straightforward, but it relies on the assumption that the website code - and the registration way - won't change. The error handling can be improved, as I didn't experience any issue when writing the code, so there are any errors I didn't either face or even think about.
The script sends an email with (few) logs. In case the registration didn't work, then I can still get a reminder and do it manually. This is enough in my case.

## The result
The working script is meant to run automatically on an AWS EC2 machine, each day before a training day, in the given time frame the registrations are open. 
### The Login
Trying to log in using credentials as payload didn't work, so I have them directly in the URL using percent-encoding ("URL encoding").
### Retrieving the Studio Sheet ID
This is is necessary for the registration, and as far as I could observe, it changes day after day - but not within a day. This is why I used scrapy to retrieve it.
In this step, the studio ID is also used. The value is static and can be seen in the HTML code of the /sheet.php site, as well as in the dev tools in the passed data once you select if from the dropdown filter.
### Registering for the next day
Having Studio ID and the Studio Sheet ID, I put the URL together and Voilà! "Sie sind in diesen Kurs eingeschrieben!"
For this step, having the parameters as payload didn't work either, therefore I have them once again in the URL.  
### Email Sendout
To have a notification of the - more or less - successful registration I use Gmail via SMTP. I created a new Gmail account just for this purpose.
Any other SMTP client will probably work, after some adjustments to the script. 

## Credits
The script is the result of several late evening sessions, after I was refused entry to the gym, even though I was sure I had registered online (manually). So without Elements' rejection, this script would not have been written.

## Disclaimer
I offer the code as-is and as-available, and I make no representations or warranties of any kind concerning it, whether express, implied, statutory, or other. This includes, without limitation, warranties of title, merchantability, fitness for a particular purpose, non-infringement, absence of latent or other defects, accuracy, or the presence or absence of errors, whether not known or discoverable.
