SELECT
    e.timestamp,
    et.event_type,
    et.id,
    p.HEUCOD_patient_id,
    s.id,
    s.sensor_type,
    s.device_model,
    s.device_vendor,
    g.HUECOD_gateway_id
FROM events AS e
JOIN event_types AS et
    ON e.event_type_id = et.id
JOIN patients AS p
    ON e.patient_id = p.id
JOIN gateways AS g
    ON e.gateway_id = g.id
JOIN sensors AS s
    ON s.gateway_id = g.id
WHERE
    p.id IN (
        SELECT patient_id
        FROM caregiver_patient_relation
        WHERE caregiver_id IN (
            SELECT id
            FROM caregivers
            WHERE username = '{usr}' AND login_credential_hash = '{user_hash}'
        )
    )
;