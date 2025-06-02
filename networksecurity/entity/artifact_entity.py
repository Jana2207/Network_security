from dataclasses import dataclass

# Artifact class to hold file paths for the training and testing datasets
@dataclass
class DataIngestionArtifact:
    trained_file_path: str  # Training dataset file path
    test_file_path: str     # Testing dataset file path
