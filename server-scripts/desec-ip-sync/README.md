# Desec-IP-Sync

## Reason
[desec.io](https://desec.io/) is a free DNS hosting service that has securty in mind.
I personally use this service, and I noticed that there are times in which my IP always resets to another value. Which does hinder my ability to work.

This solves this issue by containerizing the service in Docker so it can be used by any `amd64` or `arm64` server. To which the program checks to see if the server's IP has changed, comapres it to an "old" IP, and changes old information from desec.io using it's API automatically without inteference.
