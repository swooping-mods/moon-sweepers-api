"""Exercise independent providers through the real package resolver."""
import copy
import unittest

from test_api import manifest
from moon_mod_api import packages


def provider(name="other-authors-library", maximum=384):
    value = manifest(name)
    value.update(abi="MoonLab_ModStart/v6", runtime_api_abi=1, provides={name + ".building": {
        "abi": 7, "size": 64, "limits": {"build_menu_max_kind": maximum}}})
    return value


def consumer(name="independent-feature", optional=False):
    value = manifest(name)
    value.update(abi="MoonLab_ModStart/v6", runtime_api_abi=1, requires=[] if optional else ["other-authors-library"],
                 requires_apis=[{"api": "other-authors-library.building", "abi": 7,
                                 "min_size": 32, "optional": optional}])
    return value


class InterfaceChecks(unittest.TestCase):
    def resolve(self, values, selected=None):
        return packages.resolve(values, list(values) if selected is None else selected,
                                {"GameAssembly.dll": "a" * 64})

    def test_independent_provider_is_ordered_before_consumer(self):
        library, feature = provider(), consumer()
        for mod in (library, feature):
            packages.validate(mod)
        values = {mod["id"]: mod for mod in (feature, library)}
        self.assertEqual(self.resolve(values), [library["id"], feature["id"]])
        # Capacity is a caller requirement, not knowledge of a particular mod ID.
        feature["requires_apis"][0]["limits"] = {"build_menu_max_kind": 384}
        self.resolve(values)
        library["provides"][library["id"] + ".building"]["limits"]["build_menu_max_kind"] = 224
        with self.assertRaisesRegex(ValueError, "Insufficient API limit"):
            self.resolve(values)

    def test_every_valid_package_identity_can_own_an_interface(self):
        for name in ('3d-tools', 'test-3d', '7'):
            with self.subTest(owner=name):
                library, feature = provider(name), consumer()
                feature['requires'] = [name]
                feature['requires_apis'][0]['api'] = name + '.building'
                for mod in (library, feature): packages.validate(mod)
                values = {mod['id']: mod for mod in (feature, library)}
                self.assertEqual(self.resolve(values), [name, feature['id']])
        for name in ('-bad', 'bad-', 'bad--id', 'Bad'):
            with self.subTest(invalid_owner=name), self.assertRaises(ValueError):
                packages.validate(provider(name))

    def test_missing_dependency_wrong_abi_and_short_table_are_rejected(self):
        library, feature = provider(), consumer()
        values = {mod["id"]: mod for mod in (feature, library)}
        with self.assertRaisesRegex(ValueError, "unavailable"):
            self.resolve(values, [feature["id"]])
        spec = library["provides"][library["id"] + ".building"]
        for change in ({"abi": 8}, {"size": 16}):
            changed = copy.deepcopy(values)
            changed[library["id"]]["provides"][library["id"] + ".building"].update(change)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "ABI/size"):
                self.resolve(changed)
        self.assertEqual(spec["size"], 64)

    def test_target_without_registry_rejects_valid_interface_package(self):
        library = provider()
        args = ({library["id"]: library}, [library["id"]], library["game"]["hashes"])
        with self.assertRaisesRegex(ValueError, "runtime API ABI"):
            packages.resolve(*args, runtime_api_abi=0)
        self.assertEqual(packages.resolve(*args, runtime_api_abi=1), [library["id"]])

    def test_interface_packages_require_an_abi_that_older_loaders_reject(self):
        for change in ({"abi": "MoonLab_ModStart/v5"}, {"runtime_api_abi": None},
                       {"kind": "bepinex-il2cpp", "abi": "BepInEx.IL2CPP/6-be791",
                        "bepinex": {"guid": "author.plugin", "data_root": "Author"}}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                packages.validate({**provider(), **change})

    def test_optional_provider_is_ordered_when_selected_and_not_auto_selected(self):
        library, feature = provider(), consumer(optional=True)
        values = {mod["id"]: mod for mod in (feature, library)}
        self.assertEqual(self.resolve(values, [feature["id"]]), [feature["id"]])
        self.assertEqual(self.resolve(values), [library["id"], feature["id"]])
        library["provides"].clear()
        with self.assertRaisesRegex(ValueError, "unavailable"):
            self.resolve(values)

    def test_managed_consumer_binds_native_contracts_without_publishing(self):
        library, feature = provider(), consumer()
        feature.update(kind='bepinex-il2cpp', abi='BepInEx.IL2CPP/6-be791',
                       bepinex={'guid':'another.author.feature','data_root':'AnotherAuthor'})
        for native_only in ('shared_claims', 'hook_framework_abi'):
            feature.pop(native_only)
        packages.validate(feature)
        values={p['id']:p for p in (feature,library)}
        self.assertEqual(self.resolve(values),[library['id'],feature['id']])
        with self.assertRaisesRegex(ValueError,'readiness ABI'):
            packages.resolve(values,list(values),library['game']['hashes'],
                             runtime_api_abi=1,runtime_readiness_abi=0)
        self.assertEqual(packages.resolve(values,list(values),library['game']['hashes'],
                         runtime_api_abi=1,runtime_readiness_abi=1),[library['id'],feature['id']])
        feature['provides']={feature['id']+'.managed':{'abi':1,'size':16}}
        with self.assertRaisesRegex(ValueError,'cannot publish'):
            packages.validate(feature)

    def test_optional_interface_cycle_is_diagnosed(self):
        a, b = provider("author-a"), provider("author-b")
        for current, other in ((a, b), (b, a)):
            current["requires_apis"] = [{"api": other["id"] + ".building", "abi": 7,
                                         "min_size": 32, "optional": True}]
        with self.assertRaisesRegex(ValueError, "Circular"):
            self.resolve({"author-a": a, "author-b": b})

    def test_foreign_namespace_implicit_dependency_and_bad_metadata_reject(self):
        for change in (
            {"provides": {"someone-else.api": {"abi": 1, "size": 8}}},
            {"provides": {"other-authors-library.api": {"abi": True, "size": 8}}},
            {"provides": {"other-authors-library.api": {"abi": 1, "size": 65537}}},
            {"provides": {"other-authors-library.api": {"abi": 1, "size": 8, "limits": {"count": True}}}},
            {"runtime_api_abi": True},
            {"runtime_api_abi": 2},
            {"requires_apis": [{"api": "independent.api", "abi": 1, "min_size": 8}]},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                packages.validate({**provider(), **change})
        value = consumer()
        value["requires_apis"].append(copy.deepcopy(value["requires_apis"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            packages.validate(value)

    def test_building_framework_can_be_owned_by_another_author(self):
        library, feature = provider(), consumer()
        feature.update(build_api="other-authors-library.building",
                       build_items=[{"kind": 384, "key": feature["id"] + ".power.relay"}])
        packages.validate(feature)
        values = {mod["id"]: mod for mod in (feature, library)}
        self.assertEqual(self.resolve(values), [library["id"], feature["id"]])
        library["provides"][library["id"] + ".building"]["limits"]["build_menu_max_kind"] = 383
        with self.assertRaisesRegex(ValueError, "384"):
            self.resolve(values)

    def test_different_building_apis_still_share_native_saved_identity_space(self):
        a, b = provider(), provider("separate-library")
        first, second = consumer("first-feature"), consumer("second-feature")
        for feature, library in ((first, a), (second, b)):
            api = library["id"] + ".building"
            feature.update(requires=[library["id"]], build_api=api,
                           requires_apis=[{"api": api, "abi": 7, "min_size": 32}],
                           build_items=[{"kind": 256, "key": feature["id"] + ".power.item"}])
        with self.assertRaisesRegex(ValueError, "256"):
            self.resolve({mod["id"]: mod for mod in (a, b, first, second)})


if __name__ == "__main__":
    unittest.main()
