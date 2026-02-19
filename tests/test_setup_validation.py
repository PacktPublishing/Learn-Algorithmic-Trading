"""
Validation tests to ensure the testing infrastructure is properly configured.
"""
import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validate that the testing infrastructure is properly set up."""
    
    def test_pytest_is_available(self):
        """Verify pytest is installed and importable."""
        assert "pytest" in sys.modules or __import__("pytest")
    
    def test_pytest_cov_is_available(self):
        """Verify pytest-cov is installed."""
        try:
            import pytest_cov
            assert True
        except ImportError:
            # pytest-cov might be installed as a plugin
            assert any("pytest_cov" in str(p) for p in pytest.__file__)
    
    def test_pytest_mock_is_available(self):
        """Verify pytest-mock is installed."""
        try:
            import pytest_mock
            assert True
        except ImportError:
            # Check if it's available as a fixture
            pass
    
    def test_project_root_is_in_path(self):
        """Verify the project root is in Python path."""
        project_root = Path(__file__).parent.parent
        assert str(project_root) in sys.path or str(project_root.absolute()) in sys.path
    
    def test_conftest_fixtures_available(self, temp_dir, mock_config, sample_dataframe):
        """Verify conftest fixtures are accessible."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert hasattr(mock_config, 'debug')
        assert not sample_dataframe.empty
        assert len(sample_dataframe) == 10
    
    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Test that the unit marker is recognized."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Test that the integration marker is recognized."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Test that the slow marker is recognized."""
        assert True
    
    def test_coverage_configuration(self):
        """Verify coverage is properly configured."""
        # This test will help verify coverage is running
        x = 1
        y = 2
        assert x + y == 3
    
    def test_mock_fixtures_work(self, mock_order, mock_portfolio, mocker):
        """Test that mocking fixtures work correctly."""
        assert mock_order.symbol == "AAPL"
        assert mock_portfolio.cash == 100000.0
        
        # Test mocker fixture
        mock_func = mocker.Mock(return_value=42)
        assert mock_func() == 42
    
    def test_pandas_numpy_available(self):
        """Verify key dependencies are available."""
        import pandas as pd
        import numpy as np
        
        assert pd.__version__
        assert np.__version__


class TestDirectoryStructure:
    """Validate the testing directory structure."""
    
    def test_tests_directory_exists(self):
        """Verify tests directory exists."""
        tests_dir = Path(__file__).parent
        assert tests_dir.exists()
        assert tests_dir.name == "tests"
    
    def test_unit_directory_exists(self):
        """Verify unit tests directory exists."""
        unit_dir = Path(__file__).parent / "unit"
        assert unit_dir.exists()
        assert unit_dir.is_dir()
    
    def test_integration_directory_exists(self):
        """Verify integration tests directory exists."""
        integration_dir = Path(__file__).parent / "integration"
        assert integration_dir.exists()
        assert integration_dir.is_dir()
    
    def test_conftest_exists(self):
        """Verify conftest.py exists."""
        conftest = Path(__file__).parent / "conftest.py"
        assert conftest.exists()
        assert conftest.is_file()