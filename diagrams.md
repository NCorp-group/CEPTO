Sequence diagram for local system:
````
title Sensor - Raspberry PI Interaction

participant "++Light Guide Controller++" as ctrl
participant "++MQTT Broker++" as mqtt
participant "++Zigbee Coordinator++" as zb
participant "++PIR Sensor++" as pir
participant "++Light Strip++" as light

activate ctrl
ctrl ->> mqtt: subscribe to PIR
// TODO: maybe change "Light Guide" to product name

loop
pir -> pir: detect movement
activate pir
note over pir: sensor detects something,\n e.g. user enters a new zone

opt change in state
pir ->> zb: publish state
deactivate pir
activate zb
zb ->> mqtt: publish to PIR
deactivate zb
activate mqtt
mqtt ->> ctrl: on_message() callback
deactivate mqtt
activate ctrl
note over ctrl: controller filters out all irrelevant topics, \n i.e. it only reacts to occupancy changes

opt occupancy changed
ctrl ->> mqtt: publish to light_strip/state
deactivate ctrl
activate mqtt
mqtt ->> zb: publish light_strip/state
deactivate mqtt
activate zb
zb ->> light: update light strip state
deactivate zb
end
end
end
````

Mermaid layered diagram:
```mermaid
graph TD
    subgraph UI;
    %% One class per html file
    HTML[Views];
    CSS[Styles];
    JS[Scripts];
    end;

    subgraph UIM[UI Management];
    %% Web App
    %% One class per component script
    HTML --- comp1[Component logic];
    HTML --- comp2[Component logic];
    end;

    subgraph B[Server Business Logic];
    %% Web Server
    %% All serious stuff is in here
    comp1 --- session[Session manager];
    comp2 --- session;
    end;

    subgraph PI[RasPI Business Logic];
    %% Processing sensor data, sensor and actuator logic
    something2;
    vib[PIR sensor controller];
    led[LED strip controller];
    end;

    subgraph DB[Service];
    %% Database management
    something2[MQTT publisher] --- user_data[MQTT listener];
    session --- user_data;
    user_data --- database[Database controller];
    end;

    subgraph phys[Physical];
    %% Sensor controllers
    vib --- sensor1[PIR sensor listener];
    led --- act1[LED strip publisher];
    end;
```
Alternative:
````mermaid
graph TD;

    %% Caregiver Computer
    subgraph caregiver[Caregiver PC];
        app[Web app];
    end;

    %% Server Computer
    subgraph server_comp[Server Computer];
        server[Web server];
        db[Database];
    end;

    %% Raspberry PI
    subgraph raspi[Raspberry PI];
        mqtt[MQTT broker];
        ztm[Z2M];
        logic[Application];
    end;

    %% PIR Sensor
    subgraph pir[PIR sensor];
        zb_pub1[Zigbee publisher];
    end;

    %% Vibration Sensor
    subgraph vib[Vibration sensor];
        zb_pub2[Zigbee publisher];
    end;

    %% LED Strip
    subgraph led[LED strip];
        zb_sub1[Zigbee subscriber];
    end;

    %% Connections
    zb_pub1 --- ztm;
    zb_pub2 --- ztm;
    zb_sub1 --- ztm;
    server --- app;
    ztm --- mqtt;
    mqtt --- logic;
    logic --- server;
````
