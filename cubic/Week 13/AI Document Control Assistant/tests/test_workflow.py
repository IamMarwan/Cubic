import pytest
from app.models import WorkflowState, validate_transition

def test_valid_transition():
    validate_transition(WorkflowState.DRAFT, WorkflowState.IN_REVIEW)

def test_invalid_transition():
    with pytest.raises(ValueError):
        validate_transition(WorkflowState.DRAFT, WorkflowState.ISSUED)
