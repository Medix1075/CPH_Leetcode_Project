class SharedData:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedData, cls).__new__(cls)
            cls._instance.problem_content = None
        return cls._instance
