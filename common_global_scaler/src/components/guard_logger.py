import os

class GuardLogger:
    def __init__(self, enable_proactive=False, enable_proactive_reactive=False):
        self.enable_proactive = enable_proactive
        self.enable_proactive_reactive = enable_proactive_reactive
    
    @classmethod
    def from_env(cls):
        """Create logger from environment variables."""
        proactive = os.environ.get("PROACTIVE", "false").lower() == 'true'
        proactive_reactive = proactive and os.environ.get("PROACTIVE_REACTIVE", "false").lower() == 'true'
        return cls(enable_proactive=proactive, enable_proactive_reactive=proactive_reactive)
    
    def log_metrics(self, iter_num, avg_lat, measured_workload, current_mcl, config, 
                   total_requests=0, completed=0, loss=0, pred_workload=None, mixed_workload=None):
        """Log metrics in the exact same format as the original code."""
        
        log_str = f"{iter_num} {avg_lat}"
    
        if self.enable_proactive and pred_workload is not None:
            log_str += f" next: {pred_workload}"
        
        log_str += f" measured: {measured_workload}"
        
        if self.enable_proactive_reactive and mixed_workload is not None:
            log_str += f" mixed: {mixed_workload}"
        
        log_str += f" tot: {total_requests} comp: {completed} rej: {loss} supp: {current_mcl} inst: {config}"
        
        print(log_str, flush=True)
        return log_str