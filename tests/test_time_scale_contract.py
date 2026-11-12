"""Pure admission checks; synthetic offers do not qualify a real adapter."""
import copy
import unittest

from test_compatibility import modern, profile, target
from test_runtimes import managed
from moon_mod_api import compatibility as compat, packages


class TimeScaleContractChecks(unittest.TestCase):
    def setUp(self):
        self.mod = modern(clock=False)
        self.mod["requires_game"] = {"unity.time-scale": {"abi": 1, "min_size": 16}}

    def evaluate(self, row):
        row["digest"] = compat.profile_digest(row)
        return compat.evaluate({self.mod["id"]: self.mod}, [self.mod["id"]],
                               row["hashes"], **target(row))

    def test_clock_offer_does_not_implicitly_grant_time_scale(self):
        self.assertFalse(self.evaluate(profile())["allowed"])

    def test_independent_scale_offer_accepts_only_matching_contract(self):
        row = profile()
        row["capabilities"] = {"unity.time-scale": {"abi": 1, "size": 16}}
        result = self.evaluate(row)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["status"], "requirements-matched")
        self.assertEqual(result["verification"], [])
        for change in ({"abi": 2}, {"size": 15}):
            changed = copy.deepcopy(row)
            changed["capabilities"]["unity.time-scale"].update(change)
            self.assertFalse(self.evaluate(changed)["allowed"])

    def test_old_managed_plugin_cannot_relabel_itself_as_adapter_consumer(self):
        plugin = managed()
        plugin.update(game_access="adapter", game_api_abi=1,
                      requires_game=self.mod["requires_game"])
        with self.assertRaisesRegex(ValueError, "native v8"):
            packages.validate(plugin)
