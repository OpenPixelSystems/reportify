# Reportify

## Summary

The `generate.py` script can be used to generate tests reports.

## Usage

Install dependencies via `pip -r requirements.txt`

```
usage: generate.py [-h] -i INPUT -o OUTPUT -t TITLE [-d] [-s] [-v]

options:
  -h, --help                    show this help message and exit
  -i INPUT, --input INPUT       path to JSON input files (e.g., "json1,json2")
  -o OUTPUT, --output OUTPUT    path to HTML output file
  -t TITLE, --title TITLE       title of the report
  -d, --dynamic                 generate dynamic report
  -s, --self-test               include self tests
  -v, --verbose                 verbose output
```

## Generating example test file 

Inside the folder tests, an example of how to structure a pytest test file can be found. Also, `tests/test_helpers.py` is a very import file which is used to automate some of the metadata generation. This file should be included in all pytest files which generate output that needs to end up in the report.

``` sh
pytest --json-report --json-report-file=example.json ./tests/
```

## Adding metadata to the test

Every test should contain the following data as a minimum:
``` python
def test_pass(suite, json_metadata):
    """
    Success test on purpose to test report generator
    Note: this test should not make it into the reports
    """
    # Add some metadata to the test
    json_metadata["device"] = "virtual"
    json_metadata["description"] = get_docstr()
    json_metadata["active_test"] = get_name()
    json_metadata["steps"] = 0 # should always be 0

    # Add tests here

```

These parameters are used to uniquely identify a test and add the test description and function name to the report. The device parameter is optional. This is mainly useful if one test gets run on multiple devices, allowing unique identification of each run.

### Adding documented steps

In order to easily create links between test documentation and the tests themselves, the generator can add step descriptions.
This is done as follows:
``` python
def test_with_steps(suite, json_metadata):
    """
    Example test with multiple steps defined
    """
    # Add some metadata to the test
    json_metadata["device"] = "test device 1"
    json_metadata["active_test"] = get_name()
    json_metadata["description"] = get_docstr()
    json_metadata["steps"] = 0

    def step_1():
        assert True

    def step_2():
        assert True

    def step_3():
        assert True

    add_step(json_metadata, "example step 1", step_1)
    add_step(json_metadata, "example step 2", step_2)
    add_step(json_metadata, "example step 1", step_3)
    assert True

```
