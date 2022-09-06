# TODO actually write the Dockerfile
# the boot script needs to start the guicorn process,
# and the rq worker process
# NOTE Miguel configures the image to either start in "guicorn" mode, or
# to start in "rq-worker" mode.  So the rq worker runs in a separate container
# from the guicorn process.

