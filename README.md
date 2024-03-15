MIT Code For Good IAP 2017
Seeding Labs
Abigail Katcoff '18, Tho Tran '19, Venita Boodhoo '18

Project Description
Our app, "main_flask_app.py", found at https://equip-search-2e33e9b172fc.herokuapp.com/, allows users to search multiple websites for used or new lab equipment, finds the median value, and returns a list of results. Users also have the option to download a csv file (editable in Microsoft Excel) of the results, including url, price, and title.
_________________________________________________________________
Project Structure

     main_flask_app.py
   /               \            
backend.py         templates (html)
   |      \ 
util.py   <website>.py
   |       /
   Result.py

(scraping_tests.py test <website>.py files)

Our GUI is a Flask app (http://flask.pocoo.org/docs/0.12/) located in main_flask_app. This file handles the front end of the web app and can be run locally by running "python main_flask_app". HTML templates for the website's pages are located in the templates directory. For the backend, main_flask_app imports backend.py and util.py. 

backend.py has only one function called by main_flask_app: do_search, which does a search based on a specified subset of websites and returns a list of Result objects. do_search does this by calling the individual website scraping files below.


WEBSITE                      SCRAPER                   EQUIPMENT
biosurplus                   Abigail K                   Used
coleparmer                   Tho T                       New
daigger                      Venita B                    New
dotmed                       Tho T                     Used/New
ebay                         Abigail K                 Used/New
equipnet                     Abigail K                   Used
eurekaspot                   Venita B                    Used
google                       Abigail K                 Used/New
ika                          Tho T                       New
labcommerce                  Venita B                    Used
labx                         Venita B                  Used/New
marshallscientific           Tho T                       Used
medwow                       Tho T                     Used/New
newlifescientific            Venita B                    Used
sci-bay                      Abigail K                   Used
sibgene                      Venita B                  Used/New
used-line                    Tho T                       Used

These files use BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrape search results and return Result objects for each. 

To add a new website to the list, simply create a file with the website's name and an extract_results function and add it the appropriate list of functions in backend.py. Use Google Developer Tools and BeautifulSoup to scrape the website. 

Most files make use of functions in util.py, which includes a median finding function, a url creating function, etc.

Refer to comments in individual files for more details. 
_________________________________________________________________
Deployment with Heroku: https://devcenter.heroku.com/articles/git

Install heroku and log into an account that can access the app. Add a git remote named heroku for https://git.heroku.com/seedinglabsequipmentvaluation.git. 

If you add any new system requirements or imports, run "pip freeze > requirements.txt" so that the changes are reflected in the Heroku system.

To make changes to the website, commit and run "git push heroku master."

If the website is buggy, you can run "heroku logs" to locate the problem.
# seedingLabs
