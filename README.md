# expensifly

a basic django webapp for manually recording expenses for budgeting purposes. i currently do this via google forms and view the current month in excel, but i will replace that with this and build out some visualizations. this is the next iteration of the my CS50 final project from late 2019.

## TODO
- [ ] viz / view app
  1. pull expense from db
  2. select month to pull
  3. summary by category in that month - dropdown of available months
  4. "view all" button by each category to bring up those transactions
  5. another "view all" at the end to see all for that month
  6. .delete() button


- [ ] Edit functionality. See [the save() method](https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method). Edit button next to TX, or pass TX ID into an edit search box to bring up a populated form. Change as needed there.

- [x] comment and tag need to be nullable
