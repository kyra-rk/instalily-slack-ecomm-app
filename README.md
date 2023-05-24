# instalily-slack-ecomm-app

Notes for app.py: 
- include two local environment variables named SLACK_BOT_TOKEN and SLACK_APP_TOKEN to configure the app. 

Notes for scrapper.py: 
- this uses the BeautifulSoup and Requests libraries
- takes a link to the sitemap of Bed Bath and Beyond and finds all product details pages 
- adds all links to their respective categories 

Notes for webscraper.py 
- uses the BeautifulSoup and Selenium libraries
- takes a single product details page from Home Depot
- creates a list of Product objects each with a title and price  
 
