# railway-scheduler
More complex scheduler for Railway.app, which takes command line args and sets up a schedule. Runs constantly but sleeps.

Railway does not allow parameters to be passed to cron, so this is a more customizable replacement.

Jobs can be scheduled as JSON inside an environment variable.

## Task types

### GET

Not recommended, except fo things like health statuses.

Note that any tasks triggered by a GET should be idempotent, ie they can be requested multiple times without side effects.


### POST

POSTs are more resistant to being called multiple times, ie by an errant browser, so are the preferred task types for triggering events. But you should still consider cases where the timer is called multiple times after a server restart, etc.


