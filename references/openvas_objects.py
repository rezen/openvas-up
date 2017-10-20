
class OpenvasObject:

  def command(self, name, details={}):
    if details is None: 
      details = {}
    elif not isinstance(details, dict):
      raise Error()
  
  
class Agent(OpenvasObject):
  """ @entity agent """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'installer':  {
        'signature':  signature,
      },
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'howto_install':  howto_install,
      'howto_use':  howto_use,
    }
 
    return self.command('create_agent', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@agent_id':  check_uuid(agent_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_agent', directives)
 
  def get(self, **kwargs):
    directives = {
      '@agent_id':  check_uuid(agent_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'trust':  trust,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@details':  check_boolean(details),
      '@format':  format,
    }
 
    return self.command('get_agents', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@agent_id':  check_uuid(agent_id),
      'name':  name,
      'comment':  comment,
    }
 
    return self.command('modify_agent', directives)
 
  def verify(self, **kwargs):
    directives = {
      '@agent_id':  check_uuid(agent_id),
    }
 
    return self.command('verify_agent', directives)
 

class Alert(OpenvasObject):
  """ @entity alert """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'condition':  {
        'data':  {
          'name':  name,
        },
      },
      'event':  {
        'data':  {
          'name':  name,
        },
      },
      'method':  {
        'data':  {
          'name':  name,
        },
      },
      'filter':  {
        '@id':  check_uuid(id),
      },
    }
 
    return self.command('create_alert', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@alert_id':  check_uuid(alert_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_alert', directives)
 
  def get(self, **kwargs):
    directives = {
      '@alert_id':  check_uuid(alert_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'event':  event,
        'condition':  condition,
        'method':  method,
        'filter':  filter,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@tasks':  check_boolean(tasks),
    }
 
    return self.command('get_alerts', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@alert_id':  check_uuid(alert_id),
      'name':  name,
      'comment':  comment,
      'filter':  {
        '@id':  check_uuid(id),
      },
      'event':  {
        'data':  {
          'name':  name,
        },
      },
      'condition':  {
        'data':  {
          'name':  name,
        },
      },
      'method':  {
        'data':  {
          'name':  name,
        },
      },
    }
 
    return self.command('modify_alert', directives)
 
  def test(self, **kwargs):
    directives = {
      '@alert_id':  check_uuid(alert_id),
    }
 
    return self.command('test_alert', directives)
 

class Asset(OpenvasObject):
  """ @entity asset """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'asset':  {
        'name':  name,
        'comment':  comment,
      },
      'report':  {
        '@id':  check_uuid(id),
        'filter':  {
          'term':  term,
        },
      },
    }
 
    return self.command('create_asset', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@asset_id':  check_uuid(asset_id),
      '@report_id':  check_uuid(report_id),
    }
 
    return self.command('delete_asset', directives)
 
  def get(self, **kwargs):
    directives = {
      '@asset_id':  check_uuid(asset_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'severity':  severity,
        'os':  os,
        'oss':  oss,
        'hostname':  hostname,
        'ip':  ip,
        'title':  title,
        'hosts':  hosts,
        'latest_severity':  latest_severity,
        'highest_severity':  highest_severity,
        'average_severity':  average_severity,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@ignore_pagination':  check_boolean(ignore_pagination),
    }
 
    return self.command('get_assets', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@asset_id':  check_uuid(asset_id),
      'comment':  comment,
    }
 
    return self.command('modify_asset', directives)
 

class Config(OpenvasObject):
  """ @entity config """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'comment':  {
        'copy':  copy,
        'get_configs_response':  get_configs_response,
      },
      'name':  name,
    }
 
    return self.command('create_config', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@config_id':  check_uuid(config_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_config', directives)
 
  def get(self, **kwargs):
    directives = {
      '@config_id':  check_uuid(config_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'nvt_selector':  nvt_selector,
        'families_total':  families_total,
        'nvts_total':  nvts_total,
        'families_trend':  families_trend,
        'nvts_trend':  nvts_trend,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@details':  check_boolean(details),
      '@families':  check_boolean(families),
      '@preferences':  check_boolean(preferences),
      '@tasks':  check_boolean(tasks),
    }
 
    return self.command('get_configs', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@config_id':  check_uuid({
        'name':  name,
        'comment':  comment,
        'scanner':  scanner,
        'preference':  {
          'name':  name,
          'nvt':  {
            '@oid':  check_oid(oid),
          },
          'value':  value,
        },
        'family_selection':  {
          'growing':  growing,
          'family':  {
            'all':  all,
            'growing':  growing,
            'name':  name,
          },
        },
        'nvt_selection':  {
          'family':  family,
          'nvt':  {
            '@oid':  check_oid(oid),
          },
        },
      }),
    }
 
    return self.command('modify_config', directives)
 
  def sync(self, **kwargs):
    directives = {
    }
 
    return self.command('sync_config', directives)
 

