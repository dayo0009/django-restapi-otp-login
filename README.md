Customized Django Login OTP Authentication


Build A Login Form using Email/Phone Number With OTP generated Using Django and Rest API


This mini projects provides guides and code implementation on how to customized a django authentication backend similar to the Google sign-in form using Django and Rest API. 

It also has a simple user phone verification extra security layer for authentication whilst also preserving maximum attempts on the one time password(OTP) for implementation and other flexible reasons.This can be integrated in your app with just a twerk on your model already design or when starting a new project.


Requirements

- Python 3
- Django
- Django REST Framework
- Other required packages are specificied in the requirements.txt


Procedures of implementation for users

- A user must have a prerequisite knowledge of Python/Django and git

- install python3, create a virtual environment and activate.

- use pip to install the requirements (pip install -r requirements.txt)

- Ensure to update your project settings with appropriate configurations include Login authentication model, SMI API KEY, amongst others.

- Ensure you run migration services and resfresh your server


Code Review

- Models: This file definea the django models used in the project

-  Auth: This file stands for form serializer 

- Middleware: This is a file resonponsible for timeout after 5 minutes inactivity on the web app

- Views: Contains Necessasry classes and functions that handle the whole process

- Urls: Contains URL routes and mapping for the application

- Permission: Defines user authentication

- Backend: Contains django customized authentication code


Additional Folder

- Error: This contains invalid errors 

- Success: This contain valid information provided




Contribution

For further improvements, feel free to contribute to this project. You can submit a pull request. 

Thank you!

