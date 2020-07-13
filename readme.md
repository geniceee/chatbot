Documentation for chat app:

1. Pull repository from GitHub and open in Visual Studio Code
2. Navigate to the project folder and create a new virtual environment
3. Activate the virtual environment
4. Run req.txt using _pip install -r req.txt_
5. On another window (cmd/ubuntu), run the Redis server as follows:

1. Compile and build Redis

- _cd redis-6.0.5_
- _make_

1. Start Redis

- _cd src_
- _./redis-server_

1. Run _python3 manage.py makemigrations_ and _python3 manage.py migrate_ to migrate models.py
2. Run _python3 manage.py runserver_ and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the chat app