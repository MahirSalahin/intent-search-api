import time
import logging
import psutil
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import Counter, Histogram, Gauge
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

# Get logger
logger = logging.getLogger("api")
tracer = trace.get_tracer(__name__)

# Prometheus Metrics
REQUESTS = Counter(
    "api_requests_total", "Total count of requests", ["method", "endpoint"]
)
EXCEPTIONS = Counter(
    "api_exceptions_total", "Total count of exceptions", ["endpoint", "exception_type"]
)
LATENCY = Histogram(
    "api_request_duration_seconds", "Request duration", ["method", "endpoint"]
)
ACTIVE_REQUESTS = Gauge("api_active_requests", "Number of currently active requests")

# System metrics
CPU_USAGE = Gauge("api_cpu_usage_percent", "Current CPU usage percentage")
RAM_USAGE = Gauge("api_ram_usage_bytes", "Current RAM usage in bytes")
RAM_USAGE_PERCENT = Gauge("api_ram_usage_percent", "Current RAM usage percentage")

# Process metrics
PROCESS_CPU_USAGE = Gauge(
    "api_process_cpu_usage_percent", "Process CPU usage percentage"
)
PROCESS_RAM_USAGE = Gauge("api_process_ram_usage_bytes", "Process RAM usage in bytes")
PROCESS_RAM_USAGE_PERCENT = Gauge(
    "api_process_ram_usage_percent", "Process RAM usage percentage"
)

# Basic GPU metrics
GPU_COUNT = Gauge('api_gpu_count', 'Number of GPUs detected')
GPU_USAGE = Gauge('api_gpu_usage_percent', 'GPU utilization percentage', ['gpu'])
GPU_MEMORY_USED_BYTES = Gauge('api_gpu_memory_used_bytes', 'GPU memory used in bytes', ['gpu'])
GPU_MEMORY_TOTAL = Gauge('api_gpu_memory_total', 'GPU total memory in bytes', ['gpu'])
GPU_MEMORY_USAGE_PERCENT = Gauge('api_gpu_memory_usage_percent', 'GPU memory usage percentage', ['gpu'])
GPU_TEMPERATURE = Gauge('api_gpu_temperature', 'GPU temperature in Celsius', ['gpu'])
GPU_POWER_USAGE = Gauge('api_gpu_power_usage', 'GPU power usage in Watts', ['gpu'])

# Get current process
current_process = psutil.Process(os.getpid())

# Add this to your middleware.py file

import threading
import time

def start_metrics_collection_thread(interval=15):
    """Start a thread to collect metrics at regular intervals"""
    def collect_metrics():
        while True:
            try:
                update_resource_metrics()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in metrics collection thread: {e}")
                time.sleep(interval)
    
    # Start the collection thread
    collection_thread = threading.Thread(target=collect_metrics, daemon=True)
    collection_thread.start()
    logger.info(f"Started metrics collection thread (interval: {interval}s)")

# Modify your setup_middleware function to start the metrics collection thread
def setup_middleware(app: FastAPI):
    """Configure all middleware for the application"""
    
    # ... existing code ...
    
    # Start periodic metrics collection
    start_metrics_collection_thread(interval=5)  # Update every 5 seconds


