package org.lani.stock;

import com.jacob.com.Variant;

public class TestEvent {
    public void OnReceiveConnect(Variant a) {
        System.out.println(a);
    }
}