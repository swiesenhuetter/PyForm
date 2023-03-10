using System;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;

namespace PyForm
{
    public partial class Form1 : Form
    {
        public delegate void TextSetterDelegate(string text);
        public TextSetterDelegate _delegate;
        public event EventHandler Awake;
        public Form1()
        {
            InitializeComponent();
            _delegate = new TextSetterDelegate(set_text);
        }

        private void set_text(string text)
        {
            if (InvokeRequired)
            {
                Invoke(_delegate, text);
            }
            label1.Text = text;
        }

        protected virtual void OnAwake(EventArgs e)
        {
            EventHandler handler = Awake;
            if (handler != null)
            {
                handler(this, e);
            }
        }


        public void run_cmd()
        {
            var t = Task.Factory.StartNew(() => {
                set_text("Sleeping");
                Thread.Sleep(1000);
                set_text("back from sleep " + Thread.CurrentThread.ManagedThreadId);
                OnAwake(EventArgs.Empty);
            });
        }

        private void button_run_Click(object sender, EventArgs e)
        {
            run_cmd();
        }
    }
}
