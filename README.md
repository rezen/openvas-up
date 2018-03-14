# openvas-up
Takes interacting with OpenVAS up to the next level. The library enables you to interact with the OpenVAS manager via it's custom protocol,  omp. The goal is to be simple and readable.

```python
from openvasup.model import OpenvasObject
from openvasup.scan import Task

# Default creds for Docker image  mikesplain/openvas
username = 'admin'
password = 'admin'

# Login
OpenvasObject.connect(username=username, password=password)

# Get scan tasks
tasks = Task.get_by_name("Scan of 127.0.0.1")

``` 

## Requirements
- Python
- OpenVAS 9

## Getting Started
I've done most of the development with Docker which makes getting going with OpenVAS pretty quick.

`docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`

There is an example you can run in the `examples/` directory.

## Ideas
- Automatically tag asset hosts based on scan results

## Testing
Tests are all in the `tests/` directory and are setup to use `pytest`

DO NOT EVER RUN IN PRODUCTION!

```
python -m pip install -U pip
pip install pytest mock
python -m pytest tests/
```


```
/var/lib/openvas/mgr/tasks.db

sqlite> 
PRAGMA table_info(config_preferences);

sqlite> .tables
agents                             permissions_trash                
agents_trash                       port_lists                       
alert_condition_data               port_lists_trash                 
alert_condition_data_trash         port_names                       
alert_event_data                   port_ranges                      
alert_event_data_trash             port_ranges_trash                
alert_method_data                  report_counts                    
alert_method_data_trash            report_format_param_options      
alerts                             report_format_param_options_trash
alerts_trash                       report_format_params             
auth_cache                         report_format_params_trash       
config_preferences                 report_formats                   
config_preferences_trash           report_formats_trash             
configs                            report_host_details              
configs_trash                      report_hosts                     
credentials                        reports                          
credentials_data                   resources_predefined             
credentials_trash                  result_new_severities            
credentials_trash_data             result_overrides                 
filters                            results                          
filters_trash                      results_autofp                   
group_users                        role_users                       
group_users_trash                  role_users_trash                 
groups                             roles                            
groups_trash                       roles_trash                      
host_details                       scanners                         
host_identifiers                   scanners_trash                   
host_max_severities                schedules                        
host_oss                           schedules_trash                  
hosts                              settings                         
meta                               tags                             
notes                              tags_trash                       
notes_trash                        targets                          
nvt_cves                           targets_login_data               
nvt_preferences                    targets_trash                    
nvt_selectors                      targets_trash_login_data         
nvts                               task_alerts                      
oss                                task_files                       
overrides                          task_preferences                 
overrides_trash                    tasks                            
permissions                        users 
```