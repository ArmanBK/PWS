using System;
using System.IO;
using UnityEngine;

public class csvReader : MonoBehaviour
{
    public string bestand;
    void Start()
    {

    }
    void FixedUpdate()
    {
        ReadString();
    }
    
    static void ReadString()
    {
        string path = "C:\\Users\\jaspe\\Documents\\GitHub\\PWS\\TestApp\\TestApp\\bin\\Debug\\net6.0\\TestAppOutput.csv";
        //Read the text directly from the test.txt file
        StreamReader reader = new StreamReader(path);
        Debug.Log(reader.ReadToEnd());
        reader.Close();
    }
}