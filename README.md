# BTC Assessors email signatures
This repository is intended to provide the tools to mass-update the email signatures of every user in our Google Suite domain given a generic templates with variables in it.

## Configuration
### The `users.json` file
Allows to specify the users to update and their signature information

The format of the `users.json` file is a key / value map where the user's email is the key and the values to set in their signature are the values.

The values to set in their signature are specified as a key / value map where the key is the name of the variable in the signature file and the value is the value to set for this user in that variable.

The format of this file then depends on the signature file used.

### The signature template `signature.html`
The signature template file is an HTML file that contains a generic signature to be used for all users. In order to specify each users' information, variables inside the signature file are used. Those variables are then parsed by the `jinja2` template module to combine them with the users information specified in the `users.json` file.

Basic variables can be specified using the following `jinja2`'s syntax:
```
{{ name }}
```

Where `name` is the variable's name.

In `users.json` file you must set then for each user, a key named `name` and a value to replace this variable with the users' related information (like his phone, position, location, ...)

### The `update_signatures.py` script
Retrieves the users' information from `users.json` file (constant `USERS_FILE`), loads the HTML template specified in the variable `SIGNATURE_FILE` (inside the folder `SIGNATURE_FOLDER`), and loops all users in the users' file, rendering the template with the user information and applying the rendered result as the email signature in their Gmail account.

> Due to the _Jekyll_ site, the signature is placed in the `_includes` folder so it can be parsed by _Jekyll_. Unlike the _JSON_ file, that can be _symlinked_, this file can't so it must be there if you want to have the _Jekyll_ minisite too.

### Authentication: the `service_account.json` file
#### Creating a _Google APIs_ project
To authenticate against Google API's, you must create a project first in the [Google API's developer console](https://console.developers.google.com/apis). Make sure you are using the Google Suite's account to create this project and the following operations.

#### Creating a _service account_
The authentication used is a _Service account_ (because we need to allow domain-wide authentication in Google Suite after that to change all users' signatures therefore impersonating them). Create a service account in [Google API's developers console](https://console.developers.google.com/apis): ['IAM's and administration -> Service accounts' (to find this menu click on the top left square's three bars button)](https://console.developers.google.com/iam-admin/serviceaccounts/). Copy your _Client Id_, we'll need it later.

#### Creating a credential for this _service account_
Then, we must create a credential for this _service account_. Go to the [credentials page](https://console.developers.google.com/apis/credentials) (`APIs and services -> Credentials` on the same previous menu) and create a _service account_ credential in _JSON_ format. The _JSON_ file will be downloaded to your computer. Rename it as `service_account.json` and place it in the same folder as the repository (the script will look for it with this name).

> Don't worry, our `.gitignore` will prevent a file named `service_account.json` to end uploaded in the repository

#### Granting domain-wide permissions for this _service account_
Finally, go to the [Google Suite's Admin](https://admin.google.com) console. Click on `Security -> Advanced configuration`. Now introduce the _Client Id_ in the _client name_ field. Place the scopes delimited by comma in the _API scopes_ field.

The scopes that this script uses are:
```
https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing
```

#### Ready
You have setup the authentication properly and are ready to go!

## Usage
In order to update all users signatures with the information and users placed in `users.json`, with the generic HTML signature template located in the file specified by the variable `SIGNATURE_FILE` inside the folder `SIGNATURE_FOLDER` in the _Python_ script, please do the following:

1. Check `users.json` is properly formatted and with valid information
2. Ensure the `SIGNATURE_FILE` and `SIGNATURE_FOLDER` variables in the _Python_ script point to the generic HTML signature file
3. Check you have the `service_account.json` obtained from the authentication steps before placed in the current directory of the script.
3. Make sure you can run _Python 2_ and the dependencies in the `requirements.txt` are installed. You can install them with `pip` using `pip install -r requirements.txt`
4. Run the script with `python update_signatures.py`.
5. Check your [Gmail](https://mail.google.com) to see if the signature has been updated. Reload the page to see changes if you had Gmail already opened

## The _Jekyll_ website
A little _Jekyll_ website is also available to show the compiled signatures for each user if they need to copy and paste them to their third party email client.

In order to keep in sync with the generic template, you must check that all variables are reassigned in the file `_includes/index.html`, inside the [_reassignment block_](_includes/index.html#L21-L25). Otherwise your _Jekyll_ site may miss some variables.

Please also check that the variables in the `_config.yml` file are correct.

> Be sure to specify the correct `domain` variable (that must be equal to the users' emails domain) in order to generate valid _ids_ to the DOM elements.

**<> with ♥ in [BTC Assessors](https://www.btcassessors.com), Andorra by [@ccebrecos](https://github.com/ccebrecos) & [@davidlj95](https://github.com/davidlj95)**


![BTC Assessors](https://i.imgur.com/7nzUvR0.png)
