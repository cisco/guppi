| Description                                     | Command                                                      |
| :---------------------------------------------: | ------------------------------------------------------------ |
| view available cloud service names              | %guppi cloud                                                 |
| view running cloud instances                    | %guppi cloud *cloud_service* view                            |
| view all running cloud instances                | %guppi cloud multicloud view                                 |
| create a new instance                           | %guppi cloud *cloud_service* create                          |
| ssh into running cloud instances with a GUI     | %guppi cloud *cloud_service* ssh view                        |
| ssh into all running cloud instances with a GUI | %guppi cloud multicloud ssh view                             |
| ssh into running cloud instances without a GUI  | %guppi cloud *cloud_service* ssh [v] *group_name* *commands* |