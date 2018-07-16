Wedding Gallery, A project for anchor loans hiring process.
===============

About the project
-----------------
To build the project i used mainly the technologies below:
- VS Code, Python 3.6, Pyramid framework, SQLAchemy, boto3, python-decouple, paginate, pytest, amazon s3, pylint, autopep8, isort, bootstrap, jquery

It is a web project based in MVC architecture.


Some tips about the application and How to Use
----------------------------------------------

To use the project access that link: https://wedding-gallery-anchor.herokuapp.com.

>The application don't have any photo, you must upload, approve and etc.

>In the end of this file has some images of the application.

Two users are already created, husband and wife, they have admin permissions and  only them have that permission.
```
Husband user: name: husband, password: admin
```
```
Wife user: name: wife, password: admin
```
They can see the photos, like photos, upload photos(their photos not need approvement) and them approve photos from non admin users.

In home page, If don't have any photo a message is showed explain that,
so you need upload one or see if have any to be approved.
Photos are showed in groups of three ordered by number of likes. Each in a card with the image, description, like button, number of likes and date. More then that will be paginated.
To see the better the image just click in the image in the card.
To like phot just click in like button. To revert the like click again.

To upload a photo they need click in `upload` button in  navigation bar.
To see photos that need to be approved just click in
`drop down menu` where a username is showed and then select `Approve Photos`. So they can see a list of photos with: a thumbnail, who upload that photo, a description about it and a button to approve it.
To see the photo better just click in thumbnail.
If don't have any photo to be approved a message is showed in `Approve Photos` page explain that.

Other users to upload, see and like photos they need to register.
Just click in `Sign up` button.
They have basic permission, and they have their photos approved by admin users.


How Run Locally
---------------

- Clone project

    git clone https://github.com/anderson89marques/anchor_loans_challenge.git

- Change directory into your newly created project.

    cd anchor_loans_challenge

- Simply create a .env text file on your repository's root directory in the form:
```console
AWS_ACCESS_KEY_ID=YOUR-AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR-AWS_SECRET_ACCESS_KEY
BUCKET_NAME=YOUR-S3-BUCKET-NAME
REGION=sa-east-1
```
>Without that the application don't work because it will not comunicate with amazon s3

>And you need of the bucket already created.

>If you don't want create the .env file you can put in environment variables.

- Create a Python virtual environment.

    python3 -m venv env

- Activate your virtual enviroment
    
    Ex: source env/bin/activate

- Upgrade packaging tools.

    pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    pip install -e ".[testing]"

- Configure the database.

    initialize_wedding_gallery_db development.ini

- Run your project's tests.

    pytest

- Run your project.

    pserve development.ini

Some screenshots
----------------

![Alt text](doc_images/home.png?raw=true "Home")

![Alt text](doc_images/photo_clicked.png?raw=true "photo clicked")

![Alt text](doc_images/approve_page.png?raw=true "approve page")

![Alt text](doc_images/upload_page.png?raw=true "approve page")

That's it.

Thank you for the opportunity.