# Add/modify this function to handle more gracefully the case where GPU libraries aren't available
def update_resource_metrics():
    """Update all resource metrics"""
    # System metrics
    CPU_USAGE.set(psutil.cpu_percent(interval=None))

    ram = psutil.virtual_memory()
    RAM_USAGE.set(ram.used)
    RAM_USAGE_PERCENT.set(ram.percent)

    # Process metrics
    try:
        PROCESS_CPU_USAGE.set(
            current_process.cpu_percent(interval=None) / psutil.cpu_count()
        )

        process_memory_info = current_process.memory_info()
        PROCESS_RAM_USAGE.set(process_memory_info.rss)  # Resident Set Size
        PROCESS_RAM_USAGE_PERCENT.set(current_process.memory_percent())
    except Exception as e:
        logger.error(f"Error updating process metrics: {e}")

    # GPU metrics - try multiple libraries for flexibility
    try:
        # Fallback approach - always set these to 0 first to ensure we have metrics
        # This ensures the metrics show up in Grafana even if no real data is available
        GPU_COUNT.set(0)
        # Set default values for at least one GPU to ensure metrics exist
        GPU_USAGE.labels(gpu="0").set(0)
        GPU_MEMORY_USED_BYTES.labels(gpu="0").set(0)
        GPU_MEMORY_TOTAL.labels(gpu="0").set(0)
        GPU_MEMORY_USAGE_PERCENT.labels(gpu="0").set(0)
        GPU_TEMPERATURE.labels(gpu="0").set(0)
        GPU_POWER_USAGE.labels(gpu="0").set(0)

        # Try simulating GPU metrics if no real GPU is available
        # This is important for demos and development environments
        simulate_gpu = os.environ.get("SIMULATE_GPU", "false").lower() == "true"
        
        if simulate_gpu:
            # Simulate metrics for a single GPU
            import random
            GPU_COUNT.set(1)
            
            gpu_usage = random.uniform(10, 95)
            GPU_USAGE.labels(gpu="0").set(gpu_usage)
            
            gpu_mem_total = 8 * 1024 * 1024 * 1024  # 8 GB
            gpu_mem_used = int(gpu_mem_total * random.uniform(0.1, 0.9))
            GPU_MEMORY_USED_BYTES.labels(gpu="0").set(gpu_mem_used)
            GPU_MEMORY_TOTAL.labels(gpu="0").set(gpu_mem_total)
            
            mem_percent = (gpu_mem_used / gpu_mem_total) * 100
            GPU_MEMORY_USAGE_PERCENT.labels(gpu="0").set(mem_percent)
            
            GPU_TEMPERATURE.labels(gpu="0").set(random.uniform(40, 80))
            GPU_POWER_USAGE.labels(gpu="0").set(random.uniform(50, 200))
            
            logger.info("Using simulated GPU metrics")
            return

        # First try NVML (NVIDIA Management Library)
        try:
            import pynvml
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            
            # Log diagnostic info
            logger.info(f"NVML detected {device_count} GPUs")
            GPU_COUNT.set(device_count)

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                
                # Get device info for logging
                device_name = pynvml.nvmlDeviceGetName(handle)
                logger.info(f"Processing GPU {i}: {device_name.decode('utf-8') if isinstance(device_name, bytes) else device_name}")

                # GPU utilization
                try:
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    GPU_USAGE.labels(gpu=str(i)).set(utilization.gpu)
                    logger.debug(f"GPU {i} usage: {utilization.gpu}%")
                except Exception as e:
                    logger.warning(f"Failed to get GPU {i} utilization: {e}")
                    GPU_USAGE.labels(gpu=str(i)).set(0)

                # GPU memory
                try:
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    GPU_MEMORY_USED_BYTES.labels(gpu=str(i)).set(memory_info.used)
                    GPU_MEMORY_TOTAL.labels(gpu=str(i)).set(memory_info.total)
                    mem_percent = (memory_info.used / memory_info.total) * 100 if memory_info.total > 0 else 0
                    GPU_MEMORY_USAGE_PERCENT.labels(gpu=str(i)).set(mem_percent)
                    logger.debug(f"GPU {i} memory: {memory_info.used/1024/1024:.1f}MB/{memory_info.total/1024/1024:.1f}MB ({mem_percent:.1f}%)")
                except Exception as e:
                    logger.warning(f"Failed to get GPU {i} memory: {e}")
                    GPU_MEMORY_USED_BYTES.labels(gpu=str(i)).set(0)
                    GPU_MEMORY_TOTAL.labels(gpu=str(i)).set(1)  # Avoid division by zero
                    GPU_MEMORY_USAGE_PERCENT.labels(gpu=str(i)).set(0)

                # GPU temperature
                try:
                    temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    GPU_TEMPERATURE.labels(gpu=str(i)).set(temperature)
                    logger.debug(f"GPU {i} temperature: {temperature}°C")
                except Exception as e:
                    logger.warning(f"Failed to get GPU {i} temperature: {e}")
                    GPU_TEMPERATURE.labels(gpu=str(i)).set(0)

                # GPU power usage
                try:
                    power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                    GPU_POWER_USAGE.labels(gpu=str(i)).set(power_usage)
                    logger.debug(f"GPU {i} power: {power_usage:.1f}W")
                except Exception as e:
                    logger.warning(f"Failed to get GPU {i} power usage: {e}")
                    GPU_POWER_USAGE.labels(gpu=str(i)).set(0)

            pynvml.nvmlShutdown()
            logger.info(f"Updated GPU metrics via NVML - found {device_count} GPUs")
            
        except Exception as nvml_error:
            logger.warning(f"NVML initialization failed: {nvml_error}")
            # Try GPUtil as a fallback
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                
                # Log diagnostic info
                logger.info(f"GPUtil detected {len(gpus)} GPUs")
                GPU_COUNT.set(len(gpus))

                for i, gpu in enumerate(gpus):
                    # Log GPU info
                    logger.info(f"Processing GPU {i}: {gpu.name}")
                    
                    # Set metrics
                    GPU_USAGE.labels(gpu=str(i)).set(gpu.load * 100)
                    GPU_MEMORY_USED_BYTES.labels(gpu=str(i)).set(gpu.memoryUsed * 1024 * 1024)
                    GPU_MEMORY_TOTAL.labels(gpu=str(i)).set(gpu.memoryTotal * 1024 * 1024)
                    GPU_MEMORY_USAGE_PERCENT.labels(gpu=str(i)).set(gpu.memoryUtil * 100)
                    GPU_TEMPERATURE.labels(gpu=str(i)).set(gpu.temperature)
                    # GPUtil doesn't provide power usage
                    GPU_POWER_USAGE.labels(gpu=str(i)).set(0)
                    
                    # Log metrics
                    logger.debug(f"GPU {i} usage: {gpu.load * 100:.1f}%, memory: {gpu.memoryUtil * 100:.1f}%, temperature: {gpu.temperature}°C")
                
                logger.info(f"Updated GPU metrics via GPUtil - found {len(gpus)} GPUs")
                
            except Exception as gputil_error:
                logger.warning(f"GPUtil initialization failed: {gputil_error}")
                
                # Last resort: manually simulate a GPU with mock data if requested
                GPU_COUNT.set(0)
                logger.debug("No GPU monitoring libraries available or no GPUs detected")
                    
    except Exception as e:
        logger.error(f"Error updating GPU metrics: {e}")


