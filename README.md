# railway-scheduler
More complex scheduler for Railway.app, which takes command line args and sets up a schedule. Runs constantly but sleeps.

Railway does not allow parameters to be passed to cron, so this is a more customizable replacement.

Jobs can be scheduled as JSON inside an environment variable.

At the moment, only hitting a GET url is supported, at the given intervals.

Note that any tasks triggered by a GET should be idempotent, ie they can be requested multiple times without side effects.

