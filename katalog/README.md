# Assignments 2: Introduction to Django dan Models View Template (MVT) in Django

**Nama:** Eduardus Tjitrahardja

**NPM:** 2106653602

**Kelas:** D

**Link:** [Deployed Heroku Website](https://edutjie-pbp-2.herokuapp.com/)

## Django Diagram
<br/>

![diagram](/images/diagram.png)

<br/>

The client-side sends a `GET` request to the server-side, in this case Django. Django works as a controller and check to the available resource in URL. The request is passed to the `url.py` and it calls the function in `view.py` that matches the url. That function in `view.py` interacts with `model.py` and retrieve the appropriate data from the database. The View then renders back an appropriate template from `templates/` along with the retrieved data to the user. After all of that, it responds back to the client-side and sends a template as a response.

<br/>

## Why should we use a virtual environment? Can we make a Django project without it?

We can make a Django project without virtual environment, however it might cause conflicts with other projects' requirements. For example, your Django project might require a different version of python from your Flask project. To prevent conflicts and potential errors, it is recommended to use a virtual environment to isolate every project from the other.

Other than that, we should use a virtual environment to make sure that all developers are in the same environment for the same project. It will tackles the possibility of one developer that's developing the same project has different requirements with the others that can cause errors.

<br/>

## Step by step in making this project
1. Create a katalog app if it doesn't already exist.
2. Append "katalog" to the `INSTALLED_APPS` list in `project_django/settings.py`.

        INSTALLED_APPS = [
            ...
            'katalog',
        ]

3. Create a `CatalogItem` model in `models.py`.

        class CatalogItem(models.Model):
            item_name = models.CharField(max_length=255)
            item_price = models.BigIntegerField()
            item_stock = models.IntegerField()
            description = models.TextField()
            rating = models.IntegerField()
            item_url = models.URLField()

4. Create a `show_catalog` function in `views.py`.

        from katalog.models import CatalogItem

        def show_catalog(request):
            catalog = CatalogItem.objects.all()
            return render(
                request,
                "katalog.html",
                {
                    "name": "Your Name",
                    "student_id": "Your Studen ID",
                    "catalogs": catalog,
                },
            )

    It uses `CatalogItem` model to retrieves data from the database (in this case `fixtures/initial_catalog_data.json`). It renders the `katalog.html` template with the data retrieved from the database and name, student_id.

5. Append katalog path to `urlpatterns` list in `project_django/urls.py`.

        urlpatterns = [
            ...
            path("katalog", include("katalog.urls")),
        ]

    This will create a path from the base path to the "katalog" app.

6. Create `app_name` and `urlpatterns` in `katalog/urls.py`.

        from katalog.views import show_catalog

        app_name = "katalog"
        urlpatterns = [
            path("", show_catalog, name="show_catalog"),
        ]

    This will create a path from `/katalog` that calls `show_catalog`.

7. 
   - Use the return data from the `show_catalog` function and create a template html to be rendered.
   - Create `katalog.html` file in `katalog/templates`.
   - Fill the file with:
  
            {% extends 'base.html' %}
            {% block content %}

            <h1>Lab 1 Assignment PBP/PBD</h1>

            <h5>Name:</h5>
            <p>{{ name }}</p>

            <h5>Student ID:</h5>
            <p>{{ student_id }}</p>

            <table>
                <tr>
                    <th>Item Name</th>
                    <th>Item Price</th>
                    <th>Item Stock</th>
                    <th>Rating</th>
                    <th>Description</th>
                    <th>Item URL</th>
                </tr>

                {% for catalog in catalogs %}
                <tr>
                    <td>{{catalog.item_name}}</td>
                    <td>{{catalog.item_price}}</td>
                    <td>{{catalog.item_stock}}</td>
                    <td>{{catalog.rating}}</td>
                    <td>{{catalog.description}}</td>
                    <td>{{catalog.item_url}}</td>
                </tr>
                {% endfor %}

            </table>

            {% endblock content %}

        This template uses **name**, **student_id**, and **catalogs** from the `show_catalog` function from the view.

8. To load the data from `katalog/fixtures`, run this command:

        python manage.py loaddata initial_catalog_data.json

9. Deploy the project using Heroku
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