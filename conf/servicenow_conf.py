import socket
import os


# Service Now access configuration
INSTANCE = "instance"
USERNAME = "user"
PASSWORD = "pass"

# Events that match with the conditions below  will be ignored
IGNORE_CI = {'operational_status': '3'}

# Debugging flag for SOAP API
SOAP_API_DEBUG = False

# Hostname with only the first part (in upper case)
HOSTNAME = socket.gethostname().split('.', 1)[0].upper()


# Customize here your alert event
def build_alert_event(parameters):
    severity_map = {
        'Clear': 'Normalizacao',
        'Info': 'Informativo',
        'Critical': 'Falha critica',
        'Service Down': 'Falha de servico',
        'Attention': 'Baixa',
        'Trouble': 'Baixa',
    }
    opm_entity = parameters.split(';')[2]
    opm_severity = parameters.split(';')[1]
    severity = severity_map[opm_severity]
    short_description = ''.join(parameters.split(';')[3:])
    cmdb_ci = '.'.join(parameters.split(';')[0].split('.')[0:2]).upper()
    company = parameters.split(';')[0].split('.')[0].upper()
    management_mode = parameters.split(';')[0].split('.')[2].upper()

    if opm_severity != 'Clear':
        if (management_mode != 'GT') and \
           not (management_mode == 'HD' and company == 'LOGIN'):
            severity = 'Informativo'
        elif ('ProcessMonitor' in opm_entity) or ('URL_Poll' in opm_entity):
            severity = 'Falha de Servico'
        elif '_Poll' in opm_entity:
            severity = 'Falha critica'
        elif ('CPU' in opm_entity) or ('MEM' in opm_entity) or \
             ('RAM' in opm_entity) or \
             ('Disk' in opm_entity) or ('Partition' in short_description) or \
             ('IF_UTIL' in opm_entity):
            severity = 'Capacidade'

    data = {
        'cmdb_ci': cmdb_ci,
        'company': company,
        'short_description': short_description,
        'u_monitoring_system': 'OpManager',
        'u_monitoring_server': 'ALOG.' + HOSTNAME,
        'u_severity': severity,
        'u_opm_severity': opm_severity,
        'u_opm_entity': opm_entity,
    }
    return data

# Using the same function above for building the incident
build_incident = build_alert_event


# Customize here your function to filter alert events
def filter_alert_event(event):
    ''' returns False if the alert event is to be ignored '''

    if (event['company'] != 'LOGIN'):
        return False

    return True


LOG_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/log'
ALERT_EVENTS_LOCK = LOG_PATH + '/.alertEventsNotInserted.lock'
ALERT_EVENTS_REINSERTION_LOCK = LOG_PATH + '/.alertEventsReinsertion.lock'
