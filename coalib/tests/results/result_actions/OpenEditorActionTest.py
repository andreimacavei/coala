import subprocess
import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction
from coalib.settings.Section import Section, Setting


class ResultActionTest(unittest.TestCase):
    @staticmethod
    def fake_edit(commands):
        filename = commands[1]
        with open(filename) as f:
            lines = f.readlines()

        del lines[1]

        with open(filename, "w") as f:
            f.writelines(lines)

    @staticmethod
    def fake_edit_subl(commands, stdout):
        """
        Solely the declaration raises an exception if stdout not provided.
        """
        assert ("--wait" in commands), "Did not wait for the editor to close"

    def test_apply(self):
        file_dict = {
            "f_a": ["1\n", "2\n", "3\n"],
            "f_b": ["1\n", "2\n", "3\n"],
            "f_c": ["1\n", "2\n", "3\n"]
        }
        expected_file_dict = {
            "f_a": ["1\n", "3\n"],
            "f_b": ["1\n", "3_changed\n"],
            "f_c": ["1\n", "2\n", "3\n"]
        }
        diff_dict = {"f_b": Diff()}
        diff_dict["f_b"].change_line(3, "3\n", "3_changed\n")

        section = Section("")
        section.append(Setting("editor", ""))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit
        diff_dict = uut.apply_from_section(
            Result("origin", "msg", "f_a"),
            file_dict,
            diff_dict,
            section)
        diff_dict = uut.apply_from_section(
            Result("origin", "msg", "f_b"),
            file_dict,
            diff_dict,
            section)

        for filename in diff_dict:
            file_dict[filename] = (
                diff_dict[filename].apply(file_dict[filename]))

        self.assertEqual(file_dict, expected_file_dict)

    def test_subl(self):
        file_dict = {"f_a": []}
        section = Section("")
        section.append(Setting("editor", "subl"))
        uut = OpenEditorAction()
        subprocess.call = self.fake_edit_subl
        diff_dict = uut.apply_from_section(
            Result("origin", "msg", "f_a"),
            file_dict,
            {},
            section)
        file_dict["f_a"] = diff_dict["f_a"].apply(file_dict["f_a"])

        self.assertEqual(file_dict, file_dict)

    def test_is_applicable(self):
        result1 = Result("", "")
        result2 = Result("", "", "")
        invalid_result = ""
        self.assertFalse(OpenEditorAction.is_applicable(result1))
        self.assertTrue(OpenEditorAction.is_applicable(result2))
        self.assertFalse(OpenEditorAction.is_applicable(invalid_result))

if __name__ == '__main__':
    unittest.main(verbosity=2)
