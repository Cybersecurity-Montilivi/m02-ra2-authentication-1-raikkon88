# Authentication generation

This program generates a list of names with authentication methods retrieved from a json file. 

## Input file

Accepts every possible format regarding the json input. In this documentation we will suppose that the format accepted as an input file is the following: 

```
[
    {
        "oauth": {
            "name": "OAuth",
            "description": "The other apps can reuse google authentication"
        }
    },
    {
        "showDNI": {
            "name": "Show a DNI",
            "description": "A person can identify the other throughout the person's picture"
        }
    }
]
```

## Output file

The output file will have the following format:

```
[
    {
        "name": "Ina Earp Redd",
        "authentications": [
            {
                "oauth": {
                    "name": "OAuth",
                    "description": "The other apps can reuse google authentication"
                }
            },
            {
                "showDNI": {
                    "name": "Show a DNI",
                    "description": "A person can identify the other throughout the person's picture"
                }
            },
            {
                "fingerprint": {
                    "name": "Fingerprint",
                    "description": "Biometric way to identify a person"
                }
            },
            {
                "2FA": {
                    "name": "Two factor authentication",
                    "description": "Resource used by companies to verify a user is who must be with different devices"
                }
            },
            {
                "jwt": {
                    "name": "Json web token authentication",
                    "description": "String based authentication that allows communication mostly with web services"
                }
            }
        ]
    },
    {
        "name": "John Glass Forcier",
        "authentications": [
            {
                "oauth": {
                    "name": "OAuth",
                    "description": "The other apps can reuse google authentication"
                }
            },
            {
                "showDNI": {
                    "name": "Show a DNI",
                    "description": "A person can identify the other throughout the person's picture"
                }
            },
            {
                "fingerprint": {
                    "name": "Fingerprint",
                    "description": "Biometric way to identify a person"
                }
            },
            {
                "2FA": {
                    "name": "Two factor authentication",
                    "description": "Resource used by companies to verify a user is who must be with different devices"
                }
            },
            {
                "jwt": {
                    "name": "Json web token authentication",
                    "description": "String based authentication that allows communication mostly with web services"
                }
            }
        ]
    }
]
```

## Execution

Help is listed above: 

```
$ python3 generator.py -h   
usage: generator [-h] [-s SOURCE_PATH] [-d DEST_PATH] [-n TOTAL_PEOPLE]

Auth and names generator params

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_PATH, --source-path SOURCE_PATH
                        Source path to read the authentication methods
  -d DEST_PATH, --dest-path DEST_PATH
                        Destination path to store the generated file
  -n TOTAL_PEOPLE, --total-people TOTAL_PEOPLE
                        Number of people to generate
```

By default the arguments are:

- Source path -> `./auth.json`
- Destination path -> `./generated.json`
- Total people -> `10`

### Execution examples:

```
$ python3 generator.py -n 10
[INFO] 2022-09-21 22:08:31,840 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:08:31,920 [0.08019185066223145s]: list generation
[INFO] 2022-09-21 22:08:31,920 [0.00029397010803222656s]: writting json
[INFO] 2022-09-21 22:08:31,921  -- -- Finished -- -- 
```

```
$ python3 generator.py -n 1000
[INFO] 2022-09-21 22:09:11,918 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:09:17,570 [5.6528003215789795s]: list generation
[INFO] 2022-09-21 22:09:17,580 [0.009092569351196289s]: writting json
[INFO] 2022-09-21 22:09:17,580  -- -- Finished -- -- 
```

```
python3 generator.py -n 100000
[INFO] 2022-09-21 22:09:53,201 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:18:19,303 [506.10190534591675s]: list generation
[INFO] 2022-09-21 22:18:19,931 [0.6280190944671631s]: writting json
[INFO] 2022-09-21 22:18:19,931  -- -- Finished -- -- 
```
