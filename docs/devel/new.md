
# add an endpoint

In the course of your development you might also need to create new development. You shouldn't need this in your current exercise, but feel free to try if you're curious.

NOTE: instructions below are more difficult than the ones you saw so far.

## prepare the scaffold

If you need a new endpoint rapydo can quickly prepare a template for you:
```bash
rapydo template books

[...]
rendered projects/proof/backend/swagger/books/specs.yaml
rendered projects/proof/backend/swagger/books/get.yaml
rendered projects/proof/backend/apis/books.py
rendered projects/proof/backend/tests/test_books.py
[...]
```

At this point, if you restart your Flask debug instance, you can already call from the other terminal:
```bash
$ http GET localhost:8080/api/books 
HTTP/1.0 200 OK
```


## understand the scaffold

### specs of your endpoint

The `specs.yaml` specifies where your file and class position:
```
file: books     # expecting to find projects/PROJECT/backend/apis/books.py
class: Books    # expecting a `Books` class inside that file
```

Also you want to map one or more URLs to your class, and that's what you do with mappings:

```
mapping:
  books: "/books"
```

This means that the label `books` will be associated in the methods YAML files (described in next section) to the URL `/api/books`. 
NOTE: `/api` is automatically added.

### methods

For each method you want to add to your endpoint you have to add in the relative swagger directory a `$method.yaml` file.

By default you receive a `get.yaml` as example. There you might tweak authentication (but that is a separated discussion).

### tests

Also a unittest is prepared for you to work on your endpoint.
Nothing different from the previous chapter here!

