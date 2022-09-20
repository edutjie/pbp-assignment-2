# Assignments 1: Data Delivery Implementation using Django

**Nama:** Eduardus Tjitrahardja

**NPM:** 2106653602

**Kelas:** D

**Link:** [Deployed Heroku Website](https://edutjie-pbp-2.herokuapp.com/mywatchlist/)

## JSON vs XML vs HTML

**HTML** (Hyper Text Markup Language) and **XML** (Extensible markup language) both would wrap content in tags, but **XML** has more strict regarding which tags could be used when and where. Therefore, **XML** is usually responsible for sending and receiving datas and **HTML** is usually responsible for formatting and displaying the data. **JSON** (JavaScript Object Notation) serves similar purpose to **XML**, but **JSON** is more popular than **XML** because web applications are developed using languages such as JavaScript and **JSON** is a way of structuring information in a way that can more easily and fluently interact with these languages.

## Why do we need data delivery in a platform?

A platform may use data from many ends, so we need to have data delivery to make it easier to send data accross many platforms. Since that is the way computer communicate with each other.

## Step by step in making this assignment

1.  Create a mywatchlist app if it doesn't already exist. Using `python manage.py startapp mywatchlist`
2.  Append "mywatchlist" to the `INSTALLED_APPS` list in `project_django/settings.py`.

        INSTALLED_APPS = [
            ...
            'mywatchlist',
        ]

3.  Create a `MyWatchList` model in `models.py`.

        from django.core.validators import MaxValueValidator, MinValueValidator

        class MyWatchList(models.Model):
            watched = models.BooleanField(default=False)
            title = models.CharField(max_length=255)
            rating = models.IntegerField(
                validators=[MaxValueValidator(5), MinValueValidator(1)]
            )
            release_date = models.DateField()
            review = models.TextField()

    After making changes on the model, you have to run `python manage.py makemigrations` and `python manage.py migrate` to migrate your model changes to the database.

4.  Create a json in `mywatchlist/fixtures/` called `initial_mywatchlist_data.json` and fill it with a list of dummy objects. For example:

        [
            {
                "model": "mywatchlist.mywatchlist",
                "pk": 1,
                "fields": {
                    "watched": true,
                    "title": "Thor Ragnarok",
                    "rating": 5,
                    "release_date": "2017-10-25",
                    "review": "Exciting, funny, and above all fun."
                }
            },
            ...
        ]

5.  Create a `show_watchlist_html`, `show_watchlist_json` and `show_watchlist_xml` function in `views.py`.

        from mywatchlist.models import MyWatchList

    It uses `MyWatchList` model to retrieves data from the database (in this case `fixtures/initial_catalog_data.json`).

        def show_watchlist_html(request):
            return render(
                request,
                "mywatchlist.html",
                {
                    "name": "Eduardus Tjitrahardja",
                    "student_id": "2106653602",
                    "watchlist": watchlist,
                },
            )

    `show_watchlist_html` renders the `mywatchlist.html` template with the data retrieved from the database and name, student_id.

        def show_watchlist_json(request):
        return HttpResponse(
            serializers.serialize("json", watchlist), content_type="application/json"
        )

    `show_watchlist_json` renders a json formatted data with the data retrieved from the database.

        def show_watchlist_xml(request):
        return HttpResponse(
            serializers.serialize("xml", watchlist), content_type="application/xml"
        )

    `show_watchlist_xml` renders a xml formatted data with the data retrieved from the database.

6.  Append katalog path to `urlpatterns` list in `project_django/urls.py`.

        urlpatterns = [
            ...
            path("mywatchlist/", include("mywatchlist.urls")),
        ]

    This will create a path from the base path to the "mywatchlist" app.

7.  Create `app_name` and `urlpatterns` in `mywatchlist/urls.py`.

        from mywatchlist.views import show_watchlist_html, show_watchlist_json, show_watchlist_xml

        app_name = "katalog"
        urlpatterns = [
            path("html/", show_watchlist_html, name="show_watchlist_html"),
            path("json/", show_watchlist_json, name="show_watchlist_json"),
            path("xml/", show_watchlist_xml, name="show_watchlist_xml"),
        ]

    This will create a path from `/mywatchlist` that calls `show_watchlist_html`, `show_watchlist_json` and `show_watchlist_xml`.


8. 
- Use the return data from the `show_watchlist_html` function and create a template html to be rendered.
- Create `mywatchlist.html` file in `mywatchlist/templates/`.
- Fill the file with:

         {% extends 'base.html' %}
         {% block content %}
         {% load customtags %}

         <h1>Assignment 3 PBP</h1>

         <h5>Name:</h5>
         <p>{{ name }}</p>

         <h5>Student ID:</h5>
         <p>{{ student_id }}</p>

         <h5>Message:</h5>
         {% if watchlist|count_watched >= watchlist|count_not_watched  %}
             <p style="color:green;">
                 {{ "Selamat, kamu sudah banyak menonton!" }}
             </p>
             {% else %}
             <p style="color:red;">
                 {{ "Wah, kamu masih sedikit menonton!" }}
             </p>
         {% endif %}
         <table>
         <tr>
             <th>Watched</th>
             <th>Title</th>
             <th>Rating</th>
             <th>Release Date</th>
             <th>Review</th>
         </tr>
         {% for movie in watchlist %}
         <tr>
             <td>{{movie.watched}}</td>
             <td>{{movie.title}}</td>
             <td>{{movie.rating}}</td>
             <td>{{movie.release_date}}</td>
             <td>{{movie.review}}</td>
         </tr>
         {% endfor %}
         </table>

         {% endblock content %}

- Create custom tags that's being used in the template above:

  - Create `customtags.py` in `mywatchlist/templatetags/`.
  - Fill the file with:

        from django import template

        register = template.Library()


        @register.filter
        def count_not_watched(value):
            return sum([not i.watched for i in value])


        @register.filter
        def count_watched(value):
            return sum([i.watched for i in value])

9. Create a Test Unit:
   - Create `tests.py` in `mywatchlist/`
   - Fill it with:  

            from django.test import TestCase, Client
            from django.urls import reverse

            class MyWatchListResponseTest(TestCase):
                def setUp(self):
                    self.client = Client()

                def test_url_html_exists(self):
                    response = self.client.get(reverse("mywatchlist:show_watchlist_html"))
                    self.assertEqual(response.status_code, 200)
                
                def test_url_json_exists(self):
                    response = self.client.get(reverse("mywatchlist:show_watchlist_json"))
                    self.assertEqual(response.status_code, 200)

                def test_url_xml_exists(self):
                    response = self.client.get(reverse("mywatchlist:show_watchlist_xml"))
                    self.assertEqual(response.status_code, 200)

    
10. To load the data from `katalog/fixtures`, run this command:

        python manage.py loaddata initial_catalog_data.json

11. Replace `Procfile`'s release with

        release: sh -c 'python manage.py migrate && python manage.py loaddata initial_catalog_data.json && python manage.py loaddata initial_mywatchlist_data.json'

    so it will load `initial_mywatchlist_data.json` when deployed in Heroku.

12. Deploy the project using Heroku
    - Go to Heroku, create a new app
    - Go to the Heroku settings and copy your `API Key`
    - Go to your github repository
      - Go to `Settings > Secrets > Actions`
      - Create two new repository secret
        - `HEROKU_API_KEY`: your API key from Heroku
        - `HEROKU_APP_NAME`: your app name in Heroku
    - Push your changes to your github repository if you haven't already
    - Go to Actions in your github repository
      - Run/Re-run all jobs
    - Done!
      - Your Django project should've been deployed.
      - Mine: [edutjie-pbp-2.herokuapp.com](https://edutjie-pbp-2.herokuapp.com)

## Postman Responses

### HTML Response
![postman-html](/images/postman-html.png)

### JSON Response
![postman-json](/images/postman-json.png)

### XML Response
![postman-xml](/images/postman-xml.png)
