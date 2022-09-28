# Assignments 1: Data Delivery Implementation using Django

**Nama:** Eduardus Tjitrahardja

**NPM:** 2106653602

**Kelas:** D

**Link:** [Deployed Heroku Website](https://edutjie-pbp-2.herokuapp.com/todolist/)

## What is `{% csrf_token %}`?

**The Cross-Site Request Forgery (CSRF)** is an attack that forces an end-user to execute unwanted actions on a web application in which they have authenticated themselves.

**`{% csrf_token %}`** tag in Django is used to avoid this **CSRF attacks**. Django has made the implementation for **`{% csrf_token %}`** so easy, you only have to add this tag inside your `<form>` tag in the template.

**`{% csrf_token %}`** generates a **token** on the server-side when rendering the page and cross-check it for any requests coming back to the server. If the request doesn't contain the **token** then the server won't execute the request. In django, if you don't have **`{% csrf_token %}`** tag, when to make a request to the form the web will forces an error that says:

![CSRF Verification Failed](/images/csrf-verification-failed.png)


## Can we make a form without using form generator like `{{ form.as_table }}`? How to make a form using `<form>` in general?

Absolutely, we can make a form from scratch using `<form>` tag instead of using form generator. To make a form, we need to specify the method to be "POST" so the form tag will look like this `<form method="POST">`. Then, we need to add `{% csrf_token %}` inside the form tag to avoid CSRF attacks. Inside the form tag, you can add the input tags to get data from the user. Then, add `<button  type="submit">` tag to submit the form. After the form has been submitted, view can access the request data from the form using `request.POST.get("INPUT_NAME")`.

## Flow from the form to the template.

When a user submitted a form, it will send a "POST" request to the server and the server will call a method from view. That method will get the data from the request using `request.POST.get("INPUT_NAME")` and will create a new object in the database using `Task.objects.create(FIELDS=INPUT, ..)`. Then, we can access the data from the database `Task.objects.filter(user=request.user)`, we filter the object to only the ones that matches the current user so we can show the data for only the current user. Then, render the data we get from the databse to the template using `{% for task in todolist %}`, inside the for loop we can call all the fields in todolist, for example `{{ task.title }}`, etc.   

## Step by step in making this assignment

1.  Create a todolist app if it doesn't already exist. Using `python manage.py startapp todolist`
2.  Append "todolist" to the `INSTALLED_APPS` list in `project_django/settings.py`.

        INSTALLED_APPS = [
            ...
            'todolist',
        ]

3.  Create a `Task` model in `models.py`.

        class Task(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            date = models.DateField()
            title = models.CharField(max_length=255)
            description = models.TextField()
            is_finished = models.BooleanField(default=False)

    After making changes on the model, you have to run `python manage.py makemigrations` and `python manage.py migrate` to migrate your model changes to the database.

4.  Create a superuser `python manage.py createsuperuser` and fill your username and password. Go to `localhost:8000/admin` lalu login dan tambahkan data dummy.

5.  Create functions in `views.py`.

        @login_required(login_url="/todolist/login/")
        def show_todolist(request):
            todolist_objects = Task.objects.filter(user=request.user)
            context = {"todolist": todolist_objects, "username": request.user}
            return render(request, "todolist.html", context)


        def register(request):
            form = UserCreationForm()

            if request.method == "POST":
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Akun telah berhasil dibuat!")
                    return redirect("todolist:login")

                context = {"form": form}
                return render(request, "register.html", context)


        def login_user(request):
            if request.method == "POST":
                username = request.POST.get("username")
                password = request.POST.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)  # melakukan login terlebih dahulu
                    response = HttpResponseRedirect(
                        reverse("todolist:show_todolist")
                    )  # membuat response
                    response.set_cookie(
                        "last_login", str(datetime.datetime.now())
                    )  # membuat cookie last_login dan menambahkannya ke dalam response
                    return response
                else:
                    messages.info(request, "Username atau Password salah!")
            context = {}
            return render(request, "login.html", context)


        def logout_user(request):
            logout(request)
            response = HttpResponseRedirect(reverse("todolist:login"))
            response.delete_cookie("last_login")
            return response


        @login_required(login_url="/todolist/login/")
        def create_task(request):
            if request.method == "POST":
                title = request.POST.get("title")
                description = request.POST.get("description")
                Task.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    date=datetime.datetime.today(),
                )
                return HttpResponseRedirect(reverse("todolist:show_todolist"))
            return render(request, "create_task.html")


        @login_required(login_url="/todolist/login/")
        def delete_task(request, id):
            task = Task.objects.get(user=request.user, id=id)
            task.delete()
            return HttpResponseRedirect(reverse("todolist:show_todolist"))


        @login_required(login_url="/todolist/login/")
        def update_finished(request, id):
            task = Task.objects.get(user=request.user, id=id)
            task.is_finished = not task.is_finished
            task.save(update_fields=["is_finished"])
            return HttpResponseRedirect(reverse("todolist:show_todolist"))

