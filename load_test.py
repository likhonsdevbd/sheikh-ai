#!/usr/bin/env python3
"""
Sheikh AI Load Testing Script
This script performs basic load testing on the Sheikh AI application
"""

import asyncio
import aiohttp
import time
import statistics
from datetime import datetime
import json
import argparse
import sys

class LoadTester:
    def __init__(self, base_url="http://localhost:8000/api/v1", concurrent_users=10, test_duration=30):
        self.base_url = base_url.rstrip('/')
        self.concurrent_users = concurrent_users
        self.test_duration = test_duration
        self.results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'start_time': None,
            'end_time': None,
            'errors': []
        }
    
    async def make_request(self, session, endpoint, method='GET', data=None):
        """Make a single HTTP request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            start_time = time.time()
            
            if method.upper() == 'GET':
                async with session.get(url) as response:
                    await response.text()
                    status = response.status
            elif method.upper() == 'POST':
                async with session.post(url, json=data) as response:
                    await response.text()
                    status = response.status
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            return {
                'success': 200 <= status < 400,
                'status_code': status,
                'response_time': response_time,
                'endpoint': endpoint,
                'error': None
            }
            
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            return {
                'success': False,
                'status_code': None,
                'response_time': response_time,
                'endpoint': endpoint,
                'error': str(e)
            }
    
    async def user_simulation(self, session, user_id):
        """Simulate a single user making requests"""
        print(f"User {user_id} started")
        
        while time.time() - self.results['start_time'] < self.test_duration:
            # Test different endpoints
            endpoints = [
                ('health', 'GET'),
                ('conversations', 'POST', {'title': f'Load Test Conversation {user_id}'}),
            ]
            
            for endpoint_info in endpoints:
                endpoint = endpoint_info[0]
                method = endpoint_info[1]
                data = endpoint_info[2] if len(endpoint_info) > 2 else None
                
                result = await self.make_request(session, endpoint, method, data)
                await self.record_result(result)
                
                # Small delay between requests
                await asyncio.sleep(0.5)
        
        print(f"User {user_id} finished")
    
    async def record_result(self, result):
        """Record the result of a request"""
        self.results['total_requests'] += 1
        
        if result['success']:
            self.results['successful_requests'] += 1
        else:
            self.results['failed_requests'] += 1
            self.results['errors'].append(result['error'])
        
        self.results['response_times'].append(result['response_time'])
    
    async def run_load_test(self):
        """Run the load test"""
        print(f"🚀 Starting load test with {self.concurrent_users} concurrent users for {self.test_duration} seconds")
        print(f"Target URL: {self.base_url}")
        print("-" * 50)
        
        self.results['start_time'] = time.time()
        
        # Create a single session for connection pooling
        connector = aiohttp.TCPConnector(limit=self.concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Start all user simulations
            tasks = [
                self.user_simulation(session, i) 
                for i in range(self.concurrent_users)
            ]
            
            await asyncio.gather(*tasks)
        
        self.results['end_time'] = time.time()
        self.print_results()
    
    def print_results(self):
        """Print the test results"""
        duration = self.results['end_time'] - self.results['start_time']
        
        print("\n" + "=" * 50)
        print("📊 LOAD TEST RESULTS")
        print("=" * 50)
        
        # Basic statistics
        print(f"Test Duration: {duration:.2f} seconds")
        print(f"Total Requests: {self.results['total_requests']}")
        print(f"Successful Requests: {self.results['successful_requests']}")
        print(f"Failed Requests: {self.results['failed_requests']}")
        
        # Success rate
        success_rate = (self.results['successful_requests'] / self.results['total_requests']) * 100
        print(f"Success Rate: {success_rate:.2f}%")
        
        # Response time statistics
        if self.results['response_times']:
            response_times = self.results['response_times']
            print(f"\n⏱️  Response Time Statistics:")
            print(f"  Average: {statistics.mean(response_times):.2f} ms")
            print(f"  Median: {statistics.median(response_times):.2f} ms")
            print(f"  Min: {min(response_times):.2f} ms")
            print(f"  Max: {max(response_times):.2f} ms")
            print(f"  95th Percentile: {sorted(response_times)[int(len(response_times) * 0.95)]:.2f} ms")
        
        # Performance metrics
        requests_per_second = self.results['total_requests'] / duration
        print(f"\n📈 Performance Metrics:")
        print(f"  Requests per Second: {requests_per_second:.2f}")
        print(f"  Average Response Time: {statistics.mean(self.results['response_times']):.2f} ms" if self.results['response_times'] else "  N/A")
        
        # Error analysis
        if self.results['errors']:
            print(f"\n❌ Errors ({len(self.results['errors'])} total):")
            error_counts = {}
            for error in self.results['errors']:
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {count}x: {error[:100]}...")
        
        # Test verdict
        print(f"\n🏆 Test Verdict:")
        if success_rate >= 95:
            print("  ✅ PASSED - Excellent performance")
        elif success_rate >= 90:
            print("  ⚠️  ACCEPTABLE - Good performance with minor issues")
        elif success_rate >= 80:
            print("  ⚠️  WARNING - Performance needs improvement")
        else:
            print("  ❌ FAILED - Critical performance issues")
        
        # Save results to file
        self.save_results()
    
    def save_results(self):
        """Save results to JSON file"""
        filename = f"load_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Prepare data for JSON serialization
        results_copy = self.results.copy()
        if results_copy['response_times']:
            results_copy['response_times'] = {
                'min': min(results_copy['response_times']),
                'max': max(results_copy['response_times']),
                'mean': statistics.mean(results_copy['response_times']),
                'median': statistics.median(results_copy['response_times']),
                'count': len(results_copy['response_times'])
            }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results_copy, f, indent=2, default=str)
            print(f"\n💾 Results saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Failed to save results: {e}")

async def main():
    parser = argparse.ArgumentParser(description='Sheikh AI Load Testing Tool')
    parser.add_argument('--url', default='http://localhost:8000/api/v1', 
                       help='Base URL of the API (default: http://localhost:8000/api/v1)')
    parser.add_argument('--users', type=int, default=10,
                       help='Number of concurrent users (default: 10)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Test duration in seconds (default: 30)')
    parser.add_argument('--health-only', action='store_true',
                       help='Only test health endpoint')
    
    args = parser.parse_args()
    
    # Test if the server is accessible
    print("🔍 Checking server connectivity...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{args.url}/health") as response:
                if response.status == 200:
                    print("✅ Server is accessible")
                else:
                    print(f"⚠️  Server responded with status {response.status}")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the backend server is running on the specified URL")
        sys.exit(1)
    
    # Run the load test
    tester = LoadTester(
        base_url=args.url,
        concurrent_users=args.users,
        test_duration=args.duration
    )
    
    await tester.run_load_test()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Load test interrupted by user")
    except Exception as e:
        print(f"\n❌ Load test failed: {e}")
        sys.exit(1)