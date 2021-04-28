# CEPTO

```bash
mosquitto_pub -h 127.0.0.1 -p 1883 -t light_guide/events -m '{"event_type": "notification", "user": {"full_name": "user", "date_of_birth": "1940-01-01"},  "time_of_occurence" : "2021-04-24 23:23:02" }'
```
