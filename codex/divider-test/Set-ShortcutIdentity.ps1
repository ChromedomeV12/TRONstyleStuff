param([Parameter(Mandatory=$true)][string]$Path)
$ErrorActionPreference = 'Stop'
if (-not ('TronShortcutIdentity' -as [type])) {
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
public static class TronShortcutIdentity {
    [StructLayout(LayoutKind.Sequential)] public struct Key { public Guid fmtid; public uint pid; }
    [StructLayout(LayoutKind.Explicit, Size=24)] public struct Variant {
        [FieldOffset(0)] public ushort type;
        [FieldOffset(8)] public IntPtr pointer;
    }
    [ComImport, Guid("886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface Store {
        void GetCount(out uint count);
        void GetAt(uint index, out Key key);
        void GetValue(ref Key key, out Variant value);
        void SetValue(ref Key key, ref Variant value);
        void Commit();
    }
    public static void Set(string path) {
        object link = Activator.CreateInstance(Type.GetTypeFromCLSID(new Guid("00021401-0000-0000-C000-000000000046")));
        var file = (IPersistFile)link;
        file.Load(path, 2);
        var store = (Store)link;
        var key = new Key { fmtid = new Guid("9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3"), pid = 5 };
        var value = new Variant { type = 31, pointer = Marshal.StringToCoTaskMemUni("com.openai.codex") };
        try { store.SetValue(ref key, ref value); store.Commit(); file.Save(path, true); }
        finally { Marshal.FreeCoTaskMem(value.pointer); Marshal.FinalReleaseComObject(link); }
    }
}
'@
}
[TronShortcutIdentity]::Set($Path)
