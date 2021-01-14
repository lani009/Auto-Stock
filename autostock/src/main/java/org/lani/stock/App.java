package org.lani.stock;

import com.jacob.activeX.ActiveXComponent;
import com.jacob.com.Dispatch;
import com.jacob.com.DispatchEvents;
import com.jacob.com.Variant;

public class App
{
    public static void main( String[] args )
    {
        String dllPath = "D:/git/Auto-Stock/autostock/src/dependency/jacob-1.20-x86.dll";

        System.setProperty("jacob.dll.path", dllPath);

        ActiveXComponent kiwoom = new ActiveXComponent("KHOPENAPI.KHOpenAPICtrl.1");


        ActiveXComponent.call(kiwoom, "CommConnect");
        

    }

}