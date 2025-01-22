# Landing Page with CMS

This project was created as part of my University course in 2022 and was deployed by a real company for a year. This is a landing page to promote a company service, with the options to add information through the Wagtail CMS.

## Characteristics

The technologies in this project are:
- Django REST Framework
- Django Wagtail CMS
- Docker container
- HTML
- CSS
- JavaScript

## Installation
### Step 1
To clone this repo, use the following command:

```bash
git clone https://github.com/EdgarCarrilloEstrada/Landing-page-with-CMS.git
```

### Step 2
Go to "grupolias" folder and look for the Dockerfile

```bash
cd grupolias
```
### Step 3
Inside "grupolias" folder, the Dockerfile and requirements.txt are found and are necessary to run this project. The command to create the docker image for this project is:

```bash
docker build -t docker-image-name .
```

Once this command is executed, it will automatically install all the requirements listed in the txt file.
