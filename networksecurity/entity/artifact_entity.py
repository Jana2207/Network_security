from dataclasses import dataclass

# Artifact class to hold file paths for the training and testing datasets
@dataclass
class DataIngestionArtifact:
    trained_file_path: str  # Training dataset file path
    test_file_path: str     # Testing dataset file path

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    