class Credential(OpenvasObject):
  """ @entity credential """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'allow_insecure':  allow_insecure,
      'certificate':  certificate,
      'key':  {
        'phrase':  phrase,
        'private':  private,
      },
      'login':  login,
      'password':  password,
      'auth_algorithm':  auth_algorithm,
      'community':  community,
      'privacy':  {
        'algorithm':  algorithm,
        'password':  password,
      },
      'type':  type,
    }
 
    return self.command('create_credential', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@credential_id':  check_uuid(credential_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_credential', directives)
 
  def get(self, **kwargs):
    directives = {
      '@credential_id':  check_uuid(credential_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'login':  login,
        'type':  type,
        'allow_insecure':  allow_insecure,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@scanners':  check_boolean(scanners),
      '@trash':  check_boolean(trash),
      '@targets':  check_boolean(targets),
      '@format':  format,
    }
 
    return self.command('get_credentials', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@credential_id':  check_uuid(credential_id),
      'comment':  comment,
      'name':  name,
      'allow_insecure':  allow_insecure,
      'certificate':  certificate,
      'key':  {
        'phrase':  phrase,
        'private':  private,
      },
      'login':  login,
      'password':  password,
      'community':  community,
      'auth_algorithm':  auth_algorithm,
      'privacy':  {
        'algorithm':  algorithm,
        'password':  password,
      },
    }
 
    return self.command('modify_credential', directives)
 

class Filter(OpenvasObject):
  """ @entity filter """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  {
        'make_unique':  make_unique,
      },
      'comment':  comment,
      'copy':  copy,
      'term':  term,
      'type':  type,
    }
 
    return self.command('create_filter', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@filter_id':  check_uuid(filter_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_filter', directives)
 
  def get(self, **kwargs):
    directives = {
      '@filter_id':  check_uuid(filter_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'type':  type,
        'term':  term,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@alerts':  check_boolean(alerts),
    }
 
    return self.command('get_filters', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@filter_id':  check_uuid(filter_id),
      'comment':  comment,
      'name':  name,
      'term':  term,
      'type':  type,
    }
 
    return self.command('modify_filter', directives)
 

class Group(OpenvasObject):
  """ @entity group """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'specials':  {
        'full':  full,
      },
      'users':  users,
    }
 
    return self.command('create_group', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@group_id':  check_uuid(group_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_group', directives)
 
  def get(self, **kwargs):
    directives = {
      '@group_id':  check_uuid(group_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
    }
 
    return self.command('get_groups', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@group_id':  check_uuid(group_id),
      'name':  name,
      'comment':  comment,
      'users':  users,
    }
 
    return self.command('modify_group', directives)
 

class Note(OpenvasObject):
  """ @entity note """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'text':  text,
      'nvt':  {
        '@oid':  check_oid(oid),
      },
      'active':  active,
      'comment':  comment,
      'copy':  copy,
      'hosts':  hosts,
      'port':  port,
      'result':  {
        '@id':  check_uuid(id),
      },
      'severity':  severity,
      'task':  {
        '@id':  check_uuid(id),
      },
      'threat':  threat,
    }
 
    return self.command('create_note', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@note_id':  check_uuid(note_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_note', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@note_id':  check_uuid(note_id),
      'active':  active,
      'hosts':  hosts,
      'port':  port,
      'result':  {
        '@id':  check_uuid(id),
      },
      'severity':  severity,
      'task':  {
        '@id':  check_uuid(id),
      },
      'text':  text,
      'threat':  threat,
    }
 
    return self.command('modify_note', directives)
 

