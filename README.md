# Lambda first Project: (study cases)

This project checks the remaining days for SSL certificates of websites defined on webhook_cert/sites.py, and notificate when it's about to expire (10 days left!) on your discord channel and in your e-mail adress.

It's a simple project, but useful in some cases. Anyone who wants to collaborate it's welcome.

# Dependencies:

You need to create a .env on your lambda project with these two variables: 

WEBHOOK_URL=

PASSWORD=

That's the discord webhook URL, and the password from your email.

# How it's works:

You can use the pulumi project inside of this folder, to provision you project automatically in your AWS Cloud Account. You just need to configure your s3 bucket, and s3 key to point to this project with your configurations on your cloud.
