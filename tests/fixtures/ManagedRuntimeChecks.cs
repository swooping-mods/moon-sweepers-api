using System;
using System.Runtime.InteropServices;
using MoonSweepers.Api;

internal static class ManagedRuntimeChecks
{
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate void Set(uint value);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate uint Count();
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int Add(int a,int b);
    private static void Check(bool condition) { if (!condition) throw new Exception("Native client assertion failed"); }
    private static void Throws<T>(Action action) where T:Exception
    {
        try { action(); } catch(T) { return; }
        throw new Exception("Expected " + typeof(T).Name);
    }
    public static int Main(string[] args)
    {
        IntPtr module=NativeLibrary.Load(args[0]);
        IntPtr Resolve(string name)=>NativeLibrary.TryGetExport(module,name,out IntPtr p)?p:IntPtr.Zero;
        var mode=Marshal.GetDelegateForFunctionPointer<Set>(Resolve("fixture_mode"));
        var state=Marshal.GetDelegateForFunctionPointer<Set>(Resolve("fixture_state"));
        var count=Marshal.GetDelegateForFunctionPointer<Count>(Resolve("fixture_lookups"));
        for(uint bad=1;bad<=5;bad++) { mode(bad);Check(!RuntimeClient.TryConnect(Resolve,out _)); }
        mode(0);
        Check(!RuntimeClient.TryConnect(name=>name=="MoonLab_RuntimeState_v1"?IntPtr.Zero:Resolve(name),out _));
        Check(RuntimeClient.TryConnect(Resolve,out var connected));
        RuntimeClient client=connected!;
        Check(client.State==NativeRuntimeState.Pending);
        Check(!client.TryFind("3d-tools","math--plus-",7,16,out _)&&count()==0);
        state(1);
        Check(client.TryFind("3d-tools","math--plus-",7,16,out IntPtr table));
        Check(client.TryFind("3d-tools","math--plus-",7,8,out _));
        Check(!client.TryFind("3d-tools","math--plus-",8,16,out _));
        Check(!client.TryFind("3d-tools","math--plus-",7,17,out _));
        Check(!client.TryFind("unselected-author","missing",7,16,out _));
        var add=Marshal.GetDelegateForFunctionPointer<Add>(Marshal.ReadIntPtr(table,8));
        Check(add(20,22)==42);
        GC.Collect();GC.WaitForPendingFinalizers();GC.Collect();
        for(int i=0;i<10000;i++)Check(add(i,2)==i+2);
        foreach(string bad in new[]{"Upper","a--b","a-","a\0b","../author"})
            Throws<ArgumentException>(()=>client.TryFind(bad,"valid",1,16,out _));
        foreach(string bad in new[]{"1service","a..b","a.1b","a\0b","../service"})
            Throws<ArgumentException>(()=>client.TryFind("author",bad,1,16,out _));
        Throws<ArgumentException>(()=>client.TryFind("author","valid",0,16,out _));
        Throws<ArgumentException>(()=>client.TryFind("author","valid",1,65537,out _));
        state(2);Throws<InvalidOperationException>(()=>client.TryFind("3d-tools","math--plus-",7,16,out _));
        state(3);Throws<InvalidOperationException>(()=>_ = client.State);
        Console.WriteLine("native managed lookup/readiness/ABI/GC checks passed");
        // Loader and table residency is process lifetime, including the fixture.
        GC.KeepAlive(client);return 0;
    }
}