class Override(OpenvasObject):
  """ @entity override """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'text':  text,
      'nvt':  {
        '@oid':  check_oid(oid),
      },
      'active':  active,
      'comment':  comment,
      'copy':  copy,
      'hosts':  hosts,
      'new_severity':  new_severity,
      'new_threat':  new_threat,
      'port':  port,
      'result':  {
        '@id':  check_uuid(id),
      },
      'severity':  severity,
      'task':  {
        '@id':  check_uuid(id),
      },
      'threat':  threat,
    }
 
    return self.command('create_override', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@override_id':  check_uuid(override_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_override', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@override_id':  check_uuid(override_id),
      'active':  active,
      'hosts':  hosts,
      'new_severity':  new_severity,
      'new_threat':  new_threat,
      'port':  port,
      'result':  {
        '@id':  check_uuid(id),
      },
      'task':  {
        '@id':  check_uuid(id),
      },
      'text':  text,
      'severity':  severity,
      'threat':  threat,
    }
 
    return self.command('modify_override', directives)
 

class Permission(OpenvasObject):
  """ @entity permission """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'subject':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
      'resource':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
      'copy':  copy,
      'comment':  comment,
    }
 
    return self.command('create_permission', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@permission_id':  check_uuid(permission_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_permission', directives)
 
  def get(self, **kwargs):
    directives = {
      '@permission_id':  check_uuid(permission_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'type':  type,
        'resource_uuid':  resource_uuid,
        'subject_type':  subject_type,
        'subject':  subject,
        'resource':  resource,
        'subject_uuid':  subject_uuid,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
    }
 
    return self.command('get_permissions', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@permission_id':  check_uuid(permission_id),
      'name':  name,
      'comment':  comment,
      'resource':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
      'subject':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
    }
 
    return self.command('modify_permission', directives)
 

class PortList(OpenvasObject):
  """ @entity port_list """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'port_range':  port_range,
      'get_port_lists_response':  get_port_lists_response,
    }
 
    return self.command('create_port_list', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@port_list_id':  check_uuid(port_list_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_port_list', directives)
 
  def get(self, **kwargs):
    directives = {
      '@port_list_id':  check_uuid(port_list_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'total':  total,
        'tcp':  tcp,
        'udp':  udp,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@details':  check_boolean(details),
      '@targets':  check_boolean(targets),
      '@trash':  check_boolean(trash),
    }
 
    return self.command('get_port_lists', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@port_list_id':  check_uuid(port_list_id),
      'name':  name,
      'comment':  comment,
    }
 
    return self.command('modify_port_list', directives)
 

class PortRange(OpenvasObject):
  """ @entity port_range """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'comment':  comment,
      'port_list':  {
        '@id':  check_uuid(id),
      },
      'start':  start,
      'end':  end,
      'type':  type,
    }
 
    return self.command('create_port_range', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@port_range_id':  check_uuid(port_range_id),
    }
 
    return self.command('delete_port_range', directives)
 

class Report(OpenvasObject):
  """ @entity report """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'report':  check_report(report),
      'task':  {
        '@id':  check_uuid(id),
        'name':  name,
        'comment':  comment,
      },
      'in_assets':  check_boolean(in_assets),
    }
 
    return self.command('create_report', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@report_id':  check_uuid(report_id),
    }
 
    return self.command('delete_report', directives)
 
  def get(self, **kwargs):
    directives = {
      '@report_id':  check_uuid(report_id),
      '@filter':  format_filter({
        'apply_overrides':  apply_overrides,
        'autofp':  autofp,
        'levels':  levels,
        'min_qod':  min_qod,
        'notes':  notes,
        'overrides':  overrides,
        'timezone':  timezone,
        'uuid':  uuid,
        'name':  name,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'host':  host,
        'location':  location,
        'nvt':  nvt,
        'type':  type,
        'original_type':  original_type,
        'auto_type':  auto_type,
        'description':  description,
        'task':  task,
        'report':  report,
        'cvss_base':  cvss_base,
        'nvt_version':  nvt_version,
        'severity':  severity,
        'original_severity':  original_severity,
        'vulnerability':  vulnerability,
        'date':  date,
        'report_id':  report_id,
        'solution_type':  solution_type,
        'qod':  qod,
        'qod_type':  qod_type,
        'task_id':  task_id,
        'cve':  cve,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@report_filter':  check_text({
        'apply_overrides':  apply_overrides,
        'min_qod':  min_qod,
        'uuid':  uuid,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'task_id':  task_id,
        'name':  name,
        'date':  date,
        'status':  status,
        'task':  task,
        'severity':  severity,
        'false_positive':  false_positive,
        'log':  log,
        'low':  low,
        'medium':  medium,
        'high':  high,
        'hosts':  hosts,
        'result_hosts':  result_hosts,
        'fp_per_host':  fp_per_host,
        'log_per_host':  log_per_host,
        'low_per_host':  low_per_host,
        'medium_per_host':  medium_per_host,
        'high_per_host':  high_per_host,
      }),
      '@report_filt_id':  check_uuid(report_filt_id),
      '@type':  type,
      '@format_id':  check_uuid(format_id),
      '@alert_id':  check_uuid(alert_id),
      '@note_details':  check_boolean(note_details),
      '@override_details':  check_boolean(override_details),
      '@host':  check_text(host),
      '@host_first_result':  check_integer(host_first_result),
      '@host_max_results':  check_integer(host_max_results),
      '@host_levels':  check_levels(host_levels),
      '@host_search_phrase':  check_text(host_search_phrase),
      '@pos':  check_integer(pos),
      '@delta_report_id':  check_uuid(delta_report_id),
      '@ignore_pagination':  check_boolean(ignore_pagination),
    }
 
    return self.command('get_reports', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@report_id':  check_uuid(report_id),
      'comment':  comment,
    }
 
    return self.command('modify_report', directives)
 

