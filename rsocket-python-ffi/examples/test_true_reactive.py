#!/usr/bin/env python3
"""
Test True Reactive Streaming
Tests the improved reactive streaming implementation.
"""

import asyncio
import time
import rsocket_rust

async def test_reactive_streaming():
    """Test true reactive streaming with detailed timing analysis"""
    print("🧪 Testing True Reactive Streaming Implementation")
    print("=" * 60)
    
    try:
        print("🔗 Connecting to reactive server...")
        client = await rsocket_rust.RSocketFactory.connect_tcp(
            rsocket_rust.TcpClientTransport("127.0.0.1:7881")
        )
        print("✅ Connected successfully!")
        print()
        
        print("📤 Test 1: Request-Response (baseline)")
        payload = (rsocket_rust.Payload.builder()
                   .set_data_utf8("Test request-response")
                   .build())
        
        start_time = time.time()
        response = await client.request_response(payload)
        end_time = time.time()
        
        if response:
            print(f"📥 Response: {response.data_utf8()}")
            print(f"⏱️  Time: {(end_time - start_time)*1000:.1f}ms")
        print()
        
        print("📤 Test 2: Request-Stream (reactive generator)")
        stream_payload = (rsocket_rust.Payload.builder()
                          .set_data_utf8("Test reactive streaming")
                          .build())
        
        print("⏱️  Starting stream request...")
        start_time = time.time()
        
        responses = await client.request_stream(stream_payload)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"📥 Received {len(responses)} stream items in {total_time:.3f} seconds")
        print("📋 Stream items:")
        for i, resp in enumerate(responses):
            print(f"   {i+1}: {resp.data_utf8()}")
        
        print(f"⏱️  Average time per item: {(total_time/len(responses)*1000):.1f}ms")
        
        print()
        print("🔍 Reactive Analysis:")
        if total_time > 0.05:  # Should take some time due to reactive delays
            print("✅ Stream took measurable time - appears reactive")
        else:
            print("⚠️  Stream completed very quickly - may be batch processing")
            
        if len(responses) > 3:
            print("✅ Generator produced expected number of items")
        else:
            print("⚠️  Fewer items than expected from generator")
            
        print()
        print("🎯 Expected behavior:")
        print("   - Items should be generated lazily by Python generator")
        print("   - Rust should yield items one by one with small delays")
        print("   - Total time should reflect reactive streaming nature")
        print("   - Should support backpressure and cancellation")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("Waiting for server to start...")
    await asyncio.sleep(2)
    await test_reactive_streaming()

if __name__ == "__main__":
    asyncio.run(main())
