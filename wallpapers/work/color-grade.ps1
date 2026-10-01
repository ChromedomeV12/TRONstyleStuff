Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public class CyanGrade {
 public static void Run(string input, string output) {
  using (var src = new Bitmap(input))
  using (var dst = new Bitmap(src.Width, src.Height, PixelFormat.Format24bppRgb)) {
   using (var g = Graphics.FromImage(dst)) {g.DrawImageUnscaled(src,0,0);}
   var rect = new Rectangle(0,0,dst.Width,dst.Height);
   var data = dst.LockBits(rect, ImageLockMode.ReadWrite, PixelFormat.Format24bppRgb);
   byte[] bytes = new byte[data.Stride*data.Height];
   Marshal.Copy(data.Scan0,bytes,0,bytes.Length);
   double[] levels = {0,.15,.35,.60,.80,1};
   double[,] palette = {{0,0,0},{3,14,22},{7,42,61},{14,112,155},{58,191,225},{206,252,255}};
   for(int y=0;y<data.Height;y++) for(int x=0;x<data.Width;x++) {
    int i=y*data.Stride+x*3;
    double r=bytes[i+2]/255.0,g=bytes[i+1]/255.0,b=bytes[i]/255.0;
    double luminance=.299*r+.587*g+.114*b;
    double v=.8*luminance+.2*Math.Max(r,Math.Max(g,b));
    int k=0; while(k<4 && v>levels[k+1]) k++;
    double t=(v-levels[k])/(levels[k+1]-levels[k]);
    for(int c=0;c<3;c++) bytes[i+2-c]=(byte)Math.Round(palette[k,c]*(1-t)+palette[k+1,c]*t);
   }
   Marshal.Copy(bytes,0,data.Scan0,bytes.Length);
   dst.UnlockBits(data);
   dst.Save(output,ImageFormat.Png);
   Console.WriteLine("Saved color grade: "+dst.Width+" x "+dst.Height+"; pointwise color transform only.");
  }
 }
}
"@
[CyanGrade]::Run((Join-Path $PSScriptRoot '../inputs/source.jpg'),(Join-Path $PSScriptRoot '../outputs/shanghai-tron-color-grade.png'))