class ReportFormat(OpenvasObject):
  """ @entity report_format """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'copy':  copy,
      'get_report_formats_response':  get_report_formats_response,
    }
 
    return self.command('create_report_format', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@report_format_id':  check_uuid(report_format_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_report_format', directives)
 
  def get(self, **kwargs):
    directives = {
      '@report_format_id':  check_uuid(report_format_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'extension':  extension,
        'content_type':  content_type,
        'summary':  summary,
        'description':  description,
        'trust':  trust,
        'trust_time':  trust_time,
        'active':  active,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@alerts':  check_boolean(alerts),
      '@params':  check_boolean(params),
      '@details':  check_boolean(details),
    }
 
    return self.command('get_report_formats', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@report_format_id':  check_uuid({
        'active':  active,
        'name':  name,
        'summary':  summary,
        'param':  {
          'name':  name,
          'value':  value,
        },
      }),
    }
 
    return self.command('modify_report_format', directives)
 
  def verify(self, **kwargs):
    directives = {
      '@report_format_id':  check_uuid(report_format_id),
    }
 
    return self.command('verify_report_format', directives)
 

class Role(OpenvasObject):
  """ @entity role """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'users':  users,
    }
 
    return self.command('create_role', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@role_id':  check_uuid(role_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_role', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@role_id':  check_uuid(role_id),
      'name':  name,
      'comment':  comment,
      'users':  users,
    }
 
    return self.command('modify_role', directives)
 

class Scanner(OpenvasObject):
  """ @entity scanner """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'host':  host,
      'port':  port,
      'type':  type,
      'ca_pub':  ca_pub,
      'credential':  {
        '@id':  check_uuid(id),
      },
    }
 
    return self.command('create_scanner', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@scanner_id':  check_uuid(scanner_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_scanner', directives)
 
  def get(self, **kwargs):
    directives = {
      '@scanner_id':  check_uuid(scanner_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'host':  host,
        'port':  port,
        'type':  type,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@details':  check_boolean(details),
    }
 
    return self.command('get_scanners', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@scanner_id':  check_uuid(scanner_id),
      'comment':  comment,
      'name':  name,
      'host':  host,
      'port':  port,
      'type':  check_classic(type),
      'ca_pub':  ca_pub,
      'credential':  {
        '@id':  check_uuid(id),
      },
    }
 
    return self.command('modify_scanner', directives)
 
  def verify(self, **kwargs):
    directives = {
      '@scanner_id':  check_uuid(scanner_id),
    }
 
    return self.command('verify_scanner', directives)
 

class Schedule(OpenvasObject):
  """ @entity schedule """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'first_time':  {
        'minute':  minute,
        'hour':  hour,
        'day_of_month':  day_of_month,
        'month':  month,
        'year':  year,
      },
      'duration':  {
        'unit':  unit,
      },
      'period':  {
        'unit':  unit,
      },
      'timezone':  timezone,
    }
 
    return self.command('create_schedule', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@schedule_id':  check_uuid(schedule_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_schedule', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@schedule_id':  check_uuid(schedule_id),
      'comment':  comment,
      'name':  name,
      'first_time':  {
        'day_of_month':  day_of_month,
        'hour':  hour,
        'minute':  minute,
        'month':  month,
        'year':  year,
      },
      'duration':  {
        'unit':  unit,
      },
      'period':  {
        'unit':  unit,
      },
      'timezone':  timezone,
    }
 
    return self.command('modify_schedule', directives)
 