def setup_middleware(app: FastAPI):
    """Configure all middleware for the application"""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request metrics and tracing middleware
    @app.middleware("http")
    async def metrics_and_tracing_middleware(request: Request, call_next):
        method = request.method
        endpoint = request.url.path

        # Increment active requests for all endpoints
        ACTIVE_REQUESTS.inc()

        try:
            # Skip tracing for excluded endpoints
            if endpoint != "/metrics":
                with tracer.start_as_current_span(
                    name=f"{method} {endpoint}",
                    kind=trace.SpanKind.SERVER,
                ) as span:
                    try:
                        # Add request details to span
                        span.set_attribute("http.method", method)
                        span.set_attribute("http.url", str(request.url))
                        span.set_attribute("http.route", endpoint)

                        # Add custom attributes if needed
                        client_ip = request.client.host if request.client else "unknown"
                        span.set_attribute("client.ip", client_ip)

                        # Standard metrics
                        REQUESTS.labels(method=method, endpoint=endpoint).inc()
                        start_time = time.time()

                        # Update resource metrics
                        update_resource_metrics()

                        # Execute the request
                        response = await call_next(request)

                        # Add response information to span
                        span.set_attribute("http.status_code", response.status_code)
                        duration = time.time() - start_time
                        span.set_attribute("duration_ms", duration * 1000)

                        # Update metrics
                        LATENCY.labels(method=method, endpoint=endpoint).observe(
                            duration
                        )

                        return response

                    except Exception as e:
                        # Handle exceptions
                        exception_type = type(e).__name__
                        EXCEPTIONS.labels(
                            endpoint=endpoint, exception_type=exception_type
                        ).inc()

                        # Add error details to span
                        span.set_status(Status(StatusCode.ERROR))
                        span.record_exception(e)
                        span.set_attribute("error.type", exception_type)
                        span.set_attribute("error.message", str(e))

                        logger.error(f"500 - ❌ Exception on {method} {endpoint}: {e}")
                        raise
            else:
                # For excluded endpoints, just process without tracing
                update_resource_metrics()
                REQUESTS.labels(method=method, endpoint=endpoint).inc()
                start_time = time.time()
                response = await call_next(request)
                duration = time.time() - start_time
                LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
                return response
        finally:
            # Always decrement active requests counter, regardless of endpoint
            ACTIVE_REQUESTS.dec()

    # Update the exception handlers to include tracing
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Custom handler for HTTP exceptions"""
        current_span = trace.get_current_span()
        if current_span:
            current_span.set_attribute("error.type", "HTTPException")
            current_span.set_attribute("error.status_code", exc.status_code)
            current_span.set_attribute("error.detail", str(exc.detail))
            current_span.set_status(Status(StatusCode.ERROR))

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Custom handler for validation errors"""
        current_span = trace.get_current_span()
        if current_span:
            error_messages = [f"{err['loc']}: {err['msg']}" for err in exc.errors()]
            current_span.set_attribute("error.type", "ValidationError")
            current_span.set_attribute("error.detail", "; ".join(error_messages))
            current_span.set_status(Status(StatusCode.ERROR))

        return JSONResponse(
            status_code=422,
            content={"detail": [err for err in exc.errors()]},
        )
        
        
