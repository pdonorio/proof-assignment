
# interfaces

While developing it might nice to interact with the APIs and the database directly through some web interfaces.

## call from swagger UI

Since `rapydo` is swagger-compliant we dynamically produce via Flask an endpoint `/api/specs` to describe your current list of endpoints and methods.

To review it you need to launch a `swagger-ui` container. That's just as easy as:
```bash
rapydo interfaces swagger

[...]
You can access swaggerui web page here:
http://localhost?docExpansion=none
```

Then go to the suggested URL, and play with it.

NOTE: the custom (not in the rapydo base) endpoints are usually all tagged with `custom` so you can access them at:

http://localhost/?docExpansion=none#/custom

## checkout mongo db from UI

In a similar fashion you can quickly get an express container to navigate the data in your mongodb instance with:

```bash
rapydo interfaces mongo

[...]

Mongo Express server listening at http://0.0.0.0:8081
```

Then go to the suggested URL, and play with it.

NOTE: after you save some data with the current ODM definition you should find your data in a database called `proof`. It will not be there initially, though.