class Tag(OpenvasObject):
  """ @entity tag """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'resource':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
      'copy':  copy,
      'value':  value,
      'comment':  comment,
      'active':  active,
    }
 
    return self.command('create_tag', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@tag_id':  check_uuid(tag_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_tag', directives)
 
  def get(self, **kwargs):
    directives = {
      '@tag_id':  check_uuid(tag_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'resource_type':  resource_type,
        'resource':  resource,
        'resource_uuid':  resource_uuid,
        'resource_location':  resource_location,
        'active':  active,
        'value':  value,
        'orphan':  orphan,
        'resource_name':  resource_name,
      }),
      '@filt_id':  check_text(filt_id),
      '@trash':  check_boolean(trash),
      '@names_only':  check_boolean(names_only),
    }
 
    return self.command('get_tags', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@tag_id':  check_uuid(tag_id),
      'name':  name,
      'resource':  {
        '@id':  check_uuid(id),
        'type':  type,
      },
      'value':  value,
      'comment':  comment,
      'active':  active,
    }
 
    return self.command('modify_tag', directives)
 

class Target(OpenvasObject):
  """ @entity target """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  {
        'make_unique':  make_unique,
      },
      'comment':  comment,
      'copy':  {
        'asset_hosts':  {
          '@filter':  check_text(filter),
        },
        'hosts':  hosts,
      },
      'exclude_hosts':  exclude_hosts,
      'ssh_credential':  {
        '@id':  check_uuid(id),
        'port':  port,
      },
      'smb_credential':  {
        '@id':  check_uuid(id),
      },
      'esxi_credential':  {
        '@id':  check_uuid(id),
      },
      'snmp_credential':  {
        '@id':  check_uuid(id),
      },
      'ssh_lsc_credential':  {
        '@id':  check_uuid(id),
        'port':  port,
      },
      'smb_lsc_credential':  {
        '@id':  check_uuid(id),
      },
      'esxi_lsc_credential':  {
        '@id':  check_uuid(id),
      },
      'alive_tests':  alive_tests,
      'reverse_lookup_only':  reverse_lookup_only,
      'reverse_lookup_unify':  reverse_lookup_unify,
      'port_range':  port_range,
      'port_list':  {
        '@id':  check_uuid(id),
      },
    }
 
    return self.command('create_target', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@target_id':  check_uuid(target_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_target', directives)
 
  def get(self, **kwargs):
    directives = {
      '@target_id':  check_uuid(target_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'hosts':  hosts,
        'exclude_hosts':  exclude_hosts,
        'ips':  ips,
        'port_list':  port_list,
        'ssh_credential':  ssh_credential,
        'smb_credential':  smb_credential,
        'esxi_credential':  esxi_credential,
        'snmp_credential':  snmp_credential,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@tasks':  check_boolean(tasks),
    }
 
    return self.command('get_targets', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@target_id':  check_uuid(target_id),
      'comment':  comment,
      'name':  name,
      'hosts':  hosts,
      'hosts_ordering':  hosts_ordering,
      'exclude_hosts':  exclude_hosts,
      'ssh_credential':  {
        '@id':  check_uuid(id),
      },
      'smb_credential':  {
        '@id':  check_uuid(id),
      },
      'esxi_credential':  {
        '@id':  check_uuid(id),
      },
      'snmp_credential':  {
        '@id':  check_uuid(id),
      },
      'ssh_lsc_credential':  {
        '@id':  check_uuid(id),
      },
      'smb_lsc_credential':  {
        '@id':  check_uuid(id),
      },
      'esxi_lsc_credential':  {
        '@id':  check_uuid(id),
      },
      'port_list':  {
        '@id':  check_uuid(id),
      },
      'alive_tests':  alive_tests,
      'reverse_lookup_only':  reverse_lookup_only,
      'reverse_lookup_unify':  reverse_lookup_unify,
    }
 
    return self.command('modify_target', directives)
 

class Task(OpenvasObject):
  """ @entity task """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'comment':  comment,
      'copy':  copy,
      'alterable':  alterable,
      'config':  {
        '@id':  check_uuid(id),
      },
      'target':  {
        '@id':  check_uuid(id),
      },
      'hosts_ordering':  hosts_ordering,
      'scanner':  {
        '@id':  check_uuid(id),
      },
      'alert':  {
        '@id':  check_uuid(id),
      },
      'schedule':  {
        '@id':  check_uuid(id),
      },
      'schedule_periods':  schedule_periods,
      'observers':  observers,
      'preferences':  {
        'preference':  {
          'scanner_name':  scanner_name,
          'value':  value,
        },
      },
    }
 
    return self.command('create_task', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
      '@ultimate':  check_boolean(ultimate),
    }
 
    return self.command('delete_task', directives)
 
  def get(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
      '@filter':  format_filter({
        'apply_overrides':  apply_overrides,
        'min_qod':  min_qod,
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'status':  status,
        'total':  total,
        'first_report':  first_report,
        'last_report':  last_report,
        'threat':  threat,
        'trend':  trend,
        'severity':  severity,
        'schedule':  schedule,
        'next_due':  next_due,
        'first':  first,
        'last':  last,
        'false_positive':  false_positive,
        'log':  log,
        'low':  low,
        'medium':  medium,
        'high':  high,
        'hosts':  hosts,
        'result_hosts':  result_hosts,
        'fp_per_host':  fp_per_host,
        'log_per_host':  log_per_host,
        'low_per_host':  low_per_host,
        'medium_per_host':  medium_per_host,
        'high_per_host':  high_per_host,
        'target':  target,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@details':  check_boolean(details),
      '@ignore_pagination':  check_boolean(ignore_pagination),
      '@schedules_only':  check_boolean(schedules_only),
    }
 
    return self.command('get_tasks', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@task_id':  check_uuid({
        'comment':  comment,
        'alert':  {
          '@id':  check_uuid(id),
        },
        'name':  name,
        'observers':  observers,
        'preferences':  {
          'preference':  {
            'scanner_name':  scanner_name,
            'value':  value,
          },
        },
        'schedule':  {
          '@id':  check_uuid(id),
        },
        'schedule_periods':  schedule_periods,
        'scanner':  {
          '@id':  check_uuid(id),
        },
        'file':  {
          '@name':  check_text(name),
          '@action':  action,
        },
      }),
    }
 
    return self.command('modify_task', directives)
 
  def move(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
      '@slave_id':  check_uuid(slave_id),
    }
 
    return self.command('move_task', directives)
 
  def resume(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
    }
 
    return self.command('resume_task', directives)
 
  def start(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
    }
 
    return self.command('start_task', directives)
 
  def stop(self, **kwargs):
    directives = {
      '@task_id':  check_uuid(task_id),
    }
 
    return self.command('stop_task', directives)
 

