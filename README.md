# Creating a Google Cloud Project with OAuth 2.0 Client ID # <br />
## Introduction <br />
In this guide, we will walk you through the steps to create a Google Cloud project that uses an OAuth 2.0 Client ID. OAuth 2.0 is an authorization framework that allows you to secure access to resources on behalf of users. By using a Client ID, you can authenticate your application and access Google APIs. <br />

## Prerequisites <br />
A Google account. If you don't have one, create one at accounts.google.com.<br />
Access to the Google Cloud Console. If you don't have access, you can request it here.<br />
## Step 1: Create a Google Cloud Project ## <br />
Go to the Google Cloud Console. <br />
Click on the project drop-down and select or create the project that you want to add the OAuth 2.0 Client ID to.<br />
Click on the hamburger menu and select APIs & Services > Dashboard.<br />
Click on the hamburger menu again and select APIs & Services > Library.<br />
## Step 2: Enable APIs <br />
Search for the API that you want to enable for your project. For example, if you want to access the Google Drive API, search for "Google Drive API."<br />
Click on the API that you want to enable.<br />
Click the "Enable" button.<br />
## Step 3: Create the OAuth 2.0 Client ID <br />
Go to the Google Cloud Console.<br />
Click on the hamburger menu and select APIs & Services > Credentials.<br />
Click on the "Create credentials" button and select "OAuth client ID."<br />
Select the application type that best fits your application.<br />
Enter a name for your application and click the "Create" button.<br />
Download the JSON file for your OAuth 2.0 Client ID. You will use this file in your application to authenticate with Google.<br />
## Step 4: Use the OAuth 2.0 Client ID in your application <br />
In your application, import the JSON file that you downloaded in Step 3.<br />
Use the Client ID to authenticate with Google and access the API that you enabled in Step 2.<br />
## Conclusion <br />
By following the steps in this guide, you should now have a Google Cloud project that uses an OAuth 2.0 Client ID. This will allow you to authenticate your application and access Google APIs on behalf of users.<br />
