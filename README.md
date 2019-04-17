![Localized](frontend/logo-black.png)

# Test project for Localized

Demo: [http://localized.leolara.me/](http://localized.leolara.me/)

## Choosen stack

 + Python 3.6
 + Sqlite
 + Django 2.2 with rest framework
 + Vue

## Assumptions and some decisions

The project says that there are hundreds of courses, which is small and potentially we could send it all to the client and doing all filtering and ordering at the client.

Doing it client side pros: in a modern smartphone or computer sorting, ordering, pagination will be faster, server side code is trivial

Doing it client side in the cons: the loading time will be slightly slower, which will be noticeable on a slow connection, also data manipulation could be slow on a old smartphone, client side code is trivial

Doing it server side pros: even if there number of courses grow to thousands the same general solution will still work

Doing it server side cons: more complex server side and communication with client side

Eventually, I decided to do it server side for an external reason, the fact that I need to show some server side code, and doing it client side it would have made server side code trivial. The server would just have sent back a json file to the client. Also, due to Localized mission perhaps some Localized users can be from countries with slow internet speed and/or have smartphones.

It is vague what "times" means exactly, to keep it simple I assume it is an hour written hh:mm in 24h format from 08:00 11:00 and from 13:00 to 18:00. For the sample data I only use o'clock times. Hence, I use lexicography ordering for this. It might have been implemented as a date or timestamp DB field, but for keeping it simple I think this is better for the purpose of this test.

## Data model organization

The main entity is the Course. It contains a name (a string) and a cost a number.

To keep it simple we have cost as an integer, if cents are necessary we can assume that the number stored is the number of cents, not dollars, and in that case transform it accordingly at the presentation layer.

The course name is a string and probably it should be unique and I have set it as such.

Then courses also has relations professor and times.

Times seems to be either a many to many with courses, or a multiple attribute of courses. Either way, time as entity has no attributes, for the exercise at practical level it should be implemented with a table with a foreign key to courses and the time as a string.

If you see time as an entity the string time would be its primary key, but it is not necessary to create a third table as there are no additional attributes. I explain this because usually many to many result in an intermediate table, resulting in three total tables, where here we have two.

Professor seems at a high level to be a one professor can have many courses relationship. However, to keep it simple and because we already are using relational data with times we leave it as a string attribute of courses entity. This can be seen as denormalized but it would have made no sense to create another table as professor has no additional attributes.

These are implemented with Django models.

```
class Course(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    professor = models.CharField(max_length=200, null=False, blank=False)
    cost = models.IntegerField()

    def __str__(self):
        return self.name + " "

class Time(models.Model):
    hour = models.CharField(max_length=5)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="times")

    class Meta:
        unique_together = ("hour", "course")

    def __str__(self):
        return self.hour
```

I commit a sqlite file in the repository with sample data, for the purpose of this exercise. This is not appropiate in general.

## Performance

I have not added indexes to the database to keep it simple for the exercise and because the number of courses is bound. In a normal scenario indexes would be a must and also some type of caching.

## Tests

I have written 4 functional tests to test the API. Of course, we should test all filters, ordering and combination of those, but this is also an example.

I would have created a unit test if I had seen the opportunity, but I do not think I am creating in this exercise any isolated unit for which it would have made sense. In a longer project there would be many unit tests.

## Front-end

I have developed this in Vue with a vuetify grid. I took an example of a grid and modify it. The code retrieving the date from the API is completely of my doing.

There is no much to it apart of the code calling the API and processing the returned data. The markup code is pretty much the original from the example.

## Installing and running demo

Assuming you have the right version of python and pip installed

Clone repository

in a terminal do:

```
cd backend
pip install -r requirements.txt
python manage.py runserver
```

Migrate is not necessary in this case because the Sqlite DB file is comitted and with seed data.

In the repo there is a sqlite database so the data is seeded. To commit a database is not normal practice. The sample data has two "times" per course, but the this is not a limitation of this software, it can work with 1..n "times".

in another terminal do:

```
cd frontend
python -m SimpleHTTPServer 8080
```

open a browser pointing to localhost:8080

## Known errors, omissions and improvements

In the front-end you can select page size, but if you select "All" it uses page size 10.

API server endpoint is currently hard-coded on the client side, it should be easier to modify it.

Hours that can be selected are hard-coded in the front-end, they should not.

Once the user selects an hour to filter by, the user cannot deselect searching by hour.

When the user types in a search field it automatically request new info to the API, we should wait to see when the user stopped typing.

## Commit history

Usually in these type of tests, commits are created to show a sense of the flow of work. Given that I was learning Django and Vue, the process has been more disorganised than when you have experience with the framework, so creating a commit history was not practical.