class User(OpenvasObject):
  """ @entity user """

  def __init__(self): pass

  def create(self, **kwargs):
    directives = {
      'name':  name,
      'copy':  copy,
      'hosts':  {
        '@allow':  check_boolean(allow),
      },
      'ifaces':  {
        '@allow':  check_boolean(allow),
      },
      'password':  password,
      'role':  {
        '@id':  check_uuid(id),
      },
    }
 
    return self.command('create_user', directives)
 
  def delete(self, **kwargs):
    directives = {
      '@user_id':  check_uuid(user_id),
      '@name':  check_text(name),
      '@inheritor_id':  check_text(inheritor_id),
      '@inheritor_name':  check_text(inheritor_name),
    }
 
    return self.command('delete_user', directives)
 
  def get(self, **kwargs):
    directives = {
      '@user_id':  check_uuid(user_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'method':  method,
        'roles':  roles,
        'groups':  groups,
        'hosts':  hosts,
        'ifaces':  ifaces,
      }),
      '@filt_id':  check_uuid(filt_id),
    }
 
    return self.command('get_users', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@user_id':  check_uuid(user_id),
      'name':  name,
      'new_name':  new_name,
      'password':  password,
      'role':  {
        '@id':  check_uuid(id),
      },
      'hosts':  {
        '@allow':  check_boolean(allow),
      },
      'ifaces':  {
        '@allow':  check_boolean(allow),
      },
      'sources':  check_sources(sources),
    }
 
    return self.command('modify_user', directives)
 

class Auth(OpenvasObject):
  """ @entity auth """

  def __init__(self): pass

  def describe(self, **kwargs):
    directives = {
    }
 
    return self.command('describe_auth', directives)
 
  def modify(self, **kwargs):
    directives = {
      'group':  {
        'auth_conf_setting':  {
          'key':  key,
          'value':  value,
        },
      },
    }
 
    return self.command('modify_auth', directives)
 

class Trashcan(OpenvasObject):
  """ @entity trashcan """

  def __init__(self): pass

  def empty(self, **kwargs):
    directives = {
    }
 
    return self.command('empty_trashcan', directives)
 

