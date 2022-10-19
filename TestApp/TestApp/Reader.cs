using System;
using System.IO;

namespace TestApp
{
    class Reader
    {
        public static bool FileNotFoundException { get; private set; }

        public static void Lezen(string bestandsnaam)
        {
            if (FileNotFoundException == true)
            {
                Console.WriteLine("FOUT: het bestand bestaat niet");
                return;
            }
            string[] csvLines = File.ReadAllLines(bestandsnaam);

            Console.WriteLine("Nu uitvoeren bestand:" + bestandsnaam);
            for (int i = 0; i < csvLines.Length; i++)
            {
                Console.WriteLine(csvLines[i]);
            }
        }
    }
    public class Positie
    {
        public string Joint, X, Y, Z;
        public Positie(string rowData)
        {
            string[] data = rowData.Split(';');
            this.Joint = data[0];
            this.X = data[1];
            this.Y = data[2];
            this.Z = data[3];
        }
        public override string ToString()
        {
            string resultaat = $"{Joint} {X} {Y} {Z}";
            return resultaat;
        }
    }
}