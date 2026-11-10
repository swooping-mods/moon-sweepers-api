"""Actual C# -> C calls using an installed compiler, never a game or package host."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOTNET = os.environ.get('MOON_API_DOTNET') or shutil.which('dotnet')


@unittest.skipUnless(DOTNET, 'Optional C# client checks require installed dotnet or MOON_API_DOTNET; no download')
class ManagedClientChecks(unittest.TestCase):
    def test_actual_native_lookup_readiness_and_typed_calls(self):
        dotnet=Path(DOTNET).resolve()
        sdk=dotnet.parent
        compiler=next(iter(sorted((sdk/'sdk').glob('*/Roslyn/bincore/csc.dll'),reverse=True)),None)
        refs=next(iter(sorted((sdk/'packs/Microsoft.NETCore.App.Ref').glob('*/ref/net*'),reverse=True)),None)
        runtime=next(iter(sorted((sdk/'shared/Microsoft.NETCore.App').iterdir(),reverse=True)),None)
        self.assertIsNotNone(compiler,'Installed C# compiler required')
        self.assertIsNotNone(refs,'Installed reference pack required')
        self.assertIsNotNone(runtime,'Installed runtime required')
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory);library=output/'fixture.so';target=output/'Checks.dll'
            env={**os.environ,'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_NOLOGO':'1'}
            commands=[['clang','-std=c11','-Wall','-Wextra','-Werror','-O2','-fPIC','-shared',
                       str(ROOT/'tests/fixtures/managed_runtime_fixture.c'),'-o',str(library)],
                      [str(dotnet),str(compiler),'/nologo','/noconfig','/nostdlib+','/nullable:enable',
                       '/langversion:latest','/optimize+','/target:exe','/out:'+str(target),
                       *['/reference:'+str(p) for p in sorted(refs.glob('*.dll'))],
                       str(ROOT/'managed/MoonSweepers.Api/RuntimeClient.cs'),str(ROOT/'tests/fixtures/ManagedRuntimeChecks.cs')]]
            for command in commands:
                run=subprocess.run(command,capture_output=True,text=True,env=env,timeout=60)
                self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            (output/'Checks.runtimeconfig.json').write_text(json.dumps({'runtimeOptions':{
                'tfm':refs.name,'framework':{'name':'Microsoft.NETCore.App','version':runtime.name}}}))
            run=subprocess.run([str(dotnet),str(target),str(library)],capture_output=True,text=True,env=env,timeout=30)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            self.assertIn('native managed lookup/readiness/ABI/GC checks passed',run.stdout)