class Aggregates(OpenvasObject):
  """ @entity aggregates """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@filter':  check_text(filter),
      '@filt_id':  check_uuid(filt_id),
      '@type':  check_text(type),
      '@data_column':  check_text(data_column),
      '@group_column':  check_text(group_column),
      '@subgroup_column':  check_text(subgroup_column),
      '@sort_field':  check_text(sort_field),
      '@sort_order':  sort_order,
      '@sort_stat':  sort_stat,
      '@first_group':  check_integer(first_group),
      '@max_groups':  check_integer(max_groups),
      '@mode':  mode,
      'sort':  {
        '@sort_field':  check_text(sort_field),
        '@sort_order':  sort_order,
        '@sort_stat':  sort_stat,
      },
      'data_column':  check_text(data_column),
      'text_column':  check_text(text_column),
    }
 
    return self.command('get_aggregates', directives)
 

class Feed(OpenvasObject):
  """ @entity feed """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@type':  check_text(type),
    }
 
    return self.command('get_feeds', directives)
 
  def sync(self, **kwargs):
    directives = {
    }
 
    return self.command('sync_feed', directives)
 

class Info(OpenvasObject):
  """ @entity info """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@type':  check_text(type),
      '@name':  check_text(name),
      '@info_id':  check_text(info_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'severity':  severity,
        'version':  version,
        'summary':  summary,
        'cve':  cve,
        'xref':  xref,
        'family':  family,
        'cvss':  cvss,
        'cvss_base':  cvss_base,
        'script_tags':  script_tags,
        'qod':  qod,
        'qod_type':  qod_type,
        'solution_type':  solution_type,
        'vector':  vector,
        'complexity':  complexity,
        'authentication':  authentication,
        'confidentiality_impact':  confidentiality_impact,
        'integrity_impact':  integrity_impact,
        'availability_impact':  availability_impact,
        'products':  products,
        'cvss':  cvss,
        'description':  description,
        'published':  published,
        'title':  title,
        'status':  status,
        'deprecated_by_id':  deprecated_by_id,
        'max_cvss':  max_cvss,
        'cves':  cves,
        'nvd_id':  nvd_id,
        'version':  version,
        'deprecated':  deprecated,
        'title':  title,
        'description':  description,
        'file':  file,
        'status':  status,
        'max_cvss':  max_cvss,
        'cves':  cves,
        'title':  title,
        'summary':  summary,
        'cves':  cves,
        'max_cvss':  max_cvss,
        'type':  type,
        'extra':  extra,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@details':  check_boolean(details),
    }
 
    return self.command('get_info', directives)
 

class Notes(OpenvasObject):
  """ @entity notes """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@note_id':  check_uuid(note_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'nvt':  nvt,
        'text':  text,
        'nvt_id':  nvt_id,
        'task_name':  task_name,
        'task_id':  task_id,
        'hosts':  hosts,
        'port':  port,
        'active':  active,
        'result':  result,
        'severity':  severity,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@nvt_oid':  check_oid(nvt_oid),
      '@task_id':  check_uuid(task_id),
      '@details':  check_boolean(details),
      '@result':  check_boolean(result),
    }
 
    return self.command('get_notes', directives)
 

class Nvt(OpenvasObject):
  """ @entity nvt """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@nvt_oid':  check_oid(nvt_oid),
      '@details':  check_boolean(details),
      '@preferences':  check_boolean(preferences),
      '@preference_count':  check_boolean(preference_count),
      '@timeout':  check_boolean(timeout),
      '@config_id':  check_uuid(config_id),
      '@preferences_config_id':  check_uuid(preferences_config_id),
      '@family':  check_text(family),
      '@sort_order':  check_sort_order(sort_order),
      '@sort_field':  check_text(sort_field),
    }
 
    return self.command('get_nvts', directives)
 

class NvtFamilies(OpenvasObject):
  """ @entity nvt_families """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@sort_order':  check_sort_order(sort_order),
    }
 
    return self.command('get_nvt_families', directives)
 

class Overrides(OpenvasObject):
  """ @entity overrides """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@override_id':  check_uuid(override_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'nvt':  nvt,
        'text':  text,
        'nvt_id':  nvt_id,
        'task_name':  task_name,
        'task_id':  task_id,
        'hosts':  hosts,
        'port':  port,
        'threat':  threat,
        'new_threat':  new_threat,
        'active':  active,
        'result':  result,
        'severity':  severity,
        'new_severity':  new_severity,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@nvt_oid':  check_oid(nvt_oid),
      '@task_id':  check_uuid(task_id),
      '@details':  check_boolean(details),
      '@result':  check_boolean(result),
    }
 
    return self.command('get_overrides', directives)
 

