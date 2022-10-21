using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotator : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        var modifiedRotation = transform.rotation;
        modifiedRotation.x = 0;
        transform.rotation = modifiedRotation;
    }
}