from dataclasses import dataclass

# Artifact class to hold file paths for the training and testing datasets
@dataclass
class DataIngestionArtifact:
    trained_file_path: str  
    test_file_path: str     

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    f1_score:str
    precision_score: str
    recall: str
    accuracy: str
    auc_roc: str

@dataclass
class ModelTrainingArtifact:
    trained_model_path : str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
    
