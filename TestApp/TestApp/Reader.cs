using System;
using System.IO;

namespace TestApp
{
    class Reader
    {
        public static void Lezen(string bestandsnaam)
        {
            string[] csvLines = File.ReadAllLines(bestandsnaam);
            Console.WriteLine("Geef een delay in ms");
            int delay = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Nu uitvoeren bestand:" + bestandsnaam + " met delay:" + delay);
            for (int i = 0; i < csvLines.Length; i++)
            {
                Thread.Sleep(delay);
                Console.WriteLine(csvLines[i]);
            }
        }
    }
    public class Positie
    {
        public string Scapula_X, Scapula_Y, Scapula_Z, Shoulder_X, Shoulder_Y, Shoulder_Z, Elbow_X, Elbow_Y, Elbow_Z, Wrist_X, Wrist_Y, Wrist_Z;
        public Positie(string rowData)
        {
            
            string[] data = rowData.Split(';');
            this.Scapula_X = data[0];
            this.Scapula_Y = data[1];
            this.Scapula_Z = data[2];
            this.Shoulder_X = data[3];
            this.Shoulder_Y = data[4];
            this.Shoulder_Z = data[5];
            this.Elbow_X = data[6];
            this.Elbow_Y = data[7];
            this.Elbow_Z = data[8];
            this.Wrist_X = data[9];
            this.Wrist_Y = data[10];
            this.Wrist_Z = data[11];

        }
        public override string ToString()
        {
            string resultaat = $"{Scapula_X} {Scapula_Y} {Scapula_Z} {Shoulder_X} {Shoulder_Y} {Shoulder_Z} {Elbow_X} {Elbow_Y} {Elbow_Z} {Wrist_X} {Wrist_Y} {Wrist_Z}";
            return resultaat;
        }
    }
}