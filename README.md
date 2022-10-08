# Authentication methods

The main program, simulates an authentication process using command line arguments. This program will generate 2 files if they are not already generated:

- db.json -> Simulates the database
- pk.pem -> A private key that will be used to generate bearer tokens.

## Program help

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

We send the username and the password to realize the login

```
$ python3 main.py -l '{"email":"msanxes@institutmontilivi.cat","password":"1234"}'
[INFO] 2022-10-08 19:56:17,806 eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJlbWFpbCI6ICJtc2FueGVzQGluc3RpdHV0bW9udGlsaXZpLmNhdCIsICJpYXQiOiAxNjY1MjUxNzc3LCAiZXhwIjogMTY2NTg1NjU3N30.c4qhOTnaMehzD3Yyp-ixYNz3v6ZWIrxNfq7Ta3OCQoSjQ3yR35Vjclzi4dtMhiidH6MDgkQA1YFR11wHBKs-F0I6MD0Td6n8BsQjAD2vOxNPd9gDbupEiipS90ztm1HirmwfPoZq30GtCbou5WM6xpfyj3QmofcZq0VF5adNR42pqXQcm-TkEj_xMtIka7OPad2FyN8k5pLcK0-vmfuto-kqugorsj9_71ci1CshNCjW_5oIo5DuYWRj0LFHwRtJ8D1gW06OkfModym0Hzn_6Yi2LM40CkKrRhvhfVEkPPxoK73Tzc7B803bO62DmC9ao1URv4UnW_IAAo36veM4KeIurCUOjRRWV012tnLZ0pmUJMSrE0K63csg5GMd_0xU_JUGwwUJzFHtaO3P1u0yPRQfksldGB3bRlO3CKLToplhRWAgDt-p1DRYbwpmZJ4RUnub7AjcLe5LKLqf0440fsrMXzVsDUVSNz80McYmB94M9jzAHlZ8NFTGNCijVoF4hmxHmVyE86cgdgYXrhCBnqMeBox2XHjap3RvUErHqzGu2NVVqEi5nTObBUMdi2la0sPjmOXjsfaKZS7wZE2WtEXEv2vxArfcw0lOPUaTq-qBXExt0JG0KzoME_jCD-6nTj3dF-UjMyZiIqaXeeFBBYwIAPbIZ-qVG4WOrC7PUWU
```

In this case a token bearer is printed. This token contains some information about:

- iat
- exp
- user email

All is signed with RS256

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

> The database stays as it no changes expected.

## Authorize action

Using the token generated in the previous step (login action) we want to authorize the user action.

```
$ python3 main.py -a '{"authorization":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJlbWFpbCI6ICJtc2FueGVzQGluc3RpdHV0bW9udGlsaXZpLmNhdCIsICJpYXQiOiAxNjY1MjUzODA3LCAiZXhwIjogMTY2NTg1ODYwN30.ReeGs1lQbxLx992Nd3j3tMqzUudbEacfmVs_9IqvBtaRUo2eHaH5OrvYeM7lCJMghHKehILPdOrOgWv59wh4qF_qE4-1plOMuRlNzma5NnMFIN0KUy2vit2toKw4e-Na67ELtSOdGW5cLKspd3oyvJ2UxKB-2wJ5Vqppi7tJBhul4k_cmeznLsKQLbwjQUIQddJEyQfmcqkqOMNBw6LEohSPmdNjRu2LkSo_hD-GwIx6Bc7B51URckJ7TVq14S0Vs836buqGueeu1PbdaF7ggpMwzbogTfbka14CFiEZMrCm5U2jJYthVIJXFPPS9Z5mGgcwbqrbOCOR6lmQIAb-BBrPjgpO7z8M-0Wq9KEVpF4d3bn1UdDrFj1Uc1tnBvQPypv6yb4lYd53iXKbPKyG3CNvKQ2nK2ugMdXpJ6bm6n2omz4YoInq2PpNXLgzNwWpaultBmLqC95YF8kWTyMjRuDxJSlSF-nY64trH1OOSUSiVmPLxe63MwF8K2WYz1FpmMdZ1G8BvOqPhaLeRjjgJk6PLebdi_S5mCwqXYPw4mKW6mgOgrbl-evMw-XgY2UVbO2fVtlaN3SJFvOKwNlCz1Hi5SRnNxDqAB5YIJp0xTf2id3EJfBoiR15hrJsPwfUZv0u-Pk_ValTIqUiUTjAGbYeDLv7vHBE2Ef2LSHCDR4"}'
[INFO] 2022-10-08 20:31:14,763 {'email': 'msanxes@institutmontilivi.cat', 'iat': 1665253807, 'exp': 1665858607}
```

The user is printed:

```
{
  "email": "msanxes@institutmontilivi.cat",
  "iat": 1665253807,
  "exp": 1665858607
}
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

> The database stays as it no changes expected.

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
