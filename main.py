import krpc

conn = krpc.connect()
print(conn.krpc.get_status().version)

vessel = conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame

with conn.stream(vessel.position, refframe) as position:
    while True:
        print(position())