# Setting Up Ada Fruit Bot

## Part 1 Creating a Google Cloud Project with OAuth 2.0 Client ID <br />
### Introduction <br />
In this subsection, we will walk you through the steps to create a Google Cloud project that uses an OAuth 2.0 Client ID. OAuth 2.0 is an authorization framework that allows you to secure access to resources on behalf of users. By using a Client ID, you can authenticate your application and access Google APIs. <br />

### Prerequisites <br />
1. A Google account. If you don't have one, create one at [accounts.google.com](accounts.google.com).<br />
2. Access to the Google Cloud Console. If you don't have access, you can request it [here](https://console.cloud.google.com/welcome?).<br />
### Step 1: Create a Google Cloud Project <br />
1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome?). <br />
2. Click on the project drop-down and select or create the project that you want to add the OAuth 2.0 Client ID to.<br />
3. Click on the hamburger menu and select APIs & Services > Dashboard.<br />
4. Click on the hamburger menu again and select APIs & Services > Library.<br />
### Step 2: Enable APIs <br />
1. Search for the API that you want to enable for your project. For example, if you want to access the Google Drive API, search for "Google Drive API."<br />
2. Click on the API that you want to enable.<br />
3. Click the "Enable" button.<br />
### Step 3: Create the OAuth 2.0 Client ID <br />
1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome?).<br />
2. Click on the hamburger menu and select APIs & Services > Credentials.<br />
3. Click on the "Create credentials" button and select "OAuth client ID."<br />
4. Select the application type that best fits your application.<br />
5. Enter a name for your application and click the "Create" button.<br />
6. Download the JSON file for your OAuth 2.0 Client ID. You will use this file in your application to authenticate with Google.<br />
### Step 4: Use the OAuth 2.0 Client ID in your application <br />
1. In your application, import the JSON file that you downloaded in Step 3.<br />
2. Use the Client ID to authenticate with Google and access the API that you enabled in Step 2.<br />
### Step 5: Add Client ID Secrets to Package <br />
1. After downloading the google client ID secrets json file move it to the [data/config/](https://github.com/calebmwelsh/AdaFruitBot/tree/main/data/config) directory.<br />
2. No need to rename file, it should look very similar to the sample file in the same directory.<br />
### Conclusion <br />
By following the steps in this guide, you should now have a Google Cloud project that uses an OAuth 2.0 Client ID. This will allow you to authenticate your application and access Google APIs on behalf of users.<br />



## Part 2 Configuration File Setup <br />
### Introduction <br />
In this subseection, we will walk you through the steps to setup the configuration file located here. This configuration file will determine the product you want to automate and will include the credentials for your Ada Fruit account(s).  <br />

### Prerequisites <br />
1. One or more Ada Fruit accounts. If you don't have one, create one at [adafruit.com/](https://www.adafruit.com/).<br />
2. You will also need to enable two factor authentication if you plan to bot more popular items i.e. Raspberry Pi. 
You can enable two factor [here](https://accounts.adafruit.com/users/security)<br />\

### Overview <br />
This file provides information about the config.py file, which contains information for interacting with various platforms and services. The file includes the following sections:

1. selenium: Information for using the Selenium web driver to access a website.
2. gmail: Information for accessing a Gmail account.
3. accounts: Information for accessing two different Ada Fruit accounts, including login information and checkout information.


### Selenium

The selenium section of the creds JSON file includes the following fields:

driver_path: The file path to the Chrome driver executable.
url: The URL of the website that will be accessed using the Selenium web driver.

### Gmail

The gmail section of the creds JSON file includes the following field:

gmail_address: The email address of the Gmail account that will be accessed.

### Accounts

The accounts section of the creds JSON file includes information for two different Ada Fruit accounts. Each account has the following fields:

login_info: Information for logging into the account.
username: The username for the account.
password: The password for the account.
otp: The one-time password for the account.
checkout_info: Information for checking out as a customer.
name: The name to use during checkout.
address: The address to use during checkout.
city: The city to use during checkout.
postal_code: The postal code to use during checkout.
state: The state to use during checkout.
phone_number: The phone number to use during checkout.


#### Note: Replace all fields enclosed in < > with actual values.