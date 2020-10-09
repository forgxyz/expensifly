#### [to home](https://jackforgash.com/)

# expensifly

**try it out:**  
*un: testuser*  
*pw: banana4g*  

## todo
### general
- [ ] split out update month and refresh transactions
- [caching](https://docs.djangoproject.com/en/3.0/topics/cache/) instead of session storage? pros/cons/best practice?
  - **yes bc the way i have it set up currently does not refresh well**


### record
- [ ] option for money in
  - record top line to have a view of cash flow
- Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.
- SO, if i shouldn't use render, how can i pass a message on submit?

### view
- [ ] filter month by category / dynamic table
- [ ] portal with more in depth options
  - comparison
    - month to month
    - YTD y-o-y
- [ ] categories: list alpha and show to 2 decimals


### deployment
- [ ] https
- [ ] security checklist - what do i need to know?




## other
### notes
- #181a1b looked good as a dark bg for body


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
- [x] link tx entries to a user id
- [x] decorator/wrapper requiring login to load any other view
- [x] fix loading data & user permissions
- [x] edit tx functionality. See [the save() method](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method). Edit button next to TX, or pass TX ID into an edit search box to bring up a populated form. Change as needed there.
- [x] add permission requirement for edit and delete
- make sure another user cannot plug in a number after edit or delete
- [x] finish delete()
- [x] get on heroku for testing during development by end of sept
- [x] mobile compatability
- [x] date accepts str input
  - popup calendar for one click input?
  - datepicker
  - admin panel uses one
- [x] test db
