# Colony CLI

[![Coverage Status](https://coveralls.io/repos/github/QualiSystemsLab/colony-cli/badge.svg?branch=dev)](https://coveralls.io/github/QualiSystemsLab/colony-cli?branch=dev)
![CI](https://github.com/QualiSystemsLab/colony-cli/workflows/CI/badge.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/colony-cli.svg)](https://badge.fury.io/py/colony-cli)
[![Maintainability](https://api.codeclimate.com/v1/badges/5a9f730163de9b6231e6/maintainability)](https://codeclimate.com/github/QualiSystemsLab/colony-cli/maintainability)


---

![quali](quali.png)

## Cloudshell Colony Cli

Colony Cli is a command line interface to Colony.

The main functionality this tool currently provides is a validation of your colony blueprints. But there are many
plans to turn it to the unified tool for accessing and managing all Colony's services.

## Why use Colony Cli

When developing blueprints for Colony, it can be very helpful to immediately check your work for errors.

Let's assume you are currently working in *development* branch, and you also have some main branch which is connected
to Colony. You would like to be sure that your latest committed changes haven't broken anything before merge them to
the main branch.

This is where this tool might be handy for you. Instead of reconnecting Colony to your development branch in UI you can
use Colony Cli to validate your current blueprints state and even launch sandboxes from them.

## Installing

You can install Colony Cli with [pip](https://pip.pypa.io/en/stable/):

`$ python -m pip install colony-cli`

Or if you want to install it for your user:

`$ python -m pip install --user colony-cli`

### Configuration

First of all you need to generate access token in Colony UI in a Settings.
Then, you need to configure Colony Cli with generated token and colony space you are going to access.
There are three ways how to do it:

* Create a configuration file ~/.colony/config where you can have several profiles:

```bash
[default]
token = xxxyyyzzz
space = DemoSpace

[user]
token = aaabbbccc
space = TestSpace
```


* Set environment variables:

```bash
export COLONY_TOKEN = xxxzzzyyy
export COLONY_SPACE = demo_space
```

* Specify _--space_ and _--token_ options then running command:

`$ colony --space=trial --token=xxxyyyzzz <command>`



## Basic Usage

Colony Cli currently allows you to make two actions:

- validate blueprint (using `colony bp validate` command)
- start sandbox (via `colony sb start`)

In order to get help run:

`$ colony --help`

It will give you detailed output with usage:

```bash
$ colony --help
Usage: colony ( [(--space=<space> --token=<token>)] | [--profile=<profile>] ) [--help] [--debug]
              <command> [<args>...]

Options:
  -h --help             Show this screen.
  --space=<space>       Colony Space name
  --token=<token>       Specify token generated by Colony
  --profile=<profile>   Profile indicates a section in config file.
                        If set neither --token or --space must not be specified.

Commands:
    bp, blueprint       validate colony blueprints
    sb, sandbox         start sandbox
```

You can elaborate help message for a particular command, specifying *--help* flag after command name, like:

```bash
$ colony sb --help
    usage:
        colony (sb | sandbox) start <blueprint_name> [options]
        colony (sb | sandbox) [--help]

    options:
       -h --help        Show this message
       -d, --duration <minutes>
       -n, --name <sandbox_name>
       -i, --inputs <input_params>
       -a, --artifacts <artifacts>
       -b, --branch <branch>
       -c, --commit <commitId>
```

### Blueprint validation

* If you are currently inside git-enabled folder containing your blueprint, commit and push your latest changes and run:

`$ colony bp validate MyBlueprint`

* If you want to check another blueprint from another branch you can specify --branch argument or even elaborate in a
specific point of time by setting --commit:

`$ colony bp validate MyBlueprint --branch dev --commit fb88a5e3275q5d54697cff82a160a29885dfed24`

---
**NOTE**

If you are not it git-enabled folder of your blueprint repo and haven't set --branch/--commit arguments tool will
validate blueprint with name "MyBlueprint" from branch currently attached to your Colony space.

---

If blueprint is valid you will get output with "Valid" message. If no, it will print you a table with found errors

**Example:**

```bash
$colony blueprint validate Jenkins -b master


message                                                                      name                             code
---------------------------------------------------------------------------  -------------------------------  -------------------------------
Cloud account: AWS is not recognized as a valid cloud account in this space  Blueprint unknown cloud account  BLUEPRINT_UNKNOWN_CLOUD_ACCOUNT
```

### Launching sandbox

* similar to the previous command you can omit *--branch/--commit* arguments if you are in a git-enabled folder of your
blueprint repo:

`colony sb start MyBlueprint`

* this will run you a sandbox from specified blueprint

* if you want to start sandbox from specific state of blueprint, specify _--branch_ and _--commit_ arguments:

`colony sb start MyBlueprint --branch dev --commit fb88a5e3275q5d54697cff82a160a29885dfed24`

* lets review another options you can set here:
  * `-d, --duration <minutes>` - you can specify duration of sandbox reservation in minutes. Default is 120 minutes
  * `-n, --name <sandbox_name>` - the name of sandbox you want to run. By default it will generate name using current timestamp
  * `-i, --inputs <input_params>` - comma-separated list of input parameters for sandbox, like: _"param1=val1, param2=val2_
  * `-a, --artifacts <artifacts>` - comma-separated list of sandbox artifacts, like: _app1=path1, app2=path2_

---
**NOTE**

1. If you are not it git-enabled folder of your blueprint repo and haven't set --branch/--commit arguments tool will
start sandbox using blueprint with name "MyBlueprint" from branch currently attached to your Colony space.

2. If you omit artifacts and inputs options, you are inside a git enabled folder and the local is in sync with remote
then Colony Cli will try to get default values for artifacts and inputs from blueprint yaml.
---

Result of a command is a Sandbox ID.

**Example**:

```bash
colony sb start MyBlueprint --inputs "CS_COLONY_TOKEN=ABCD, IAM_ROLE=s3access-profile, BUCKET_NAME=abc"

ybufpamyok03c11
```


## Troubleshooting and Help

For questions, bug reports or feature requests, please refer to the [Issue Tracker]. Also, make sure you check out our [Issue Template](.github/issue_template.md).

## Contributing


All your contributions are welcomed and encouraged. We've compiled detailed information about:

* [Contributing](.github/contributing.md)
* [Creating Pull Requests](.github/pull_request_template.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)
