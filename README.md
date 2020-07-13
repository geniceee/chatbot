Documentation for chat app:
1.	Pull repository from GitHub and open in Visual Studio Code
2.	Navigate to the project folder and create a new virtual environment
3.	Activate the virtual environment
4.	Run req.txt using pip install -r req.txt
5.	On another window (cmd/ubuntu), run the Redis server as follows:
1)	Compile and build Redis
      - cd redis-6.0.5
      - make
2)	Start Redis
      - cd src	
      - ./redis-server
6.	Run python3 manage.py makemigrations and python3 manage.py migrate to migrate models.py
7.	Run python3 manage.py runserver and go to http://127.0.0.1:8000/ to view the chat app 
