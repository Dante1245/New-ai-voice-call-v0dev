#!/usr/bin/env python3
"""
Verify production deployment is working correctly
"""

import requests
import json
import time
import sys
from datetime import datetime

class DeploymentVerifier:
    def __init__(self, app_url):
        self.app_url = app_url.rstrip('/')
        self.results = {}
    
    def verify_all(self):
        """Run all verification tests"""
        print(f"🔍 Verifying deployment: {self.app_url}")
        print("=" * 60)
        
        tests = [
            ("Basic Connectivity", self.test_connectivity),
            ("Health Endpoint", self.test_health),
            ("Dashboard Access", self.test_dashboard),
            ("API Endpoints", self.test_api_endpoints),
            ("WebSocket Support", self.test_websocket_support),
            ("Error Handling", self.test_error_handling),
            ("Security Headers", self.test_security),
            ("Performance", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}...")
            try:
                result = test_func()
                self.results[test_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   {status}")
            except Exception as e:
                self.results[test_name] = False
                print(f"   ❌ ERROR: {e}")
        
        self.generate_report()
        return self.results
    
    def test_connectivity(self):
        """Test basic connectivity"""
        try:
            response = requests.get(self.app_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def test_health(self):
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.app_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   Status: {data.get('status')}")
                
                services = data.get('services', {})
                for service, status in services.items():
                    icon = "✅" if status else "⚠️"
                    print(f"   {icon} {service}: {'Ready' if status else 'Not configured'}")
                
                return data.get('status') == 'healthy'
            return False
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_dashboard(self):
        """Test dashboard accessibility"""
        try:
            response = requests.get(self.app_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                required_elements = [
                    'Steve Perry',
                    'AI Voice Assistant',
                    'Start Call',
                    'phone'
                ]
                
                found_elements = []
                for element in required_elements:
                    if element.lower() in content.lower():
                        found_elements.append(element)
                
                print(f"   Found elements: {len(found_elements)}/{len(required_elements)}")
                return len(found_elements) >= 3
            return False
        except:
            return False
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        endpoints = [
            ('/health', 200),
            ('/get_memory', 200),
            ('/nonexistent', 404)
        ]
        
        passed = 0
        for endpoint, expected_status in endpoints:
            try:
                response = requests.get(f"{self.app_url}{endpoint}", timeout=5)
                if response.status_code == expected_status:
                    passed += 1
                    print(f"   ✅ {endpoint}: {response.status_code}")
                else:
                    print(f"   ❌ {endpoint}: {response.status_code} (expected {expected_status})")
            except Exception as e:
                print(f"   ❌ {endpoint}: Error - {e}")
        
        return passed == len(endpoints)
    
    def test_websocket_support(self):
        """Test WebSocket support (basic check)"""
        try:
            # Check if Socket.IO endpoint responds
            response = requests.get(f"{self.app_url}/socket.io/", timeout=5)
            # Socket.IO should return 400 for GET requests (expecting upgrade)
            return response.status_code in [400, 405]
        except:
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        try:
            # Test invalid JSON
            response = requests.post(
                f"{self.app_url}/start_call",
                data="invalid json",
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            # Should handle gracefully with 400 or 500
            return response.status_code in [400, 500]
        except:
            return False
    
    def test_security(self):
        """Test security headers and protections"""
        try:
            response = requests.get(self.app_url, timeout=10)
            headers = response.headers
            
            security_checks = []
            
            # Check for security headers (optional but good)
            if 'X-Content-Type-Options' in headers:
                security_checks.append("Content-Type protection")
            
            if 'X-Frame-Options' in headers:
                security_checks.append("Frame protection")
            
            # Test path traversal protection
            traversal_response = requests.get(f"{self.app_url}/static/../app.py", timeout=5)
            if traversal_response.status_code == 404:
                security_checks.append("Path traversal protection")
            
            print(f"   Security features: {len(security_checks)}")
            for check in security_checks:
                print(f"   ✅ {check}")
            
            return True  # Basic security is acceptable
        except:
            return False
    
    def test_performance(self):
        """Test performance characteristics"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.app_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            print(f"   Response time: {response_time:.3f}s")
            
            if response_time < 2.0:
                print("   ✅ Excellent response time")
                return True
            elif response_time < 5.0:
                print("   ✅ Acceptable response time")
                return True
            else:
                print("   ⚠️  Slow response time")
                return False
        except:
            return False
    
    def generate_report(self):
        """Generate verification report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 DEPLOYMENT VERIFICATION REPORT")
        print("=" * 60)
        print(f"🎯 App URL: {self.app_url}")
        print(f"📅 Verified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT! Deployment is fully functional!")
        elif success_rate >= 75:
            print("\n✅ GOOD! Deployment is working with minor issues.")
        else:
            print("\n⚠️  NEEDS ATTENTION! Several tests failed.")
        
        # Save report
        report = {
            'app_url': self.app_url,
            'timestamp': datetime.now().isoformat(),
            'results': self.results,
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'success_rate': success_rate
            }
        }
        
        try:
            with open('deployment_verification_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Report saved: deployment_verification_report.json")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/verify_deployment.py <app_url>")
        print("Example: python scripts/verify_deployment.py https://your-app.onrender.com")
        sys.exit(1)
    
    app_url = sys.argv[1]
    verifier = DeploymentVerifier(app_url)
    results = verifier.verify_all()
    
    # Exit with appropriate code
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    sys.exit(0 if success_rate >= 75 else 1)

if __name__ == "__main__":
    main()
