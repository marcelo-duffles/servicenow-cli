import socket

# Service Now access configuration
INSTANCE = "instance"
USERNAME = "user"
PASSWORD = "pass"

# Events that match with the conditions below  will be ignored
IGNORE_CI = {'operational_status': '3'}
IGNORE_ALERT_EVENT = {'cmdb_ci': 'google'}

# Debugging flag for SOAP API
SOAP_API_DEBUG = False

# Hostname with only the first part (in upper case)
HOSTNAME = socket.gethostname().split('.', 1)[0].upper()


# Customize here your alert event
def build_alert_event(parameters):
    data = {
        'cmdb_ci': '.'.join(parameters.split(';')[0].split('.')[0:2]),
        'short_description': ''.join(parameters.split(';')[3:]),
        'u_monitoring_system': 'OpManager',
        'u_monitoring_server': 'ALOG.' + HOSTNAME,
        'u_opm_severity': parameters.split(';')[1],
        'u_opm_entity': parameters.split(';')[2],
    }
    return data

# Using the same function above for building the incident
build_incident = build_alert_event
