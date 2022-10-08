# Authentication methods

The main program, simulates an authentication process using command line arguments.

```
$ python3 main.py --help
usage: generator [-h] [-r REGISTER] [-l LOGIN] [-i INIT]

Auth and names generator params

options:
  -h, --help            show this help message and exit
  -r REGISTER, --register REGISTER
                        Register a new user, requested parameters: { email }
  -l LOGIN, --login LOGIN
                        Login action will print a bearer token, requested parameters: { username, password }
  -i INIT, --init INIT  Init action, will print success or failed, requested parameters: { token, password }
```

## Steps to interact

Initial state, the database is empty or the file does not exists.

### 1. Register action

```
$ python3 main.py -r '{ "email": "msanxes@institutmontilivi.cat" }'
[INFO] 2022-10-08 18:51:21,292 YhaZfluFycdyvswyel_Tt1zYBeQwOkPxA3ITvGqFeNVgc1qW5e2UjSMC33BmEokWEd7iVM9TVwOfPu77Jhp8Aw
```

Database state:

```
{
  "users": [
    {
      "email": "msanxes@institutmontilivi.cat",
      "token": "YhaZfluFycdyvswyel_Tt1zYBeQwOkPxA3ITvGqFeNVgc1qW5e2UjSMC33BmEokWEd7iVM9TVwOfPu77Jhp8Aw"
    }
  ]
}
```

> A token has been generated that will be used to authenticate that the user has requested the register. Using this token the user will be able to initilize his password.

### 2. Init action

```
$ python3 main.py -i '{ "token": "YhaZfluFycdyvswyel_Tt1zYBeQwOkPxA3ITvGqFeNVgc1qW5e2UjSMC33BmEokWEd7iVM9TVwOfPu77Jhp8Aw", "password": "1234" }'
```

Database state:

```
{
    "users": [
        {
            "email": "msanxes@institutmontilivi.cat",
            "token": null,
            "salt": "e592206b326ebc740aa84379b57ec5e7",
            "hash": "1f980bffa33ac5d8cb1e65cd95c8335e60ea3ded5a1d14552505ed0f1833572ef58aa3ec4b1cadd646da2e31f75e192adbb020cb6649540cf5230a68271d0693"
        }
    ]
}
```

> No output expected, the token has been used to initilize the password, we have stored the salt and the hash. The token is set to null. (using pbkdf2_hmac algorithm from hashlib)

# 3. Login action

```

```

Database state:

```

```

>

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
$ python3 generator/generator.py -h
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
$ python3 generator/generator.py -n 10
[INFO] 2022-09-21 22:08:31,840 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:08:31,920 [0.08019185066223145s]: list generation
[INFO] 2022-09-21 22:08:31,920 [0.00029397010803222656s]: writting json
[INFO] 2022-09-21 22:08:31,921  -- -- Finished -- --
```

```
$ python3 generator/generator.py -n 1000
[INFO] 2022-09-21 22:09:11,918 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:09:17,570 [5.6528003215789795s]: list generation
[INFO] 2022-09-21 22:09:17,580 [0.009092569351196289s]: writting json
[INFO] 2022-09-21 22:09:17,580  -- -- Finished -- --
```

```
python3 generator/generator.py -n 100000
[INFO] 2022-09-21 22:09:53,201 Parameters readed, I have 5 authentication methods
[INFO] 2022-09-21 22:18:19,303 [506.10190534591675s]: list generation
[INFO] 2022-09-21 22:18:19,931 [0.6280190944671631s]: writting json
[INFO] 2022-09-21 22:18:19,931  -- -- Finished -- --
```
