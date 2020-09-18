#### [to home](https://jackforgash.com/)

# expensifly

### description
a django webapp for manually recording expenses for budgeting purposes.  
i didn't like the budgeting apps out there: mint is awful, clarity was ok but didn't have what i wanted... so, i made my own solution. i currently do this via google forms and view the current month in excel. that works alright and i like that it is a manual process - i need to register each card swipe, both physically and mentally. so, i took a course in web dev during covid spring and decided to build out a better solution for myself. i can only submit feedback to some app for a feature i want, but if it's mine - i can just build it in.  


## todo
### general
- [ ] add selected month to local storage
	- [FileSystemStorage](https://docs.djangoproject.com/en/3.1/ref/files/storage/) 
	- session data in flask
	- no localStorage was a JS thing --- so, should I add some JS to set the current month
		- cs50w p2 for reminder of this 

### home
- [ ] main screen
  - current month total
  - snapshot of that spending by category
- navbar buttons should load whatever the selected month is, as chosen by the dropdown.
- "home" loads the month overview, view transactions loads is not just for the curr month, portal does the same.
  - add current month button

### record
- [ ] option for money in
  - record top line to have a view of cash flow
- [ ] date accepts str input
  - popup calendar for one click input?

### view
- [ ] edit tx functionality. See [the save() method](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method). Edit button next to TX, or pass TX ID into an edit search box to bring up a populated form. Change as needed there.
- [ ] filter month by category / dynamic table
- [ ] portal with more in depth options
  - **category view**
    - need to have this overview
  - export "selection" as csv? (where selection is the tx data rendered to the screen)
  - comparison
    - month to month
    - YTD y-o-y

### deployment
- [ ] login screen? once online i'll want to keep my own stuff secure
  - limit random registration (heroku limits)
- [ ] get on heroku for testing during development


## django questions / to look up
- global variable for views?
  - months is used to populate the navbar. can i query that just once? save to browser local storage???
  - same for current month
    - the index page & navbar both use current month info


## done

- [x] comment and tag need to be nullable
- [x] delete view app - not broad enough to need multiple django apps