6.  Append mywatchlist path to `urlpatterns` list in `project_django/urls.py`.

        urlpatterns = [
            ...
            path("todolist/", include("todolist.urls")),
        ]

    This will create a path from the base path to the "todolist" app.

7.  Create `app_name` and `urlpatterns` in `todolist/urls.py`.

        from django.urls import path
        from todolist.views import (
            create_task,
            delete_task,
            show_todolist,
            register,
            login_user,
            logout_user,
            update_finished,
        )

        app_name = "mywatchlist"
        urlpatterns = [
            path("", show_todolist, name="show_todolist"),
            path("login/", login_user, name="login"),
            path("register/", register, name="register"),
            path("create-task/", create_task, name="create_task"),
            path("logout/", logout_user, name="logout"),
            path("delete-task/<int:id>", delete_task, name="delete_task"),
            path("update-finished/<int:id>", update_finished, name="update_finished"),
        ]

    This will create a path from `/todolist` that calls `show_todolist`, `login`, `register`, `create_task`, `logout`, `delete_task` and `update_finished`.


8. Use the return data from the function in views and create templates for each function that needs html to be rendered.
   - `todolist.html`
  
            {% extends 'base.html' %} {% block content %} {% load todolist_customtags %}

            <h1>{{ username }}</h1>
            <button style="margin-bottom: 20px">
            <a
                href="{% url 'todolist:create_task' %}"
                style="text-decoration: none; color: inherit"
                >Tambah Task</a
            >
            </button>
            <table>
            <tr style="background-color: #ced4da">
                <th>Status</th>
                <th>Task</th>
                <th>Description</th>
                <th>Created At</th>
                <th>Delete Task</th>
            </tr>
            {% for task in todolist %}
            <tr
                style="
                    {% if forloop.counter0|modulo:2 != 0 %} background-color: #e9ecef; {% endif %}
                    {% if task.is_finished %} text-decoration: line-through; opacity: 0.5; {% endif %}
                ">
                <td>
                <input
                    type="checkbox"
                    name="status"
                    id="status"
                    {% if task.is_finished %} checked {% endif %}
                    onchange="location.href='{% url 'todolist:update_finished' task.id %}'"
                />
                </td>
                <td>{{task.title}}</td>
                <td>{{task.description}}</td>
                <td>{{task.date}}</td>
                <td style="display: flex; justify-content: center">
                <button><a href="{% url 'todolist:delete_task' task.id %}">❌</a></button>
                </td>
            </tr>
            {% endfor %}
            </table>
            <button style="margin-top: 20px">
            <a
                href="{% url 'todolist:logout' %}"
                style="text-decoration: none; color: inherit"
                >Logout</a
            >
            </button>

            {% endblock content %}

   - `create_task.html`

            {% extends "base.html" %}
            {% block content %}

            <h3>{{ title }}</h3>
            <form method="post" style="display: flex; flex-direction: column; max-width: 50%; margin: auto; gap: 10px;">
                {% csrf_token %}

                <label for="title">Title</label>
                <input type="text" name="title" placeholder="Isi judul task anda">

                <label for="description">Description</label>
                <input type="text" name="description" placeholder="Isi deskripsi anda">

                <button type="submit">Create Task</button>
            </form>

            {% endblock %}

    - `login.html`

            {% extends 'base.html' %}

            {% block meta %}
            <title>Login</title>
            {% endblock meta %}

            {% block content %}

            <div class = "login">

                <h1>Login</h1>

                <form method="POST" action="">
                    {% csrf_token %}
                    <table>
                        <tr>
                            <td>Username: </td>
                            <td><input type="text" name="username" placeholder="Username" class="form-control"></td>
                        </tr>
                                
                        <tr>
                            <td>Password: </td>
                            <td><input type="password" name="password" placeholder="Password" class="form-control"></td>
                        </tr>

                        <tr>
                            <td></td>
                            <td><input class="btn login_btn" type="submit" value="Login"></td>
                        </tr>
                    </table>
                </form>

                {% if messages %}
                    <ul>
                        {% for message in messages %}
                            <li>{{ message }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}     
                    
                Belum mempunyai akun? <a href="{% url 'todolist:register' %}">Buat Akun</a>

            </div>

            {% endblock content %}

    - `register.html`

            {% extends 'base.html' %}

            {% block meta %}
            <title>Registrasi Akun</title>
            {% endblock meta %}

            {% block content %}  

            <div class = "login">
                
                <h1>Formulir Registrasi</h1>  

                    <form method="POST" >  
                        {% csrf_token %}  
                        <table>  
                            {{ form.as_table }}  
                            <tr>  
                                <td></td>
                                <td><input type="submit" name="submit" value="Daftar"/></td>  
                            </tr>  
                        </table>  
                    </form>

                {% if messages %}  
                    <ul>   
                        {% for message in messages %}  
                            <li>{{ message }}</li>  
                            {% endfor %}  
                    </ul>   
                {% endif %}

            </div>  

            {% endblock content %}


9.  Deploy the project using Heroku
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
