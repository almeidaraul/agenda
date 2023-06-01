<h1 align="center">Agenda</h1>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![GitHub Issues](https://img.shields.io/github/issues/almeidaraul/agenda)](https://github.com/almeidaraul/agenda/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/almeidaraul/agenda)](https://github.com/almeidaraul/agenda/pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Simple scheduler for executing detailed command-line programs
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## 🧐 About <a name = "about"></a>
**Agenda** is a tool for scheduling command-line programs with too many arguments. It allows the user to configure many runs at once in a configuration file and run a single, simple command that will take care of the rest. This makes running tests, experiments and per-batch scripts a lot easier.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
**Agenda** is built using Python3. Install dependencies from `src/requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### Installing
Locally install **agenda** with pip so it can be used from anywhere in your machine:

```bash
pip3 install -e .
```

## 🔧 Running the tests <a name = "tests"></a>
Automated tests are implemented with PyTest. After installing project requirements, run `pytest` from the `src` directory.

## 🎈 Usage <a name="usage"></a>
The goal of **agenda** is to be simple. All you need is a configuration JSON file and a goal in mind.

As an example, suppose you have a Python program that trains a neural network on one of a range of possible train datasets and then sends its accuracy on a test dataset to someone's email address. You would normally run it by writing `python3 main.py --train TRAIN_DATASET --test TEST_DATASET --target_email EMAIL@PROVIDER.COM`. This is okay if you're doing it once, but in many cases you'll want to run this command with many different values for `train`, `test` and `target_email`. You would have to type that out, run the first experiment, then type it out again with a different set of arguments, run the second experiment, and so it goes.

With **agenda**, your work is put into deciding what you'll be executing. The only command you run is actually pretty simple. You can configure these runs like so, in a JSON file:

```json
{
  "required_keys": ["train", "test"],
  "log_header": "This is really easy!",
  "prefix": "python3 main.py",
  "cmds": [
    {
      "train": "train_dataset_1",
      "test": "test_dataset_1"
    },
    {
      "train": "train_dataset_1",
      "test": "test_dataset_2",
      "target_email": "email@provider.com"
    },
    {
      "env_variables": {
        "CUDA_VISIBLE_DEVICES": "5,7"
      },
      "train": "train_dataset_2",
      "test": "test_dataset_3"
    }
  ]
}
```

Let's go through that step by step.
- `required_keys` is optional; if it is provided, **agenda** will look for these arguments in every command and, if it isn't there, it will raise an error.
- `log_header` is also optional and lets you write some initial message to the log file.
- `prefix` is a common prefix in all of the commands.
- `cmds` is a list of all the commands that will be run. Each of its elements is a dictionary and each key in this dictionary is a command-line argument to be run, except for...
- `env_variables` (optional) contains environment variables to be set before the command runs.

Finally, you can easily run all of these experiments with a single command, like so:

```bash
python3 agenda.py --config config.json --output output.txt
```

This is equivalent to these 3 commands:
```bash
python3 main.py --train train_dataset_1 --test test_dataset_1
python3 main.py --train train_dataset_1 --test test_dataset_2 --target_email email@provider.com
CUDA_VISIBLE_DEVICES=5,7 python3 main.py --train train_dataset_2 --test test_dataset_3
```
