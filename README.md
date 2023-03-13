OVERVIEW

This project is a web app that allows users to asynchroniously monitor a video stream, and be notified when a parcel is detected. The user can enter a video stream url and their phone number, and the application will monitor the video and notify the user using sms, and update the alerts on their dashboard. The purpose of this project was to limit package theft from the doorstep, by connecting the application to a ring camera/ ip camera stream.

The project uses open cv to monitor the video stream, and twilio to send automated text messages. Downloadable images of the frame where a package is detected are stored on an AWS S3 bucket, and an RDS Postgresql database is used for the backend.

To run the application, clone the repository and install the dependencies from requirements.txt using pip install -r requirements.txt
