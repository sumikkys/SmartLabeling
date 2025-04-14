# initialize_cache.py
class initialize_cache:
    def __init__(self):
        self.SAM_initialized = False
        self.CLIP_initialized = False

    def set_SAM_initialized(self, status: bool):
        self.SAM_initialized = status
    
    def set_CLIP_initialized(self, status: bool):
        self.CLIP_initialized = status

    def get_SAM_initialized(self) -> bool:
        return self.SAM_initialized
    def get_CLIP_initialized(self) -> bool:
        return self.CLIP_initialized

initialize_manager = initialize_cache()