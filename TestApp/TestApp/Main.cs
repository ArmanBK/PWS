﻿using System;
using System.IO;

namespace TestApp
{
    internal class Program
    {
        static void Main(string[] bestandsnaam)
        {
            if (bestandsnaam.Length == 0)
            {
                Console.WriteLine("FOUT: Geef een bestandsnaam op");
                return;
            }
            else if (bestandsnaam.Length > 1)
            {
                Console.WriteLine("FOUT: Je mag maar 1 bestandsnaam opgeven");
                return;
            }
            Console.WriteLine("*******Welkom in TestApp*******");
            TestApp.Reader.Lezen(bestandsnaam[0]);
            Console.WriteLine("Einde programma");
        }
    }
}