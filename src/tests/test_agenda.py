from io import StringIO

from agenda import agenda


def test_check_cmd_with_no_required_keys_raises_no_error():
    cmd = {"key1": "val1", "key2": "val2"}
    required_keys = []
    agenda.check_cmd(cmd, required_keys)


def test_check_cmd_with_missing_required_keys_raises_KeyError():
    cmd = {"key1": "val1", "key2": "val2"}
    required_keys = ["key3"]
    try:
        agenda.check_cmd(cmd, required_keys)
    except KeyError:
        assert True


def test_check_cmd_with_no_missing_required_keys_raises_no_error():
    cmd = {"key1": "val1", "key2": "val2"}
    required_keys = ["key1"]
    agenda.check_cmd(cmd, required_keys)


def test_build_cmd_str_with_empty_cmd_prefix_raises_ValueError():
    cmd = {"key1": "val1", "key2": "val2"}
    cmd_prefix = ""
    try:
        agenda.build_cmd_str(cmd_prefix, cmd)
    except ValueError:
        assert True


def test_build_cmd_str_with_empty_args_dict_raises_no_error():
    cmd = {}
    cmd_prefix = "baseprog"
    agenda.build_cmd_str(cmd_prefix, cmd)


def test_build_cmd_str_with_non_empty_args_dict_produces_correct_str():
    cmd = {"key1": "val1", "key2": "val2"}
    cmd_prefix = "baseprog"
    s = agenda.build_cmd_str(cmd_prefix, cmd)
    assert s == "baseprog --key1 val1 --key2 val2"


def test_log_line_outputs_correctly():
    output = StringIO()
    agenda.log_line(output, "text1", "text2")
    val = output.getvalue()
    val = val[16:]  # remove datetime
    assert val == "text1 text2\n"
