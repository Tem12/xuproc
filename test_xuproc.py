"""
Brief: Test file for xuproc.py, the JUnit XML file processing script.
Author: Tomas Hladky
Date: 04.10.2024
"""

import pytest
import xuproc


def test_inputs():
    """Test invalid file inputs"""
    with pytest.raises(SystemExit) as e:
        xuproc.process_file(None)
    assert e.type == SystemExit
    assert e.value.code == xuproc.EXIT_FAILURE_ARG

    with pytest.raises(SystemExit) as e:
        xuproc.process_file("unexisting.file")
    assert e.value.code == xuproc.EXIT_FAILURE_FILE_NOT_FOUND


def test_parsing(tmp_path):
    """Test XML parsing"""
    xml_invalid_file_content = """
    <testsuite>
        <<<testcase classname="org.example" name="method1" />
    </testsuite>
    """
    xml_invalid_file = tmp_path / "xml_invalid_file.xml"
    xml_invalid_file.write_text(xml_invalid_file_content)
    with pytest.raises(SystemExit) as e:
        xuproc.process_file(str(xml_invalid_file))
    assert e.value.code == xuproc.EXIT_FAILURE_PARSE

    xml_missing_classname_content = """
    <testsuite>
        <testcase name="method1" />
    </testsuite>
    """
    xml_missing_classname = tmp_path / "xml_missing_classname.xml"
    xml_missing_classname.write_text(xml_missing_classname_content)
    with pytest.raises(SystemExit) as e:
        xuproc.process_file(str(xml_missing_classname))
    assert e.type == SystemExit
    assert e.value.code == xuproc.EXIT_FAILURE_CLASSNAME

    xml_missing_name_content = """
    <testsuite>
        <testcase classname="org.example" />
    </testsuite>
    """
    xml_missing_name = tmp_path / "xml_missing_name.xml"
    xml_missing_name.write_text(xml_missing_name_content)
    with pytest.raises(SystemExit) as e:
        xuproc.process_file(str(xml_missing_name))
    assert e.type == SystemExit
    assert e.value.code == xuproc.EXIT_FAILURE_NAME


def test_valid_process(tmp_path, capsys):
    """Test valid XML modification"""
    xml_valid_content = """
    <testsuite>
        <testcase classname="org.example" name="method" />
    </testsuite>
    """
    xml_valid = tmp_path / "xml_valid.xml"
    xml_valid.write_text(xml_valid_content)
    xuproc.process_file(str(xml_valid))
    captured = capsys.readouterr()

    assert (
        captured.out.replace("    ", "").replace("\n", "")
        == """<?xml version='1.0' encoding='utf-8'?>\
<testsuite><testcase \
classname="org.example" name="org.example.method" \
/></testsuite>"""
    )


def test_content_accumulation(tmp_path, capsys):
    """Test accumulated XML content"""
    xml_acc_content = """
    <testsuite>
        <testcase classname="org.example" name="org.example.method" />
    </testsuite>
    """
    xml_acc = tmp_path / "xml_acc.xml"
    xml_acc.write_text(xml_acc_content)
    xuproc.process_file(str(xml_acc))
    captured = capsys.readouterr()

    # Content should remain unchanged
    assert (
        captured.out.replace("    ", "").replace("\n", "")
        == """<?xml version='1.0' encoding='utf-8'?>\
<testsuite><testcase \
classname="org.example" name="org.example.method" \
/></testsuite>"""
    )
