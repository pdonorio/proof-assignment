
# writing unittests

In rapydo the main unittest framework was `nose2`, but we recently switched to `py.test`.

## how to write unittests

Unittests are just method of a class.
There should be at least a class per endpoint.

To write unittests on `/api/articles` endpoint we created an example in the [`tests` folder](https://github.com/pdonorio/proof-assignment/tree/master/projects/proof/backend/tests/).

## run tests

To run all custom tests you have in your vanilla project just write inside the backend container:
```bash
py.test -s -x tests/custom/

[...]

1 passed in 1.02 seconds
```

