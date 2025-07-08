#!/usr/bin/env python3
"""
Test Reactive Streaming Example
Tests reactive streaming with timing measurements.
"""

import asyncio
import time
import rsocket_rust

async def test_reactive_streaming():
    """Test reactive streaming with timing"""
    print("🧪 Testing Reactive Streaming")
    
    try:
        client = await rsocket_rust.RSocketFactory.connect_tcp(
            rsocket_rust.TcpClientTransport("127.0.0.1:7880")
        )
        
        print("✅ Connected to reactive stream server")
        
        payload = (rsocket_rust.Payload.builder()
                   .set_data_utf8("Test reactive streaming")
                   .build())
        
        print("📤 Testing request-response...")
        response = await client.request_response(payload)
        if response:
            print(f"📥 Response: {response.data_utf8()}")
        
        print("\n📤 Testing reactive streaming...")
        stream_payload = (rsocket_rust.Payload.builder()
                          .set_data_utf8("Stream test data")
                          .build())
        
        start_time = time.time()
        print(f"⏱️  Stream started at: {start_time:.3f}")
        
        responses = await client.request_stream(stream_payload)
        end_time = time.time()
        
        print(f"📥 Received {len(responses)} stream items in {end_time - start_time:.3f} seconds:")
        for i, resp in enumerate(responses):
            print(f"   {i+1}: {resp.data_utf8()}")
            
        print(f"⏱️  Total streaming time: {end_time - start_time:.3f} seconds")
        
        if end_time - start_time > 0.4:  # Should take at least 0.5 seconds with delays
            print("✅ Streaming appears to be reactive (took time to complete)")
        else:
            print("⚠️  Streaming completed very quickly - may not be truly reactive")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

async def main():
    """Main test function"""
    await asyncio.sleep(2)  # Wait for server to start
    await test_reactive_streaming()

if __name__ == "__main__":
    asyncio.run(main())
