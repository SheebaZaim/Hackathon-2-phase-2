import asyncio
from typing import Dict, Any
from datetime import datetime

class HealthCheckService:
    def __init__(self):
        self.start_time = datetime.utcnow()
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks and return the results"""
        checks = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": str(datetime.utcnow() - self.start_time),
            "checks": {
                "database": await self.check_database(),
                "cache": await self.check_cache(),
                "external_services": await self.check_external_services()
            }
        }
        
        # Overall status based on individual checks
        if any(check.get("status") == "unhealthy" for check in checks["checks"].values()):
            checks["status"] = "unhealthy"
            
        return checks
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # In a real implementation, this would check the actual database connection
            # For now, we'll simulate a successful check
            await asyncio.sleep(0.01)  # Simulate async operation
            return {
                "status": "healthy",
                "message": "Database connection successful"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}"
            }
    
    async def check_cache(self) -> Dict[str, Any]:
        """Check cache connectivity"""
        try:
            # In a real implementation, this would check Redis/Memcached connection
            # For now, we'll simulate a successful check
            await asyncio.sleep(0.01)  # Simulate async operation
            return {
                "status": "healthy",
                "message": "Cache connection successful"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Cache connection failed: {str(e)}"
            }
    
    async def check_external_services(self) -> Dict[str, Any]:
        """Check external service dependencies"""
        try:
            # In a real implementation, this would check external API connections
            # For now, we'll simulate a successful check
            await asyncio.sleep(0.01)  # Simulate async operation
            return {
                "status": "healthy",
                "message": "External services accessible"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"External services inaccessible: {str(e)}"
            }

# Singleton instance
health_check_service = HealthCheckService()