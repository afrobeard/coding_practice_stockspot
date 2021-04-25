## Preamble

Developed on Python3.9 and Django3.2

## To Run

- Install Docker & Docker Compose

Get the database up
```shell
docker-compose up
```

In another terminal window run the test suite
```shell
pip install -r requirements.txt
python manage.py test
```

Review the fruit_classification.csv before proceeding. This contains the classification fruit or vegetable for the favourite foods provided in the sample file. If you're using a different file, this will need to be modified because its the definition of what is a fruit and what is a vegetable.

Migrate, load data and run server
```shell
python manage.py migrate
python manage.py add_companies --json_file=stockspot-backend-challenge/resources/companies.json
python manage.py add_people --json_file=stockspot-backend-challenge/resources/people.json
```

Setup an Admin User. Some custom views have been created for you
```shell
python manage.py createsuperuser  # Supply username, email & password
```

Start the dev server
```shell
python manage.py runserver
```

You may login to admin http://127.0.0.1:8000/admin/ and explore through the data with custom views
or you may begin using the api.

## API Documentation


###/api/company_employees/

|Get Parameter | Description|
--- | --- 
|company_id | **Required**. ID of the company|
|Get Parameter | Description|


###/api/person_fruits_and_vegetables

|Get Parameter | Description|
--- | --- 
|person_id | **One of person_id or guid is required**. Persons Identifier|
|guid | **One of person_id or guid is required**. GUID|

###/api/blue_eyed_living_common/

|Get Parameter | Description|
--- | --- 
|person_id1 | **One of person_id1 or guid1 is required**. Persons Identifier|
|guid1 | **One of person_id1 or guid1 is required**. GUID|
|person_id2 | **One of person_id2 or guid2 is required**. Persons Identifier
|guid2 | **One of person_id2 or guid2 is required**. GUID|


## Code Formatting

We use black for Code Formatting. Since black is consistent and used by https://github.com/psf/black#used-by

#### BLACK Setup

```sh
pip3 install black
which black
/Library/Frameworks/Python.framework/Versions/3.8/bin/black
```

###### To run black manually

```sh
black radar
```

###### To re-configure your editor

The following instructions are for Pycharm, but theres no magic here, you should be able to use these with whatever 
editor you prefer to use, or you can configure an external file watcher using fswatch / inotify-tools, etc

Configure File Watcher (Pycharm > Preferences > File Watchers)
- **Add File Watcher**
- Name: Black
- File Type: Python
- Scope: Project Files
- Program: <Path from which>
- Arguments: $FilePath$
- Outputs Paths to Refresh: $FilePath$
- Auto-save edited files to trigger the Watcher: Uncheck

Configure External Tools (Pycharm > Preferences > External Tools)
- **Add External Tool**
- Name: Black
- Program: <Path from which>
- Arguments: $FilePath$

To run on demand Tools -> External Tools -> black

## Static Analysis

For reliability, security & maintainability in addition to autoformatting, Static Analysis is great.

Rules https://rules.sonarsource.com/python
Instructions available here: https://www.sonarlint.org/ (Click link for intellij idea if you're using PyCharm)
