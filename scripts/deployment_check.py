#!/usr/bin/env python3
"""
Pre-deployment validation and checklist
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentChecker:
    """Pre-deployment validation system"""
    
    def __init__(self):
        self.checks = []
        self.warnings = []
        self.errors = []
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all deployment checks"""
        logger.info("🚀 Pre-Deployment Validation")
        logger.info("=" * 50)
        
        checks = [
            ("Environment Variables", self.check_environment_variables),
            ("Dependencies", self.check_dependencies),
            ("File Structure", self.check_file_structure),
            ("Configuration", self.check_configuration),
            ("Security", self.check_security),
            ("Performance", self.check_performance_settings),
            ("Logging", self.check_logging_setup),
            ("Error Handling", self.check_error_handling),
            ("Documentation", self.check_documentation)
        ]
        
        for check_name, check_func in checks:
            logger.info(f"\n🔍 Checking: {check_name}")
            logger.info("-" * 30)
            
            try:
                result = check_func()
                if result:
                    logger.info(f"✅ {check_name}: PASSED")
                    self.checks.append(f"✅ {check_name}")
                else:
                    logger.warning(f"⚠️  {check_name}: ISSUES FOUND")
                    self.warnings.append(f"⚠️  {check_name}")
            except Exception as e:
                logger.error(f"❌ {check_name}: ERROR - {e}")
                self.errors.append(f"❌ {check_name}: {e}")
        
        return self.generate_deployment_report()
    
    def check_environment_variables(self) -> bool:
        """Check all required environment variables"""
        required_vars = {
            'TWILIO_ACCOUNT_SID': 'Twilio Account SID',
            'TWILIO_AUTH_TOKEN': 'Twilio Auth Token',
            'TWILIO_PHONE_NUMBER': 'Twilio Phone Number',
            'OPENAI_API_KEY': 'OpenAI API Key',
            'ELEVENLABS_API_KEY': 'ElevenLabs API Key',
            'ELEVENLABS_VOICE_ID': 'ElevenLabs Voice ID',
            'SECRET_KEY': 'Flask Secret Key'
        }
        
        missing = []
        placeholder = []
        
        for var, description in required_vars.items():
            value = os.environ.get(var)
            if not value:
                missing.append(f"{var} ({description})")
            elif value.startswith('your_') or value == 'dev-secret-key-change-in-production':
                placeholder.append(f"{var} ({description})")
            else:
                logger.info(f"✅ {var}: Configured")
        
        if missing:
            logger.error(f"❌ Missing variables: {', '.join(missing)}")
        
        if placeholder:
            logger.warning(f"⚠️  Placeholder values: {', '.join(placeholder)}")
        
        return len(missing) == 0 and len(placeholder) == 0
    
    def check_dependencies(self) -> bool:
        """Check all dependencies are installed"""
        try:
            # Check requirements.txt exists
            if not os.path.exists('requirements.txt'):
                logger.error("❌ requirements.txt not found")
                return False
            
            logger.info("✅ requirements.txt found")
            
            # Check critical imports
            critical_imports = [
                'flask',
                'flask_socketio',
                'requests',
                'twilio',
                'openai'
            ]
            
            missing_imports = []
            for module in critical_imports:
                try:
                    __import__(module)
                    logger.info(f"✅ {module}: Available")
                except ImportError:
                    missing_imports.append(module)
                    logger.error(f"❌ {module}: Missing")
            
            if missing_imports:
                logger.error(f"❌ Missing critical modules: {', '.join(missing_imports)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Dependency check failed: {e}")
            return False
    
    def check_file_structure(self) -> bool:
        """Check required file structure"""
        required_files = [
            'app.py',
            'requirements.txt',
            '.env.example',
            'templates/dashboard.html',
            'README.md'
        ]
        
        required_dirs = [
            'static',
            'static/audio',
            'static/recordings',
            'scripts',
            'templates'
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file_path in required_files:
            if os.path.exists(file_path):
                logger.info(f"✅ {file_path}: Found")
            else:
                missing_files.append(file_path)
                logger.error(f"❌ {file_path}: Missing")
        
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                logger.info(f"✅ {dir_path}/: Found")
            else:
                missing_dirs.append(dir_path)
                logger.error(f"❌ {dir_path}/: Missing")
        
        return len(missing_files) == 0 and len(missing_dirs) == 0
    
    def check_configuration(self) -> bool:
        """Check configuration files"""
        try:
            # Check .env.example
            if os.path.exists('.env.example'):
                logger.info("✅ .env.example: Found")
            else:
                logger.warning("⚠️  .env.example: Missing")
            
            # Check .env
            if os.path.exists('.env'):
                logger.info("✅ .env: Found")
            else:
                logger.warning("⚠️  .env: Missing (using environment variables)")
            
            # Check Procfile for deployment
            if os.path.exists('Procfile'):
                logger.info("✅ Procfile: Found")
                with open('Procfile', 'r') as f:
                    content = f.read()
                    if 'gunicorn' in content and 'eventlet' in content:
                        logger.info("✅ Procfile: Properly configured")
                    else:
                        logger.warning("⚠️  Procfile: May need eventlet worker")
            else:
                logger.warning("⚠️  Procfile: Missing (needed for deployment)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration check failed: {e}")
            return False
    
    def check_security(self) -> bool:
        """Check security configurations"""
        security_issues = []
        
        # Check SECRET_KEY
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            security_issues.append("SECRET_KEY not set")
        elif secret_key == 'dev-secret-key-change-in-production':
            security_issues.append("SECRET_KEY is default development value")
        else:
            logger.info("✅ SECRET_KEY: Properly configured")
        
        # Check .gitignore
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
                
            required_ignores = ['.env', '*.log', '__pycache__', '*.pyc']
            missing_ignores = []
            
            for ignore_pattern in required_ignores:
                if ignore_pattern not in gitignore_content:
                    missing_ignores.append(ignore_pattern)
            
            if missing_ignores:
                security_issues.append(f"Missing .gitignore patterns: {', '.join(missing_ignores)}")
            else:
                logger.info("✅ .gitignore: Properly configured")
        else:
            security_issues.append(".gitignore file missing")
        
        # Check for exposed credentials in code
        sensitive_patterns = ['sk-', 'AC', 'auth_token']
        code_files = ['app.py', 'scripts/*.py']
        
        for pattern in code_files:
            if '*' in pattern:
                import glob
                files = glob.glob(pattern)
            else:
                files = [pattern] if os.path.exists(pattern) else []
            
            for file_path in files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        for sensitive in sensitive_patterns:
                            if sensitive in content and 'os.environ' not in content:
                                security_issues.append(f"Potential exposed credential in {file_path}")
                                break
                except Exception:
                    pass
        
        if security_issues:
            for issue in security_issues:
                logger.error(f"❌ Security: {issue}")
            return False
        else:
            logger.info("✅ Security: No issues found")
            return True
    
    def check_performance_settings(self) -> bool:
        """Check performance-related settings"""
        try:
            # Check if gunicorn is in requirements
            if os.path.exists('requirements.txt'):
                with open('requirements.txt', 'r') as f:
                    requirements = f.read()
                    
                if 'gunicorn' in requirements:
                    logger.info("✅ Gunicorn: Listed in requirements")
                else:
                    logger.warning("⚠️  Gunicorn: Not in requirements (needed for production)")
                
                if 'eventlet' in requirements:
                    logger.info("✅ Eventlet: Listed in requirements")
                else:
                    logger.warning("⚠️  Eventlet: Not in requirements (needed for WebSockets)")
            
            # Check for production optimizations in app.py
            if os.path.exists('app.py'):
                with open('app.py', 'r') as f:
                    app_content = f.read()
                    
                if 'debug=False' in app_content or 'debug=self.config' in app_content:
                    logger.info("✅ Debug mode: Properly configured")
                else:
                    logger.warning("⚠️  Debug mode: May be enabled in production")
                
                if 'logging' in app_content:
                    logger.info("✅ Logging: Configured")
                else:
                    logger.warning("⚠️  Logging: Not configured")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance check failed: {e}")
            return False
    
    def check_logging_setup(self) -> bool:
        """Check logging configuration"""
        try:
            if os.path.exists('app.py'):
                with open('app.py', 'r') as f:
                    content = f.read()
                    
                if 'logging.basicConfig' in content or 'logger = logging.getLogger' in content:
                    logger.info("✅ Logging: Configured in application")
                else:
                    logger.warning("⚠️  Logging: Not configured")
                    return False
                
                if 'FileHandler' in content:
                    logger.info("✅ File logging: Configured")
                else:
                    logger.warning("⚠️  File logging: Not configured")
                
                if 'StreamHandler' in content:
                    logger.info("✅ Console logging: Configured")
                else:
                    logger.warning("⚠️  Console logging: Not configured")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Logging check failed: {e}")
            return False
    
    def check_error_handling(self) -> bool:
        """Check error handling implementation"""
        try:
            if os.path.exists('app.py'):
                with open('app.py', 'r') as f:
                    content = f.read()
                    
                error_handling_patterns = [
                    'try:',
                    'except Exception',
                    '@app.errorhandler',
                    'logger.error'
                ]
                
                found_patterns = []
                for pattern in error_handling_patterns:
                    if pattern in content:
                        found_patterns.append(pattern)
                        logger.info(f"✅ Error handling: {pattern} found")
                
                if len(found_patterns) >= 3:
                    logger.info("✅ Error handling: Comprehensive implementation")
                    return True
                else:
                    logger.warning("⚠️  Error handling: Limited implementation")
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error handling check failed: {e}")
            return False
    
    def check_documentation(self) -> bool:
        """Check documentation completeness"""
        docs_score = 0
        
        # Check README.md
        if os.path.exists('README.md'):
            with open('README.md', 'r') as f:
                readme_content = f.read()
                
            required_sections = [
                'Features',
                'Setup',
                'Installation',
                'Usage',
                'API',
                'Environment'
            ]
            
            found_sections = []
            for section in required_sections:
                if section.lower() in readme_content.lower():
                    found_sections.append(section)
            
            docs_score += len(found_sections)
            logger.info(f"✅ README.md: {len(found_sections)}/{len(required_sections)} sections")
        else:
            logger.warning("⚠️  README.md: Missing")
        
        # Check code documentation
        if os.path.exists('app.py'):
            with open('app.py', 'r') as f:
                content = f.read()
                
            if '"""' in content:
                docs_score += 2
                logger.info("✅ Code documentation: Docstrings found")
            else:
                logger.warning("⚠️  Code documentation: Limited docstrings")
        
        # Check .env.example
        if os.path.exists('.env.example'):
            docs_score += 1
            logger.info("✅ Environment documentation: .env.example found")
        else:
            logger.warning("⚠️  Environment documentation: .env.example missing")
        
        return docs_score >= 5
    
    def generate_deployment_report(self) -> Dict[str, Any]:
        """Generate deployment readiness report"""
        total_checks = len(self.checks) + len(self.warnings) + len(self.errors)
        passed_checks = len(self.checks)
        
        readiness_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        if readiness_score >= 90:
            readiness_level = "PRODUCTION READY"
            readiness_icon = "🎉"
        elif readiness_score >= 75:
            readiness_level = "MOSTLY READY"
            readiness_icon = "✅"
        elif readiness_score >= 50:
            readiness_level = "NEEDS WORK"
            readiness_icon = "⚠️"
        else:
            readiness_level = "NOT READY"
            readiness_icon = "❌"
        
        report = {
            'deployment_readiness': {
                'level': readiness_level,
                'score': round(readiness_score, 1),
                'timestamp': datetime.now().isoformat()
            },
            'summary': {
                'total_checks': total_checks,
                'passed': len(self.checks),
                'warnings': len(self.warnings),
                'errors': len(self.errors)
            },
            'details': {
                'passed_checks': self.checks,
                'warnings': self.warnings,
                'errors': self.errors
            },
            'next_steps': self._generate_next_steps(readiness_score)
        }
        
        # Save report
        try:
            with open('deployment_readiness_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            logger.info("📄 Deployment report saved: deployment_readiness_report.json")
        except Exception as e:
            logger.error(f"Failed to save deployment report: {e}")
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("🚀 DEPLOYMENT READINESS REPORT")
        logger.info("=" * 60)
        logger.info(f"{readiness_icon} Status: {readiness_level}")
        logger.info(f"📊 Score: {readiness_score:.1f}%")
        logger.info(f"✅ Passed: {len(self.checks)}")
        logger.info(f"⚠️  Warnings: {len(self.warnings)}")
        logger.info(f"❌ Errors: {len(self.errors)}")
        
        if readiness_score >= 90:
            logger.info("\n🎉 EXCELLENT! Your application is production-ready!")
            logger.info("🚀 You can deploy with confidence!")
        elif readiness_score >= 75:
            logger.info("\n✅ GOOD! Address warnings before deployment.")
        else:
            logger.info("\n⚠️  ATTENTION NEEDED! Please fix errors before deployment.")
        
        return report
    
    def _generate_next_steps(self, score: float) -> List[str]:
        """Generate next steps based on readiness score"""
        steps = []
        
        if self.errors:
            steps.append("🔴 CRITICAL: Fix all errors before deployment")
            steps.extend([f"   - {error}" for error in self.errors])
        
        if self.warnings:
            steps.append("🟡 RECOMMENDED: Address warnings for optimal deployment")
            steps.extend([f"   - {warning}" for warning in self.warnings])
        
        if score >= 90:
            steps.extend([
                "🚀 Deploy to staging environment for final testing",
                "🔍 Run production test suite",
                "📊 Monitor application performance",
                "🎯 Deploy to production"
            ])
        elif score >= 75:
            steps.extend([
                "🔧 Address remaining warnings",
                "🧪 Run comprehensive tests",
                "🚀 Deploy to staging environment"
            ])
        else:
            steps.extend([
                "🔧 Fix critical errors first",
                "📝 Complete missing documentation",
                "🔒 Address security issues",
                "🧪 Run all tests again"
            ])
        
        return steps

def main():
    """Main deployment check execution"""
    print("🚀 AI Voice Assistant - Deployment Readiness Check")
    print("=" * 60)
    
    checker = DeploymentChecker()
    report = checker.run_all_checks()
    
    # Exit with appropriate code
    if report['deployment_readiness']['score'] >= 75:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
