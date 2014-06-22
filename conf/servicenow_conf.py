# Service Now access configuration
INSTANCE = "instance"
USERNAME = "user"
PASSWORD = "pass"

# Events that match with the conditions below  will be ignored
IGNORE_CI = {'operational_status': '3'}
IGNORE_ALERT_EVENT = {'cmdb_ci': 'google'}

# Debugging flag for SOAP API
SOAP_API_DEBUG = False


# Customize here your alert event
def build_alert_event(parameters):
    data = {
        'cmdb_ci': '.'.join(parameters.split(';')[0].split('.')[0:2]),
        'u_opm_severity': parameters.split(';')[1],
        'u_opm_entity': parameters.split(';')[2],
        'short_description': ''.join(parameters.split(';')[3:])
    }
    return data

# Using the same function above for building the incident
build_incident = build_alert_event