class Preferences(OpenvasObject):
  """ @entity preferences """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@nvt_oid':  check_oid(nvt_oid),
      '@config_id':  check_uuid(config_id),
      '@preference':  check_text(preference),
    }
 
    return self.command('get_preferences', directives)
 

class Result(OpenvasObject):
  """ @entity result """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@result_id':  check_uuid(result_id),
      '@filter':  format_filter({
        'apply_overrides':  apply_overrides,
        'autofp':  autofp,
        'levels':  levels,
        'min_qod':  min_qod,
        'notes':  notes,
        'overrides':  overrides,
        'timezone':  timezone,
        'uuid':  uuid,
        'name':  name,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'host':  host,
        'location':  location,
        'nvt':  nvt,
        'type':  type,
        'original_type':  original_type,
        'auto_type':  auto_type,
        'description':  description,
        'task':  task,
        'report':  report,
        'cvss_base':  cvss_base,
        'nvt_version':  nvt_version,
        'severity':  severity,
        'original_severity':  original_severity,
        'vulnerability':  vulnerability,
        'date':  date,
        'report_id':  report_id,
        'solution_type':  solution_type,
        'qod':  qod,
        'qod_type':  qod_type,
        'task_id':  task_id,
        'cve':  cve,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@task_id':  check_uuid(task_id),
      '@note_details':  check_boolean(note_details),
      '@override_details':  check_boolean(override_details),
      '@details':  check_boolean(details),
    }
 
    return self.command('get_results', directives)
 

class Roles(OpenvasObject):
  """ @entity roles """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@role_id':  check_uuid(role_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
    }
 
    return self.command('get_roles', directives)
 

class Schedules(OpenvasObject):
  """ @entity schedules """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@schedule_id':  check_uuid(schedule_id),
      '@filter':  format_filter({
        'uuid':  uuid,
        'name':  name,
        'comment':  comment,
        'created':  created,
        'modified':  modified,
        'owner':  owner,
        'first_time':  first_time,
        'period':  period,
        'period_months':  period_months,
        'duration':  duration,
        'timezone':  timezone,
        'initial_offset':  initial_offset,
        'first_run':  first_run,
        'next_run':  next_run,
      }),
      '@filt_id':  check_uuid(filt_id),
      '@trash':  check_boolean(trash),
      '@tasks':  check_boolean(tasks),
    }
 
    return self.command('get_schedules', directives)
 

class Setting(OpenvasObject):
  """ @entity setting """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@setting_id':  check_uuid(setting_id),
      '@filter':  format_filter({
        'name':  name,
        'comment':  comment,
        'value':  value,
      }),
      '@first':  check_integer(first),
      '@max':  check_integer(max),
      '@sort_order':  check_sort_order(sort_order),
      '@sort_field':  check_text(sort_field),
    }
 
    return self.command('get_settings', directives)
 
  def modify(self, **kwargs):
    directives = {
      '@setting_id':  check_uuid(setting_id),
      'name':  name,
      'value':  value,
    }
 
    return self.command('modify_setting', directives)
 

class SystemReport(OpenvasObject):
  """ @entity system_report """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
      '@name':  check_text(name),
      '@duration':  check_integer(duration),
      '@start_time':  check_iso_time(start_time),
      '@end_time':  check_iso_time(end_time),
      '@brief':  check_boolean(brief),
      '@slave_id':  check_uuid(slave_id),
    }
 
    return self.command('get_system_reports', directives)
 

class Version(OpenvasObject):
  """ @entity version """

  def __init__(self): pass

  def get(self, **kwargs):
    directives = {
    }
 
    return self.command('get_version', directives)
 

class Wizard(OpenvasObject):
  """ @entity wizard """

  def __init__(self): pass

  def run(self, **kwargs):
    directives = {
      'mode':  mode,
      'name':  name,
      'params':  {
        'param':  {
          'name':  name,
          'value':  value,
        },
      },
      '@read_only':  check_boolean(read_only),
    }
 
    return self.command('run_wizard', directives)
 

class Cert(OpenvasObject):
  """ @entity cert """

  def __init__(self): pass

  def sync(self, **kwargs):
    directives = {
    }
 
    return self.command('sync_cert', directives)
 

class Scap(OpenvasObject):
  """ @entity scap """

  def __init__(self): pass

  def sync(self, **kwargs):
    directives = {
    }
 
    return self.command('sync_scap', directives)
 
