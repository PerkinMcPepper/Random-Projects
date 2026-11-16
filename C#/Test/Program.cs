using System;
using System.Windows.Forms;
using System.Drawing;
using System.Runtime.Intrinsics.X86;

float version = 0.0f;

Application.EnableVisualStyles();
Application.SetCompatibleTextRenderingDefault(false);

Form root = new()
{
    Size = new Size(1000, 600),
    Location = new Point(200, 200),
    Text = $"Sifter v{version:F1}",
    Icon = new Icon("images/icon.ico", 16, 16),
    BackColor = new Color()
};

Application.Run(root);