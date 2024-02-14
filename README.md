# Fire Guard

## Forest Fire Detection System

Project for the IoT course of the University of Patras Electrical and Computer Engineering Department

## Build and Run
The project in its current form relies on infrastructure provided by the department,
namely the context broker with associated database and the database which holds the historical data.

```bash
cd software
docker compose up --build -d
```

If you want to run the project with local infrastructure use the local_build branch.
Beware that the function for historical data will not function because a mechanism for creating it has not been configured in this case
