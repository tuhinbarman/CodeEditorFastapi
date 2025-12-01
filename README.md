setup--->
backend

branch -> dev-branch
commands -> 
git pull origin dev-branch
pip install > requirements.txt
cd backend
uncomment postgresql credentials and setup postgresql in localsystem
uvicorn main:app --reload


frontend
branch -> dev-branch-frontend
commands->
cd frontend
npm install
npm start

architecture-->
frontend --> 
created two components
->  leftsidebar for handling rooms and adding rooms
-> codeeditor for writing text and code
-> using redux for storing all rooms data


backend-->
router -> for segreting room module and creating all room apis
controller -> making managers for handling logic for websocket connections and broadcasting
main -> adding all the routers and middlewares
database -> handling all database configuration 


improvements-->
* the ui is very limited . can use code editors like monaco with the system
* LLM models can be implemented for the autocomplete functionality .
* The websocket implmentation can be made scalable by using redis.
* save functionality can be implemented to make the code persistent.

