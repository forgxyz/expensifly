#### [to home](https://jackforgash.com/)

# expensifly

### description
a django webapp for manually recording expenses for budgeting purposes.  
i didn't like the budgeting apps out there: mint is awful, clarity was ok but didn't have what i wanted... so, i made my own solution. i currently do this via google forms and view the current month in excel. that works alright and i like that it is a manual process - i need to register each card swipe, both physically and mentally. so, i took a course in web dev during covid spring and decided to build out a better solution for myself. i can only submit feedback to some app for a feature i want, but if it's mine - i can just build it in.  
*log in to the test account to see how it works:*  
*un: testuser*  
*pw: banana4g*  

## todo
### general


### auth
- [ ] add permission requirement for edit and delete
= [ ] finish delete()

### record
- [ ] option for money in
  - record top line to have a view of cash flow
- [ ] date accepts str input
  - popup calendar for one click input?
  - datepicker

### view
- [ ] filter month by category / dynamic table
- [ ] portal with more in depth options
  - comparison
    - month to month
    - YTD y-o-y


### deployment
- [ ] get on heroku for testing during development by end of sept
- [ ] tx list too wide for mobile


### models
- [ ] link tx entries to a user id


## other
### notes
- #181a1b looked good as a dark bg for body
- maybe change how ExpenseForm is deployed to add classes to the form elements. make it look a little nicer.

### django questions / to look up


## done

- [x] comment and tag need to be nullable
- [x] delete view app - not broad enough to need multiple django apps
- [x] add selected month to local storage
	- [FileSystemStorage](https://docs.djangoproject.com/en/3.1/ref/files/storage/)
	- session data in flask
	- no localStorage was a JS thing --- so, should I add some JS to set the current month??
		- cs50w p2 for reminder of this
- [x] split out get_spending info
  - save months to session. load nav data from there instead
- [x] change order of 'change month' -> desc
- [x] format of numbers - there has to be a better way to do this.. in the template?
- [x] change month does not load on this view
- "home" loads the month overview, view transactions loads is not just for the curr month, portal does the same.
  - add current month button
- navbar buttons should load whatever the selected month is, as chosen by the dropdown.
- [x] top 3 categories only showing max, not sum???
  - & make sure they aggregate across method differences
  - it's only grouping categories when the date is the same whyyyyyy
  - idk. using pandas
- global variable for views?
  - months is used to populate the navbar. can i query that just once? save to browser local storage???
  - same for current month
  - the index page & navbar both use current month info
- category: should this just be categorical type? can add new via admin panel if needed
  - drawbacks to having it in a table?
  - same with method
- [x] make fewer repeated calls to the database. moving from overview to tx_list shouldn't send the same queries... unnecessarily slow. cache them? use session?
- [x] hide nav items if logged out
- [x] login screen? once online i'll want to keep my own stuff secure
  - limit random registration (heroku limits)
  - yes and set up a test user for the current test data
- [x] main screen
  - [x] current month total
  - [x] snapshot of spending by category
- [x] decorator/wrapper requiring login to load any other view
- [x] fix loading data & user permissions
- [x] edit tx functionality. See [the save() method](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method). Edit button next to TX, or pass TX ID into an edit search box to bring up a populated form. Change as needed there.
