#!/usr/bin/env python3
"""
Test zero-copy buffer methods in PyPayload
"""

import rsocket_rust

def test_zero_copy_methods():
    print("🧪 Testing zero-copy buffer methods...")
    
    test_data = b"Hello, zero-copy world!"
    test_metadata = b"metadata content"
    
    payload = rsocket_rust.Payload(test_data, test_metadata)
    
    print(f"✅ Created payload with data: {test_data}")
    print(f"✅ Created payload with metadata: {test_metadata}")
    
    print("\n📦 Testing traditional Vec<u8> methods:")
    data_vec = payload.data()
    metadata_vec = payload.metadata()
    print(f"  data(): {data_vec}")
    print(f"  metadata(): {metadata_vec}")
    
    print("\n🚀 Testing zero-copy buffer methods:")
    try:
        data_buffer = payload.data_buffer()
        metadata_buffer = payload.metadata_buffer()
        print(f"  data_buffer(): {data_buffer}")
        print(f"  metadata_buffer(): {metadata_buffer}")
        
        if data_buffer:
            print(f"  data_buffer type: {type(data_buffer)}")
            print(f"  data_buffer content: {bytes(data_buffer)}")
        
        if metadata_buffer:
            print(f"  metadata_buffer type: {type(metadata_buffer)}")
            print(f"  metadata_buffer content: {bytes(metadata_buffer)}")
            
    except Exception as e:
        print(f"❌ Buffer methods error: {e}")
    
    print("\n🔍 Testing memoryview methods:")
    try:
        data_mv = payload.data_memoryview()
        metadata_mv = payload.metadata_memoryview()
        print(f"  data_memoryview(): {data_mv}")
        print(f"  metadata_memoryview(): {metadata_mv}")
        
        if data_mv:
            print(f"  data_memoryview type: {type(data_mv)}")
            print(f"  data_memoryview content: {bytes(data_mv)}")
        
        if metadata_mv:
            print(f"  metadata_memoryview type: {type(metadata_mv)}")
            print(f"  metadata_memoryview content: {bytes(metadata_mv)}")
            
    except Exception as e:
        print(f"❌ Memoryview methods error: {e}")
    
    print("\n✅ Zero-copy testing completed!")

if __name__ == '__main__':
    test_zero_copy_methods()