import os
import random
import time
import threading

# Define this function if it doesn't exist
def enable_gpu_simulation():
    """Enable GPU simulation and start a simulation thread"""
    os.environ["SIMULATE_GPU"] = "true"
    logger.info("GPU simulation enabled - simulating metrics for demo")
    
    # Force an immediate update
    update_resource_metrics()
    
    # Start a thread to continuously update simulated metrics
    def simulate_gpu_metrics():
        while True:
            try:
                if os.environ.get("SIMULATE_GPU", "false").lower() == "true":
                    # Setup simulation values with some variance
                    GPU_COUNT.set(1)  # Simulate one GPU
                    
                    # GPU Usage varies between 10-95% with some randomness to simulate workload
                    gpu_usage = random.uniform(10, 95)
                    GPU_USAGE.labels(gpu="0").set(gpu_usage)
                    
                    # GPU Memory (8GB total with varying usage)
                    gpu_mem_total = 8 * 1024 * 1024 * 1024  # 8 GB in bytes
                    gpu_mem_used = int(gpu_mem_total * random.uniform(0.1, 0.9))
                    GPU_MEMORY_USED_BYTES.labels(gpu="0").set(gpu_mem_used)
                    GPU_MEMORY_TOTAL.labels(gpu="0").set(gpu_mem_total)
                    
                    # Calculate percentage - explicitly ensure this is set
                    mem_percent = (gpu_mem_used / gpu_mem_total) * 100
                    GPU_MEMORY_USAGE_PERCENT.labels(gpu="0").set(mem_percent)
                    
                    # Temperature between 40-80°C
                    GPU_TEMPERATURE.labels(gpu="0").set(random.uniform(40, 80))
                    
                    # Power usage between 50-200W
                    GPU_POWER_USAGE.labels(gpu="0").set(random.uniform(50, 200))
                    
                    logger.debug(f"Updated simulated GPU metrics: usage={gpu_usage:.1f}%, memory={mem_percent:.1f}%")
            except Exception as e:
                logger.error(f"Error in GPU simulation thread: {e}")
            
            time.sleep(5)  # Update every 5 seconds
    
    # Start simulation in background thread
    sim_thread = threading.Thread(target=simulate_gpu_metrics, daemon=True)
    sim_thread.start()
    
    return {"status": "GPU simulation enabled", "thread_started": True}