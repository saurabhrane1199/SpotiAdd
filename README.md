# SpotiAdd
Google Chrome Extension to add the song playing on youtube website to spotify playlist. Uses youtube data api and spotify apis to perform this task

## Steps to run (Backend)
1. Create a python file and name it "secret.py"
2. Register the app with spotify developers console and get client_secret and client_id and store it in variables in secret.py
3. Enable youtube api on google cloud console and get youtube api developer key and store it in secret.py

The secret.py file should look like this.
![Secret.py](https://user-images.githubusercontent.com/36326161/83817479-7f7dec00-a6e2-11ea-980d-355bdee48051.png)

5. Install all the dependencies using requirements.txt

6. Run app.py file

## Steps to load extension
1. Open Chrome
2. Go to chrome://extensions enable developer mode
3. Click on Load Unoacked Extension
4. and select the frontend folder

### You might have to edit the callback and redirect url as per your extension id
### Checkout the screenshots folder to see the working of the extension
