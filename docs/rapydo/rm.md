
## removing

To only stop and remove containers when you don't use them:

```bash
rapydo remove
```

NOTE: this keeps your volume/data in place, so when restarting the database will have the same data.

## completed clean up

To remove also networks and volumes from your docker instance, you can instead use the command:
```bash
rapydo clean --rm-volumes
```

NOTE: this above is dangerous if you stored some important data!

