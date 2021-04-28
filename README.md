# Recipes Newsletter

#### A python app for sending your subscribers random recipes for each meal in a form of an email.

---
### This repository contains:
* #### scripts that scrape recipes data for any meals from two popular food blogs
* #### a class that populates a mongo database with scraped recipes
* #### a cloud function ready to be deployed that will generate random recipes for each user in a db and send them recipes - can be set up so it runs automatically at certain times

---

### Sample recipes:
<p float="left">
<img src="https://automatycznyjadlospis.s3.eu-central-1.amazonaws.com/breakfast.jpg" alt="error getting picture.. sorry" width="200" height="432" >
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img src="https://automatycznyjadlospis.s3.eu-central-1.amazonaws.com/main.jpg" alt="error getting picture.. sorry" width="200" height="432" ">
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img src="https://automatycznyjadlospis.s3.eu-central-1.amazonaws.com/soup.jpg" alt="error getting picture.. sorry" width="200" height="432" >
</p>

---
#### Single recipe contains:
* recipe's title
* ingredients list
* directions list
* number of portions it yields
* total cooking time value
* active cooking time value
* link to the photo of prepared meal
* link to the recipe's blog post
