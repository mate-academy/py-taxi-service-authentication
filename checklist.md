p# Сheck Your Code Against the Following Points

## Don't Push db files

Make sure you don't push db files (files with `.sqlite`, `.db3`, etc. extension).

## Don't forget to attach all screenshots of created/modified pages.

## Code Efficiency
1. Make sure you've added a blank line at the end to all your files including `.css`, `.html` and `.gitignore`.
2. Use `pluralize`.

Good example:

```html
    <p>You have visited this page {{ num_visits }} time{{ num_visits|pluralize }}</p>
```

Bad example:

```html
    <p>You have visited this page {{ num_visits }} {% if num_visits == 1 %} time {% else %} times {% endif %}.</p>
```

3. Make sure that `num_visits` works as expected.
When you visit the page for the first time there should be: `You have visited this page 1 time`

4. Make sure you use 2 whitespaces indentations in your `.html` files.

## Code style

Use hyphens `-` instead of underscores `_` to separate words in the URL’s `name` parameter.

Good example:

```python
urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus-list"),
]
 ```

Bad example:

```python
urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus_list"),
]
 ```

## Clean Code
Add comments, prints, and functions to check your solution when you write your code. 
Don't forget to delete them when you are ready to commit and push your code.
