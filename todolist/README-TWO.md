# Assignments 6: Javascript and Ajax

**Nama:** Eduardus Tjitrahardja

**NPM:** 2106653602

**Kelas:** D

**Link:** [Deployed Heroku Website](https://edutjie-pbp-2.herokuapp.com/todolist/)


## Asynchronous vs Synchronous Programming
Async is multi-thread, which means operations or programs can run in parallel. Sync is single-thread, so only one operation or program will run at a time.
Async is non-blocking, which means it will send multiple requests to a server. Sync is blocking, it will only send the server one request at a time and will wait for that request to be answered by the server.


## Event-Driven Programming
Event-driven programming is a programming paradigm in which program execution is determined by new user events (mouse clicks, keypresses), sensor outputs, or message passing from other programs. In this program is there is a click event listener that listen a button with a certain id to do certain function. For example, "Tambah Task" 


## Asynchronous Programming in Ajax implementation
1. Add `<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>` to html header.
2. Add `<script>` tag inside your html body.
3. Write ajax JQuery syntax inside your script, like `$.ajax()` to POST, DELETE, etc.
4. Ajax will listen the event listener you write in script to perform the action you want.
5. That action dan response/data will be processed asynchronously in the server.
6. The data will be shown in the page without needing to refresh.


## This Assignment Implementation
1. Create `show_json` in views

        @login_required(login_url="/todolist/login/")
        def show_json(request):
            task = Task.objects.filter(user=request.user)
            return HttpResponse(
                serializers.serialize("json", task), content_type="application/json"
            )

2. Edit `show_todolist` in views

        @login_required(login_url="/todolist/login/")
        def show_todolist(request):
            # todolist_objects = sorted(
            #     Task.objects.filter(user=request.user), key=lambda x: x.is_finished
            # )
            context = {"username": request.user}
            return render(request, "todolist.html", context)

3. Add Ajax script in `base.html`'s header

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

4. Create `add_task` in views to post data using Ajax

        def add_task(request):
            if request.method == "POST":
                title = request.POST.get("title")
                description = request.POST.get("description")
                task = Task.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    date=datetime.datetime.today(),
                )
                return JsonResponse(
                    {
                        "pk": task.id,
                        "fields": {
                            "title": task.title,
                            "description": task.description,
                            "is_finished": task.is_finished,
                            "date": task.date,
                        },
                    },
                    status=200,
                )

5. Add GET function in `todolist.html`

            $.get("{% url 'todolist:show_json' %}", data => {
                data.sort((a, b) => {
                return a.fields.is_finished - b.fields.is_finished;
                });
                $.each(data, (i, value) => {
                $("#todolist").append(card(value)); // append to the div

                // add event listener to the delete button
                $(`#delete-${value.pk}`).click(() => {
                    deleteTask(value.pk);
                });

                // add event listener to the checkbox
                $(`#status-${value.pk}`).change(() => {
                    updateFinished(value.pk);
                });
                });
            });

6. Create Modal and its functionality

        <script>
            const openModal = e => {
                e.preventDefault(); // prevent refresh
                $("#create-task-modal").removeClass("hidden");
            };

            const closeModal = e => {
                $("#create-task-modal").addClass("hidden");
            };

            $("#create-task").click(openModal);
            $("#close-modal").click(closeModal);
        </script>

        <div
        id="create-task-modal"
        class="w-full fixed flex justify-center w-full z-10 min-h-screen items-center bg-black bg-opacity-50 hidden"
        >
            <div class="mt-7 bg-white rounded-xl shadow-lg">
                <div class="p-4 sm:p-7">
                <div class="flex flex-col items-center justify-center gap-5">
                    <h1 class="text-3xl font-bold">Create Task</h1>
                    <form method="post" id="create-task-form">
                    {% csrf_token %}
                    <div class="gap-5 text-left grid grid-cols-3 grid-rows-3">
                        <label for="title">Title:</label>
                        <input
                        type="text"
                        name="title"
                        id="title"
                        placeholder="Isi judul task anda"
                        required
                        class="col-span-2 form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                        />

                        <label for="password">Description:</label>
                        <input
                        type="text"
                        name="description"
                        id="description"
                        placeholder="Isi deskripsi anda"
                        required
                        class="col-span-2 form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                        />

                        <input
                        data-mdb-ripple="true"
                        data-mdb-ripple-color="light"
                        class="col-span-3 text-white hover:shadow-lg hover:shadow-blue-500/50 transition-all bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
                        type="submit"
                        value="Create Task"
                        />
                    </div>
                    </form>
                    <a
                    href="{% url 'todolist:show_todolist' %}"
                    class="font-bold text-blue-600 underline hover:no-underline"
                    id="close-modal"
                    >Close</a
                    >
                </div>
                </div>
            </div>
        </div>

7. Add POST function in `todolist.html`

        $("#create-task-form").submit(e => {
            e.preventDefault();

            // get the CSRF Token
            const csrftoken = document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;

            const title = $("#title").val();
            const description = $("#description").val();

            if (title && description) {
                $.ajax({
                type: "POST",
                url: "{% url 'todolist:add_task' %}",
                headers: { "X-CSRFToken": csrftoken }, // give CSRF token to the header
                mode: "same-origin", // Do not send CSRF token to another domain.
                data: {
                    title: title,
                    description: description,
                },
                success: response => {
                    $("#create-task-form").trigger("reset");
                    closeModal();
                    $("#todolist").prepend(card(response));
                },
                error: error => {
                    console.log(error);
                },
                });
            } else {
                alert("Please fill all the fields");
            }
        });


8. Add DELETE function in `todolist.html`

        const deleteTask = id => {
            // get the CSRF Token
            const csrftoken = document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;

            $.ajax({
                url: "{% url 'todolist:delete_task' 0 %}".replace("0", id),
                type: "DELETE",
                headers: { "X-CSRFToken": csrftoken }, // give CSRF token to the header
                mode: "same-origin", // Do not send CSRF token to another domain.
                success: () => {
                // remove the card
                $(`#delete-${id}`).parent().parent().parent().remove();
                },
                error: error => {
                console.log(error);
                },
            });
        };

9.  Add PUT function in `todolist.html` 

        const updateFinished = id => {
            // get the CSRF Token
            const csrftoken = document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;

            $.ajax({
                url: "{% url 'todolist:update_finished' 0 %}".replace("0", id),
                type: "PUT",
                headers: { "X-CSRFToken": csrftoken }, // give CSRF token to the header
                mode: "same-origin", // Do not send CSRF token to another domain.
                success: response => {
                // refresh
                $("#todolist").empty();
                renderTasks();
                },
                error: error => {
                console.log(error);
                },
            });
        };