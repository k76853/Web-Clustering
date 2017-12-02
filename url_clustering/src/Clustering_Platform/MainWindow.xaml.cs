using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Forms;
using IronPython;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;

namespace Clustering_Platform
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        string file1 = "";
        string file2 = "";
        public MainWindow()
        {
            InitializeComponent();
            textBox2.Text = "请选择文件";
            textBox.IsEnabled = false;
            textBox1.IsEnabled = false;
            textBox2.IsEnabled = false;
            System.Windows.Forms.Control.CheckForIllegalCrossThreadCalls = false;
        }

        private void openFile(ref string file)
        {
            Microsoft.Win32.OpenFileDialog ofd = new Microsoft.Win32.OpenFileDialog();
            ofd.DefaultExt = ".csv";
            ofd.Filter = "csv file|*.csv";
            if (ofd.ShowDialog() == true)
            {
                file = ofd.FileName;
            }
        }

        private void button_Click(object sender, RoutedEventArgs e)
        {
            openFile(ref file1);
            textBox.Text = file1;
        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            openFile(ref file2);
            textBox1.Text = file2;
        }

        private void button2_Click(object sender, RoutedEventArgs e)
        {
            ScriptRuntime pyRuntime = Python.CreateRuntime(); //创建一下运行环境

            dynamic obj = pyRuntime.UseFile("gid_dic.py"); //调用一个Python文件
            string res = "finish";
            var op = obj.dbscan(ref res, file1, file2);
            textBox2.Text = (string)op;
        }
    }
}
